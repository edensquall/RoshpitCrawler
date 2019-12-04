import scrapy
from scrapy.spiders import CrawlSpider

from ..items import Auction, AuctionProperty, Property, ItemType, Item
from ..repositories.item_repo import ItemRepo
from ..repositories.notify_repo import NotifyRepo
from ..repositories.parameter_repo import ParameterRepo
from ..repositories.property_repo import PropertyRepo
from ..repositories.wish_repo import WishRepo
from ..services.collect_auction_info_service import CollectAuctionInfoService
from ..unit_of_works.sqlalchemy_uow import SQLAlchemyUOW


class CollectAuctionInfoSpider(CrawlSpider):
    name = 'collect_auction_info'
    custom_settings = {
        'ITEM_PIPELINES': {
            'RoshpitCrawler.pipelines.OrganiseItemDataPipeline': 100,
            'RoshpitCrawler.pipelines.StoreItemDataPipeline': 200,
            'RoshpitCrawler.pipelines.StoreItemImgPipeline': 300,
            'RoshpitCrawler.pipelines.MatchAuctionPipeline': 400
        },
        'IS_NEW_DB': False
    }

    def __init__(self, *args, **kwargs):
        super(CollectAuctionInfoSpider, self).__init__(*args, **kwargs)
        self.collect_auction_info_service = CollectAuctionInfoService(ItemRepo(), PropertyRepo(), WishRepo(),
                                                                      NotifyRepo(), ParameterRepo(), SQLAlchemyUOW())
        self.crawled_auction_id = self.collect_auction_info_service.get_crawled_auction_id()

    def start_requests(self):
        urls = [
            'https://www.roshpit.ca/market/browse'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_auction)

    def parse_auction(self, response):
        auction_id = 0
        for auction_row in reversed(response.css('#search-results-market>a')):

            auction_id = int(auction_row.css('::attr(href)').get().split('/')[-1])
            if auction_id > self.crawled_auction_id:
                item = Item()
                item['name'] = auction_row.css('.shop-search-row>div:nth-of-type(2)>span::text').get()
                item['id'] = item['name'].replace(' ', '')
                item['img_url'] = auction_row.css('.shop-search-row>div:nth-of-type(2) img::attr(src)').get()

                auction = Auction()
                auction['id'] = auction_row.css('::attr(href)').get().split('/')[-1]
                auction['currency'] = 1 if 'mithril_shard' in (
                        auction_row.css('.shop-search-row>div:nth-of-type(4)>img::attr(src)').get() or
                        auction_row.css('.shop-search-row>div:nth-of-type(5)>img::attr(src)').get()) else 2
                auction['bid'] = auction_row.css('.shop-search-row>div:nth-of-type(4)::text').extract()[
                    -1].strip().replace(',', '')
                auction['buyout'] = auction_row.css('.shop-search-row>div:nth-of-type(5)::text').extract()[
                    -1].strip().replace(',', '')
                auction['item_id'] = item['id']
                auction['action_property'] = []

                yield scrapy.Request(
                    f'https://www.roshpit.ca/player_items/get_item_tooltip?item_id='
                    f'{auction_row.css(".tooltip-gear-stash::attr(data-item-id)").get()}',
                    self.parse_auction_property, meta={'auction': auction, 'item': item})

        self.crawled_auction_id = auction_id

    def parse_auction_property(self, response):
        item_type = ItemType()
        item_type['id'] = response.css('#tooltip_quality_right::text').get().strip().replace(' ', '')
        item_type['name'] = response.css('#tooltip_quality_right::text').get().strip().capitalize()
        yield {'item_type': item_type}

        item = response.meta['item']
        item['type'] = item_type['id']
        item['rarity'] = response.css('#tooltip_quality_left::text').get().strip()
        yield {'item': item}

        auction = response.meta['auction']
        auction['item'] = item
        auction['level'] = response.css('#tooltip_requirements_left::text').get().strip().split(': ')[-1]

        for i, property_row in enumerate(response.css('#properties_container>.property_container'), start=1):
            property = Property()
            property['name'] = property_row.css(f'#properties_name{i}::text').get().strip()
            property['type'] = i
            property['id'] = item['id'] + str(property['type']) + property['name'].replace(' ', '')
            property['is_ability'] = 1 if '★' in property_row.css(f'#properties_value{i}::text').get().strip() else 0
            property['item_id'] = item['id']
            yield {'property': property}

            action_property = AuctionProperty()
            action_property['roll'] = property_row.css(f'#properties_value{i}::text').get().strip()
            action_property['property_id'] = property['id']
            action_property['property'] = property

            auction['action_property'].append(action_property)

        yield {'auction': auction}

    def closed(self, reason):
        self.collect_auction_info_service.set_crawled_auction_id(self.crawled_auction_id)
