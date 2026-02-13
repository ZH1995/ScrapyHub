# scrapyhub/spiders/juejin_spider.py
import scrapy
import json
from ..items import RankingItem


class JuejinSpider(scrapy.Spider):
    """掘金热榜爬虫"""
    name = 'juejin'
    allowed_domains = ['juejin.cn']
    start_urls = ['https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot&spider=0']
    
    custom_settings = {
        'LOG_FILE': 'logs/juejin.log',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://juejin.cn/'
        }
    }

    def parse(self, response):
        """解析掘金热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and len(data['data']) > 0:
                hot_news = data['data']
                rank = 1
                for item in hot_news:
                    if rank > 30:
                        break
                    title = item.get('content', {}).get('title')
                    id = item.get('content', {}).get('content_id')
                    url = f"https://juejin.cn/post/{id}" if id else None

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