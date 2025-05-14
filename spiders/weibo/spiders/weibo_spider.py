from pathlib import Path
import scrapy
import urllib.parse
import json

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://www.weibo.com/ajax/side/hotSearch']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })

    def parse(self, response):
        try:
            data = json.loads(response.text)
            print("成功解析JSON数据")
            if 'realtime' in data['data']:
                hot_searches = data['data']['realtime']
                for item in hot_searches:
                    title = item.get('word')
                    hot_rank = item.get('rank')
                    topic_flag = item.get('topic_flag')
                    query = '#' + title + '#' if topic_flag else title
                    encoded_query = urllib.parse.quote(query)
                    url = f"https://s.weibo.com/weibo?q={encoded_query}&t=31"
                    if title and url:
                        yield {
                            'title': title,
                            'url': url,
                            'hot_rank': hot_rank,
                        }
        except json.JSONDecodeError as e:
            print("无法解析JSON数据")
            print(response.text)