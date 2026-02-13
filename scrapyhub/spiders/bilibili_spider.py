# scrapyhub/spiders/bilibili_spider.py
import scrapy
import json
from ..items import RankingItem


class BilibiliSpider(scrapy.Spider):
    """Bilibili热榜爬虫"""
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/web-interface/popular']
    
    custom_settings = {
        'LOG_FILE': 'logs/bilibili.log',
        'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.bilibili.com/'
        }
    }

    def parse(self, response):
        """解析Bilibili热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and 'list' in data['data'] and  len(data['data']['list']) > 0:
                hot_news = data['data']['list']
                rank = 1
                for item in hot_news:
                    if rank > 30:
                        break
                    title = item.get('title')
                    bvid = item.get('bvid')
                    url = f"https://www.bilibili.com/video/{bvid}" if bvid else None

                    if title and url:
                        yield RankingItem(
                            title=title,
                            url=url,
                            hot_rank=rank,
                            source=self.name
                        )
                        rank += 1
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")