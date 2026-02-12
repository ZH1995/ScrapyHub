# scrapyhub/spiders/douyin_spider.py
import scrapy
import json
from urllib.parse import quote
from ..items import RankingItem


class DouyinSpider(scrapy.Spider):
    """抖音热榜爬虫"""
    name = 'douyin'
    allowed_domains = ['douyin.com']
    start_urls = ['https://www.douyin.com/aweme/v1/web/hot/search/list']
    
    custom_settings = {
        'LOG_FILE': 'logs/douyin.log',
    }

    def parse(self, response):
        """解析抖音热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and 'word_list' in data['data']:
                word_list = data['data']['word_list']
                for item in word_list:
                    title = item.get('word')
                    hot_rank = item.get('position')
                    sentence_id = item.get('sentence_id')
                    
                    encoded_title = quote(title)
                    url = f"https://www.douyin.com/hot/{sentence_id}/{encoded_title}"
                    
                    if title and url:
                        yield RankingItem(
                            title=title,
                            url=url,
                            hot_rank=hot_rank,
                            source=self.name
                        )
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")