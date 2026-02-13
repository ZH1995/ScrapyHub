# scrapyhub/spiders/wallstreetcn_spider.py
import scrapy
import json
from ..items import RankingItem


class WallstreetcnSpider(scrapy.Spider):
    """华尔街见闻热榜爬虫"""
    name = 'wallstreetcn'
    allowed_domains = ['wallstreetcn.com', 'api-one-wscn.awtmt.com']
    start_urls = ['https://api-one-wscn.awtmt.com/apiv1/content/articles/hot?period=all']
    
    custom_settings = {
        'LOG_FILE': 'logs/wallstreetcn.log',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://wallstreetcn.com/'
        }
    }

    def parse(self, response):
        """解析华尔街见闻热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and 'day_items' in data['data']:
                day_items = data['data']['day_items']
                rank = 1
                for item in day_items:
                    # 只取前30条数据
                    if rank > 30:
                        break

                    title = item.get('title')
                    url = item.get('uri')
                    
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