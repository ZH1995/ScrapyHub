# scrapyhub/middlewares.py
import random
import time


class RandomUserAgentMiddleware:
    """随机用户代理中间件"""
    
    def __init__(self, agents):
        self.agents = agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_LIST'))
    
    def process_request(self, request, spider):
        # 设置随机 User-Agent
        if self.agents:
            request.headers['User-Agent'] = random.choice(self.agents)
        
        # 根据不同爬虫设置对应的 Referer
        referer_map = {
            'weibo': 'https://www.weibo.com/',
            'baidu': 'https://www.baidu.com/',
            'zhihu': 'https://www.zhihu.com/',
            '36kr': 'https://36kr.com/',
            'douyin': 'https://www.douyin.com/',
            'wallstreetcn': 'https://www.wallstreetcn.com/',
            'thepaper': 'https://www.thepaper.cn/',
        }
        
        # 如果没有在 custom_settings 中指定 Referer，使用默认的
        if 'Referer' not in request.headers:
            referer = referer_map.get(spider.name, 'https://www.google.com/')
            request.headers['Referer'] = referer


class RandomDelayMiddleware:
    """随机延迟中间件"""
    
    def __init__(self, delay_range):
        self.delay_range = delay_range
    
    @classmethod
    def from_crawler(cls, crawler):
        delay = float(crawler.settings.get('DOWNLOAD_DELAY', 5))
        return cls((delay * 0.5, delay * 1.5))
    
    def process_request(self, request, spider):
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)