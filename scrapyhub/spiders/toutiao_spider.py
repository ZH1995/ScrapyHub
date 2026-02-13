# scrapyhub/spiders/toutiao_spider.py
import scrapy
import json
from ..items import RankingItem


class ToutiaoSpider(scrapy.Spider):
    """头条热榜爬虫"""
    name = 'toutiao'
    allowed_domains = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc']
    
    custom_settings = {
        'LOG_FILE': 'logs/toutiao.log',
        #'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.toutiao.com/'
        }
    }

    def parse(self, response):
        """解析头条热榜"""
        try:
            data = json.loads(response.text)
            self.logger.info("成功解析JSON数据")
            
            if 'data' in data and len(data['data']) > 0:
                hot_news = data['data']
                rank = 1
                for item in hot_news:
                    # 只取前30条数据
                    if rank > 30:
                        break

                    title = item.get('Title')
                    cluster_id = item.get('ClusterId')
                    url = f"https://www.toutiao.com/trending/{cluster_id}"

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