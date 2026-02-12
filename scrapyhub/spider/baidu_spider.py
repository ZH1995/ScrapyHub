# scrapyhub/spiders/baidu_spider.py
import scrapy
from ..items import RankingItem


class BaiduSpider(scrapy.Spider):
    """百度热搜爬虫"""
    name = 'baidu'
    allowed_domains = ['top.baidu.com']
    start_urls = ['https://top.baidu.com/board?tab=realtime']
    
    custom_settings = {
        'LOG_FILE': 'logs/baidu.log',
    }

    def parse(self, response):
        """解析百度热搜"""
        # 使用CSS选择器提取榜单项
        hot_items = response.css('div.category-wrap_iQLoo.horizontal_1eKyQ')
        
        for rank, item in enumerate(hot_items, 1):
            # 提取标题和链接
            title_element = item.css('div.c-single-text-ellipsis::text').get()
            link = item.css('a.title_dIF3B::attr(href)').get()
            
            # 跳过没有标题的项目
            if not title_element or not link:
                continue
            
            title = title_element.strip()
            # 修正链接中的HTML实体
            link = link.replace('&amp;', '&') if link else ''
            
            yield RankingItem(
                title=title,
                url=link,
                hot_rank=rank,
                source=self.name
            )