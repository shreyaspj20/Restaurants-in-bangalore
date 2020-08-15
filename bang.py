import scrapy

from ..items import HotelItem


class BangSpider(scrapy.Spider):
    name = 'bang'
    page_num=2
    start_urls = ['https://www.zomato.com/bangalore/best-restaurants?page=1']

    def parse(self, response):
        items = HotelItem()
        all_hotels=response.css('.content')
        for h in all_hotels:
                    names =(h.css('.fontsize0::text').extract())
                    name=[n.rstrip() for n in names]
                    prices = h.css('.res-cost .pl0').css('::text').extract()
                    price1=[p.replace('₹','') for p in prices]
                    price=[a.replace(',','') for a in price1]
                    cuisine=(h.css('.nowrap a::text').extract())
                    locations=h.css('.ln22').css('::text').extract()
                    location=[l.replace(',','|') for l in locations]
                    ratings=h.css('.rating-value::text').extract()
                    tags = h.css('.fontsize6::text').extract()
                    items['name']=name
                    items['price']=price
                    items['cuisine']=cuisine
                    items['location']=location
                    items['ratings']=ratings
                    items['tags']=tags
                    yield items

        next_page='https://www.zomato.com/bangalore/best-restaurants?page='+str(BangSpider.page_num)+''
        if(BangSpider.page_num <=1003):
            BangSpider.page_num += 1
            yield response.follow(next_page,callback=self.parse)