# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ScrapypyppeteerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(Item):
    #书名、标签、评分、封面、价格
    name = Field()
    tags = Field()
    score = Field()
    cover = Field()
    price = Field()