# scrapyhub/middlewares.py
import random


class RandomUserAgentMiddleware:
    """随机用户代理中间件"""
    
    def __init__(self, agents):
        self.agents = agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_LIST'))
    
    def process_request(self, request, spider):
        if self.agents:
            request.headers.setdefault('User-Agent', random.choice(self.agents))