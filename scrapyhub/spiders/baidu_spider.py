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
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.baidu.com/',
        }
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