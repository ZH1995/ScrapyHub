from pathlib import Path
import scrapy
from ..items import BaiduItem

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['top.baidu.com']
    start_urls = ['https://top.baidu.com/board?tab=realtime']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
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
            
            yield BaiduItem(
                title=title,
                url=link,
                hot_rank=rank
            )