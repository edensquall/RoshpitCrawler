# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    id = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    img = scrapy.Field()
    type = scrapy.Field()
    rarity = scrapy.Field()
    pass


class ItemType(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    pass


class Property(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    is_ability = scrapy.Field()
    range = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    item_id = scrapy.Field()
    pass


class Auction(scrapy.Item):
    id = scrapy.Field()
    currency = scrapy.Field()
    level = scrapy.Field()
    bid = scrapy.Field()
    buyout = scrapy.Field()
    item_id = scrapy.Field()
    item = scrapy.Field()
    action_property = scrapy.Field()
    potential_buyers = scrapy.Field()
    pass


class AuctionProperty(scrapy.Item):
    type = scrapy.Field()
    roll = scrapy.Field()
    property_id = scrapy.Field()
    property = scrapy.Field()
    pass


class Buyer(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    notification_method = scrapy.Field()
    notify_tokens = scrapy.Field()
    pass
