from .base_items import BaseItem
import scrapy

class BaseRankItem(BaseItem):
    """榜单爬虫项基类，子类应继承此类"""
    title = scrapy.Field()
    url = scrapy.Field()
    hot_rank = scrapy.Field()