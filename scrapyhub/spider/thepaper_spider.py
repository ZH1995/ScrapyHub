# scrapyhub/spiders/thepaper_spider.py
import scrapy
import json
from ..items import RankingItem


class ThepaperSpider(scrapy.Spider):
    """澎湃新闻热榜爬虫"""
    name = 'thepaper'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar']
    
    custom_settings = {
        'LOG_FILE': 'logs/thepaper.log',
    }

    def parse(self, response):
        """解析澎湃新闻热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and 'hotNews' in data['data']:
                hot_news = data['data']['hotNews']
                rank = 1
                for item in hot_news:
                    title = item.get('name')
                    cont_id = item.get('contId')
                    url = f"https://www.thepaper.cn/newsDetail_forward_{cont_id}"
                    
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