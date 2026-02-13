#!/usr/bin/env python
# run.py - 爬虫运行脚本
import sys
import os
from scrapy.cmdline import execute

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # 如果没有参数，显示帮助
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python run.py <spider_name>")
        print("\n可用的爬虫:")
        print("  weibo        - 微博热搜")
        print("  baidu        - 百度热搜")
        #print("  36kr         - 36氪热榜")
        print("  douyin       - 抖音热榜")
        print("  wallstreetcn - 华尔街见闻")
        print("  thepaper     - 澎湃新闻")
        print("  zhihu        - 知乎")
        print("  toutiao      - 头条热榜")
        print("  bilibili     - Bilibili热榜")
        print("\n示例:")
        print("  python run.py weibo")
        sys.exit(0)
    
    spider_name = sys.argv[1]
    execute(['scrapy', 'crawl', spider_name])