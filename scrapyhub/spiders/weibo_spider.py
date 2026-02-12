# scrapyhub/spiders/weibo_spider.py
import scrapy
import json
import urllib.parse
from ..items import RankingItem


class WeiboSpider(scrapy.Spider):
    """微博热搜爬虫"""
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://www.weibo.com/ajax/side/hotSearch']
    
    custom_settings = {
        'LOG_FILE': 'logs/weibo.log',
        'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.weibo.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
    }

    def parse(self, response):
        """解析微博热搜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and 'realtime' in data['data']:
                hot_searches = data['data']['realtime']
                for item in hot_searches:
                    title = item.get('word')
                    hot_rank = item.get('rank')
                    topic_flag = item.get('topic_flag')
                    
                    # 根据是否是话题添加#号
                    query = f'#{title}#' if topic_flag else title
                    encoded_query = urllib.parse.quote(query)
                    url = f"https://s.weibo.com/weibo?q={encoded_query}&t=31"
                    
                    if title and url:
                        yield RankingItem(
                            title=title,
                            url=url,
                            hot_rank=hot_rank + 1,
                            source=self.name
                        )
        except json.JSONDecodeError as e:
            self.logger.error(f"无法解析JSON数据: {e}")