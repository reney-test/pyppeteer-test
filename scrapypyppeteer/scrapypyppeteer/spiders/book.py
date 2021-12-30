import logging
import re
from scrapy import Request, Spider
from scrapypyppeteer.items import BookItem


class BookSpider(Spider):
    name = 'book'
    allowed_domains = ['spa5.scrape.center']
    base_urls = 'http://spa5.scrape.center'

    def start_requests(self):
        start_url = f'{self.base_urls}/page/1'
        yield Request(start_url, callback=self.parse_index)

    def parse_index(self, response):
        items = response.css('.item')
        for item in items:
            href = item.css('.top a::attr(href)').get()
            detail_url = response.urljoin(href)
            #叶的优先级高于枝干，保证新枝干开始时，旧的枝叶已处理完
            yield Request(detail_url, callback=self.parse_detail, priority=2)

        match = re.search(r'page/(\d+)', response.url)
        if not match: return
        page = int(match.group(1)) + 1
        next_url = f'{self.base_urls}/page/{page}'
        yield Request(next_url, callback=self.parse_index)

    def parse_detail(self, response):
        name = response.css('.name::text').get()
        tags = response.css('.tags button span::text').getall()
        score = response.css('.score::text').get()
        price = response.css('.price span::text').get()
        cover = response.css('.cover::attr(src)').get()
        tags = [tag.strip() for tag in tags] if tags else []
        score = score.strip() if score else None
        item = BookItem(name=name, tags=tags, score=score, price=price, cover=cover)
        yield item