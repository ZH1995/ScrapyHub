import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from useragentlist import agents

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
    	ua = random.choice(agents)
        request.headers.setdefault('User-Agent', ua)
        request.headers.setdefault('Referer', "https://www.sogou.com/")