# scrapyhub/spiders/zhihu_spider.py
import scrapy
import json
from ..items import RankingItem


class ZhihuSpider(scrapy.Spider):
    """知乎热榜爬虫"""
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=20&desktop=true']
    
    custom_settings = {
        'LOG_FILE': 'logs/zhihu.log',
        'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.zhihu.com/'
        }
    }

    def parse(self, response):
        """解析知乎热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and len(data['data']) > 0:
                hot_news = data['data']
                rank = 1
                for item in hot_news:
                    title = item.get('target', {}).get('title_area', {}).get('text')
                    url = item.get('target', {}).get('link', {}).get('url')

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