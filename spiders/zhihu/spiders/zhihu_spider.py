import scrapy
import json
from ..items import ZhihuItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']  # 修改为实际域名
    start_urls = ['https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true']
    
    def parse(self, response):
        """解析热榜页面"""
        self.logger.error(f"响应内容: {response.text}")
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            if 'data' in data:
                rank = 1
                hot_searches = data['data']
                for item in hot_searches:
                    target = item.get('target')
                    if not target:
                        continue
                    title = target.get('title')
                    url = target.get('url')
                    print(f"标题: {title}, 链接: {url}")
                    if title and url:
                        yield ZhihuItem(
                            title=title,
                            url=url,
                            hot_rank=rank
                        )
                        rank = rank + 1
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")
            