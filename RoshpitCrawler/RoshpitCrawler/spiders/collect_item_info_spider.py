from urllib import parse

import scrapy

from ..items import ItemType, Item, Property


class CollectItemInfoSpider(scrapy.Spider):
    name = 'collect_item_info'
    custom_settings = {
        'ITEM_PIPELINES': {
            'RoshpitCrawler.pipelines.OrganiseItemDataPipeline': 100,
            'RoshpitCrawler.pipelines.StoreItemDataPipeline': 200,
            'RoshpitCrawler.pipelines.StoreItemImgPipeline': 300
        },
        'IS_NEW_DB': True
    }

    def start_requests(self):
        urls = [
            'https://www.roshpit.ca/items'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_item_type)

    def parse_item_type(self, response):
        for item_type_row in response.css('.item-filter-buttons>a.button-link:not([href*="arcana"])'):
            item_type = ItemType()
            item_type['id'] = item_type_row.css("div::attr(data-slot)").get().replace(' ', '')
            item_type['name'] = item_type_row.css("div::attr(data-slot)").get().capitalize()
            yield {'item_type': item_type}
            yield scrapy.Request(f'https://www.roshpit.ca{item_type_row.css("a::attr(href)").get()}', self.parse_item,
                                 meta={'item_type_id': item_type['id']})

    def parse_item(self, response):
        item_type_id = response.meta['item_type_id']
        for item_row in response.css('tr.item-row'):
            item = Item()
            item['id'] = item_row.css('td:nth-of-type(2)::text').get().replace(' ', '')
            item['name'] = item_row.css('td:nth-of-type(2)::text').get()
            item['img_url'] = item_row.css('td>img::attr(src)').get()
            item['type'] = item_type_id
            item['rarity'] = item_row.css('td:nth-of-type(3)>span::text').get()
            yield {'item': item}
            yield scrapy.Request(f'https://www.roshpit.ca/items/{item_row.css("::attr(data-item)").get()}',
                                 self.parse_item_detail, meta={'item': item})

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['code'] = response.css('#main-item-container::attr(data-item-id)').get()
        for i in range(1, 5):
            for property_row in response.css(f'#main-item-container tbody[id="propertyData{i}"]'):
                for property_option_row in property_row.css('select[id^="propertiesList"] option'):
                    property = Property()
                    property['name'] = property_option_row.css('::attr(value)').get()
                    property['type'] = i
                    property['id'] = item['id'] + str(property['type']) + property['name'].replace(' ', '')
                    property['item_id'] = item['id']
                    if property['name']:
                        yield scrapy.Request(
                            f'https://www.roshpit.ca/propertyUpdate'
                            f'?item_id={item["code"]}'
                            f'&count={property["type"]}'
                            f'&name={parse.quote_plus(property["name"])}',
                            self.parse_property_roll, meta={'property': property})

    def parse_property_roll(self, response):
        property = response.meta['property']
        property['range'] = response.css('td:contains(" - ")::text').get()
        property['is_ability'] = 1 if '★' in response.text else 0
        yield {'property': property}
