import scrapy
import json
from ..items import ThepaperItem

class ThepaperSpider(scrapy.Spider):
    name = 'thepaper'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'hotNews' in data['data']:
                hot_news = data['data']['hotNews']
                rank = 1
                for item in hot_news:
                    title = item.get('name')
                    cont_id = item.get('contId')
                    url = f"https://www.thepaper.cn/newsDetail_forward_{cont_id}"
                    if title and url:
                        yield ThepaperItem(
                            title=title,
                            url=url,
                            hot_rank=rank
                        )
                        rank = rank + 1
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")