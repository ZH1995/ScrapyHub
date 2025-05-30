import os

BOT_NAME = "thepaper"

SPIDER_MODULES = ["spiders.thepaper.spiders"]
NEWSPIDER_MODULE = "spiders.thepaper.spiders"


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2
COOKIES_ENABLED = True
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'application/json, text/plain, */*',
   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
   'Connection': 'keep-alive',
   'Referer': 'https://thepaper.cn/'
}
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
]
DOWNLOADER_MIDDLEWARES = {
    "common.middleware.user_agent.RandomUserAgentMiddleware": 543,
}
ITEM_PIPELINES = {
    "spiders.thepaper.pipelines.ThepaperPipeline": 300,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
MYSQL_SETTINGS = {
    'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
    'PORT': int(os.environ.get('MYSQL_PORT', 3306)),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'DATABASE': os.environ.get('MYSQL_DATABASE', ''),
    'CHARSET': os.environ.get('MYSQL_CHARSET', 'utf8mb4'),
}
LOG_LEVEL = 'INFO'  # 日志级别
LOG_FILE = 'logs/thepaper.log'  # 日志文件路径
LOG_ENCODING = 'utf-8'