# scrapyhub/items.py - 统一Item定义
import scrapy

class RankingItem(scrapy.Item):
    """统一的排行榜Item"""
    title = scrapy.Field()      # 标题
    url = scrapy.Field()        # URL链接
    hot_rank = scrapy.Field()   # 排名
    source = scrapy.Field()     # 来源(爬虫名称)