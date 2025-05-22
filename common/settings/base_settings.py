"""
公共配置文件，用于集中管理所有爬虫的设置
"""
import os
import importlib
import sys

# 定义默认的爬虫模块路径
SPIDER_MODULES = [
    "spiders.weibo.spiders",
    "spiders.zhihu.spiders",
    "spiders.baidu.spiders",
    "spiders.36kr.spiders"
]

# 基本配置，所有爬虫通用
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2
COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'application/json, text/plain, */*',
   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
   'Connection': 'keep-alive',
   'Referer': 'https://www.weibo.com/'
}

# 添加随机用户代理列表
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
]

# 中间件目录修正
DOWNLOADER_MIDDLEWARES = {
    "common.middleware.user_agent.RandomUserAgentMiddleware": 543,
}

# 数据库设置
MYSQL_SETTINGS = {
    'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
    'PORT': int(os.environ.get('MYSQL_PORT', 3306)),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'DATABASE': os.environ.get('MYSQL_DATABASE', 'hot_news'),
    'CHARSET': os.environ.get('MYSQL_CHARSET', 'utf8mb4'),
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'

# 自动检测爬虫模块
# 获取命令行参数，识别当前运行的爬虫
spider_name = None
for i, arg in enumerate(sys.argv):
    if arg == 'crawl' and i + 1 < len(sys.argv):
        spider_name = sys.argv[i + 1]
        break

if spider_name:
    # 动态导入爬虫特定的设置
    try:
        # 尝试导入爬虫特定设置
        spider_settings = importlib.import_module(f"spiders.{spider_name}.settings")
        
        # 将爬虫特定设置合并到当前模块
        for key in dir(spider_settings):
            if not key.startswith('__'):
                globals()[key] = getattr(spider_settings, key)
                
        # 设置日志
        LOG_FILE = f'logs/{spider_name}.log'
        
        print(f"已加载 {spider_name} 爬虫的特定设置")
    except (ImportError, ModuleNotFoundError):
        print(f"警告: 未找到 {spider_name} 的特定设置模块")