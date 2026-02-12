# scrapyhub/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# 项目基本配置
BOT_NAME = 'Mozilla' # 通用的爬虫名称
SPIDER_MODULES = ['scrapyhub.spiders']
NEWSPIDER_MODULE = 'scrapyhub.spiders'

# 并发和延迟
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 5
ROBOTSTXT_OBEY = True # 遵守robots.txt规则

# 用户代理列表
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
]

# 默认请求头
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# 中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapyhub.middlewares.RandomUserAgentMiddleware': 543,
}

# Pipeline
ITEM_PIPELINES = {
    'scrapyhub.pipelines.RankingPipeline': 300,
}

# 数据库配置
MYSQL_SETTINGS = {
    'HOST': os.getenv('MYSQL_HOST', 'localhost'),
    'PORT': int(os.getenv('MYSQL_PORT', 3306)),
    'USER': os.getenv('MYSQL_USER', 'root'),
    'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
    'DATABASE': os.getenv('MYSQL_DATABASE', 'hot_list'),
    'CHARSET': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
}

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_ENCODING = 'utf-8'

# Scrapy 2.14+ 配置
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

# Cookie设置
COOKIES_ENABLED = True

# 自动限速(可选)
AUTOTHROTTLE_ENABLED = False
# AUTOTHROTTLE_START_DELAY = 1
# AUTOTHROTTLE_MAX_DELAY = 10
# AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0