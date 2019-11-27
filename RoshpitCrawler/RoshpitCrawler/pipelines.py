# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

import scrapy
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from .models.item import Item
from .models.item_type import ItemType
from .models.property import Property
from .models.wish import Wish
from .models.wish_property import WishProperty
from .repositories.item_repo import ItemRepo
from .repositories.item_type_repo import ItemTypeRepo
from .repositories.notify_repo import NotifyRepo
from .repositories.parameter_repo import ParameterRepo
from .repositories.property_repo import PropertyRepo
from .repositories.wish_repo import WishRepo
from .services.collect_auction_info_service import CollectAuctionInfoService
from .services.collect_item_info_service import CollectItemInfoService
from .unit_of_works.sqlalchemy_uow import SQLAlchemyUOW


class OrganiseItemDataPipeline(object):

    def process_item(self, item, spider):

        if 'item_type' in item:
            if item['item_type'].get('id'):
                if item['item_type'].get('id') == '-1':
                    item['item_type']['id'] = 'glyph'
                    item['item_type']['name'] = 'Glyph'

        if 'item' in item:
            if item['item'].get('img_url'):
                item['item']['img'] = item['item'].get('img_url').split('/')[-1]

        if 'property' in item:
            if item['property'].get('range'):
                item['property']['min'] = item['property'].get('range').split(' - ')[0]
                item['property']['max'] = item['property'].get('range').split(' - ')[1]

        return item


class StoreItemDataPipeline(object):

    def __init__(self, is_new_db):
        self.is_new_db = is_new_db
        self.collect_item_info_service = CollectItemInfoService(ItemRepo(), ItemTypeRepo(), PropertyRepo(),
                                                                SQLAlchemyUOW())

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            is_new_db=crawler.settings.get('IS_NEW_DB')
        )

    def open_spider(self, spider):
        if self.is_new_db:
            self.collect_item_info_service.delete_all_item_type()
            self.collect_item_info_service.delete_all_item()
            self.collect_item_info_service.delete_all_property()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if 'item_type' in item:
            if self.is_new_db or not self.collect_item_info_service.get_item_type_by_id(
                    ItemType(id=item['item_type'].get('id'))):
                self.collect_item_info_service.add_new_item_type(
                    ItemType(id=item['item_type'].get('id'),
                             name=item['item_type'].get('name'),
                             create_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             modify_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                raise DropItem("Item Type already exists.")

        if 'item' in item:
            if self.is_new_db or not self.collect_item_info_service.get_item_by_id(Item(id=item['item'].get('id'))):
                self.collect_item_info_service.add_new_item(
                    Item(id=item['item'].get('id'),
                         name=item['item'].get('name'),
                         img=item['item'].get('img'),
                         type=item['item'].get('type'),
                         rarity=item['item'].get('rarity'),
                         create_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         modify_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                raise DropItem("Item already exists.")

        if 'property' in item:
            if self.is_new_db or not self.collect_item_info_service.get_property_by_id(
                    Property(id=item['property'].get('id'))):
                self.collect_item_info_service.add_new_property(
                    Property(id=item['property'].get('id'),
                             name=item['property'].get('name'),
                             type=item['property'].get('type'),
                             is_ability=item['property'].get('is_ability'),
                             min=item['property'].get('min'),
                             max=item['property'].get('max'),
                             item_id=item['property'].get('item_id'),
                             create_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             modify_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                raise DropItem("Property already exists.")

        return item


class StoreItemImgPipeline(object):

    def process_item(self, item, spider):

        if 'item' in item:
            if item['item'].get('img_url') is not None:
                data = {'url': item['item'].get('img_url')}
                request = scrapy.Request(get_project_settings().get("IMAGES_STORE_URL"),
                                         body=json.dumps(data),
                                         method='POST',
                                         headers={'Content-Type': 'application/json'})
                spider.crawler.engine.crawl(request, spider)

        return item


class MatchAuctionPipeline(object):

    def __init__(self):
        self.collect_auction_info_service = CollectAuctionInfoService(ItemRepo(), PropertyRepo(), WishRepo(),
                                                                      NotifyRepo(), ParameterRepo(), SQLAlchemyUOW())

    def process_item(self, item, spider):
        if 'auction' in item:
            auction = item['auction']
            wish_properties = []
            for auction_property in auction['action_property']:
                wish_properties.append(
                    WishProperty(
                        roll=auction_property['roll'],
                        property_id=auction_property['property_id'],
                        property=Property(id=auction_property['property'].get('id'),
                                          name=auction_property['property'].get('name'),
                                          type=auction_property['property'].get('type'))))

            wish = Wish(currency=int(auction['currency']),
                        min_level=int(auction['level'] or 0),
                        max_bid=int(auction['bid'] or 0),
                        max_buyout=int(auction['buyout'] or 0),
                        item_id=auction['item_id'],
                        item=Item(id=auction['item'].get('id'), name=auction['item'].get('name')),
                        wish_properties=wish_properties)

            self.collect_auction_info_service.notify_potential_buyer(wish, auction['id'])

        raise DropItem("Auction Not match.")
