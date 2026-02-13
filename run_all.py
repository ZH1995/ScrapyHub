#!/usr/bin/env python
# run_all.py - 批量运行所有爬虫
import sys
import os
import subprocess
from datetime import datetime

SPIDERS = ['weibo', 'baidu', 'douyin', 'wallstreetcn', 'thepaper']

if __name__ == '__main__':
    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"批量爬虫任务开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    success_count = 0
    failed_count = 0
    
    # 获取 Python 解释器路径
    python_path = sys.executable
    # 获取项目根目录
    project_dir = os.path.dirname(os.path.abspath(__file__))    
    
    for spider in SPIDERS:
        print(f"\n{'='*50}")
        print(f"正在运行爬虫: {spider}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        try:
            # 使用 subprocess 在独立进程中运行每个爬虫
            result = subprocess.run(
                [python_path, '-m', 'scrapy', 'crawl', spider],
                cwd=project_dir,
                capture_output=False,  # 让输出直接显示
                text=True
            )
            
            if result.returncode == 0:
                success_count += 1
                print(f"\n✓ 爬虫 {spider} 运行成功")
            else:
                failed_count += 1
                print(f"\n✗ 爬虫 {spider} 运行失败，退出码: {result.returncode}")
                
        except Exception as e:
            failed_count += 1
            print(f"\n✗ 爬虫 {spider} 运行异常: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\n{'='*60}")
    print(f"所有爬虫运行完成！")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {duration}")
    print(f"成功: {success_count} 个，失败: {failed_count} 个")
    print(f"{'='*60}\n")
    
    # 返回适当的退出码
    sys.exit(0 if failed_count == 0 else 1)