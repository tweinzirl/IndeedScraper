# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class indeedItem(Item):
    # define the fields for your item here like:
    title			= Field()
    url 			= Field()
    company  			= Field()
    location			= Field()
