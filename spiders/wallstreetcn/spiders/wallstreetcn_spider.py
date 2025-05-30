import scrapy
import json
from ..items import WallstreetcnItem

class WallstreetcnSpider(scrapy.Spider):
    name = 'wallstreetcn'
    allowed_domains = ['wallstreetcn.com', 'api-one-wscn.awtmt.com']
    start_urls = ['https://api-one-wscn.awtmt.com/apiv1/content/articles/hot?period=all']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'day_items' in data['data']:
                day_items = data['data']['day_items']
                rank = 1
                for item in day_items:
                    title = item.get('title')
                    url = item.get('uri')
                    if title and url:
                        yield WallstreetcnItem(
                            title=title,
                            url=url,
                            hot_rank=rank
                        )
                        rank = rank + 1
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")