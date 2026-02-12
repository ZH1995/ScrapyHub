# scrapyhub/middlewares.py
import random
import time


class RandomUserAgentMiddleware:
    """随机用户代理和请求头中间件"""
    
    def __init__(self, agents):
        self.agents = agents
        self.referers = [
            'https://www.google.com/',
            'https://www.baidu.com/',
            'https://www.bing.com/',
            'https://github.com/',
            'https://www.wikipedia.org/',
        ]
        self.accept_encodings = ['gzip, deflate, br', 'gzip, deflate', 'deflate']
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_LIST'))
    
    def process_request(self, request, spider):
        # 随机 User-Agent
        if self.agents:
            request.headers['User-Agent'] = random.choice(self.agents)
        
        # 随机 Referer
        request.headers.setdefault('Referer', random.choice(self.referers))
        
        # 随机 Accept-Encoding
        request.headers.setdefault('Accept-Encoding', random.choice(self.accept_encodings))
        
        # Accept-Language 多样化
        languages = [
            'zh-CN,zh;q=0.9,en;q=0.8',
            'zh-CN,zh;q=0.8,en;q=0.6',
            'en-US,en;q=0.9,zh-CN;q=0.8',
        ]
        request.headers.setdefault('Accept-Language', random.choice(languages))
        
        # 打乱请求头顺序（增强隐蔽性）
        headers = dict(request.headers)
        request.headers.clear()
        for key in random.sample(list(headers.keys()), len(headers)):
            request.headers[key] = headers[key]


class RandomDelayMiddleware:
    """随机延迟中间件"""
    
    def __init__(self, delay_range):
        self.delay_range = delay_range
    
    @classmethod
    def from_crawler(cls, crawler):
        delay = float(crawler.settings.get('DOWNLOAD_DELAY', 5))
        return cls((delay * 0.5, delay * 1.5))  # 在基础延迟的 50%-150% 之间
    
    def process_request(self, request, spider):
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)