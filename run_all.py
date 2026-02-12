#!/usr/bin/env python
# run_all.py - 批量运行所有爬虫
import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SPIDERS = ['weibo', 'baidu', 'douyin', 'wallstreetcn', 'thepaper']

if __name__ == '__main__':
    for spider in SPIDERS:
        print(f"\n{'='*50}")
        print(f"正在运行爬虫: {spider}")
        print(f"{'='*50}\n")
        try:
            execute(['scrapy', 'crawl', spider])
        except SystemExit:
            pass  # Scrapy会调用sys.exit()，我们忽略它继续下一个
        except Exception as e:
            print(f"爬虫 {spider} 运行失败: {e}")
    
    print(f"\n{'='*50}")
    print("所有爬虫运行完成！")
    print(f"{'='*50}\n")