from pathlib import Path
import scrapy
import json
from ..items import DouyinItem
from urllib.parse import quote

class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['douyin.com']
    start_urls = ['https://www.douyin.com/aweme/v1/web/hot/search/list']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            if 'word_list' in data['data']:
                word_list = data['data']['word_list']
                for item in word_list:
                    title = item.get('word')
                    hot_rank = item.get('position')
                    sentence_id = item.get('sentence_id')
                    encoded_title = quote(title)
                    url = f"https://www.douyin.com/hot/{sentence_id}/{encoded_title}"
                    
                    if title and url:
                        yield DouyinItem(
                            title=title,
                            url=url,
                            hot_rank=hot_rank
                        )
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")