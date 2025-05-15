# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import datetime
from itemadapter import ItemAdapter


class WeiboPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        # 批次时间戳将在每次爬虫启动时创建
        self.batch_timestamp = None

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings.py中获取数据库配置
        db_settings = {
            'mysql': crawler.settings.get('MYSQL_SETTINGS', {})
        }
        return cls(db_settings)

    def open_spider(self, spider):
        # 连接数据库
        self.conn = pymysql.connect(
            host=self.db_settings['mysql'].get('HOST', 'localhost'),
            user=self.db_settings['mysql'].get('USER', 'root'),
            password=self.db_settings['mysql'].get('PASSWORD', ''),
            database=self.db_settings['mysql'].get('DATABASE', 'scrapy_db'),
            charset='utf8mb4'
        )
        
        self.cursor = self.conn.cursor()
        
        # 创建表 (如果不存在)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weibo_hot_search (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                hot_rank INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
        # 为这个批次设置一个统一的时间戳
        self.batch_timestamp = datetime.datetime.now()
        spider.logger.info(f"批次开始时间: {self.batch_timestamp}")

    def close_spider(self, spider):
        self.conn.close()
        spider.logger.info(f"批次结束，所有数据使用相同时间戳: {self.batch_timestamp}")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        url = adapter.get('url')
        hot_rank = adapter.get('hot_rank')
        
        # 获取当前小时的开始时间
        current_hour = self.get_current_hour_start()
        
        # 检查是否在当前小时内已经存在相同标题的记录
        self.cursor.execute(
            '''
            SELECT id FROM weibo_hot_search 
            WHERE title = %s 
            AND created_at >= %s
            ''',
            (title, current_hour)
        )
        
        result = self.cursor.fetchone()
        
        if result:
            # 更新已有记录，使用批次时间戳
            self.cursor.execute(
                '''
                UPDATE weibo_hot_search 
                SET hot_rank = %s, created_at = %s 
                WHERE id = %s
                ''',
                (hot_rank, self.batch_timestamp, result[0])
            )
        else:
            # 插入新记录，使用批次时间戳
            self.cursor.execute(
                '''
                INSERT INTO weibo_hot_search (title, url, hot_rank, created_at) 
                VALUES (%s, %s, %s, %s)
                ''',
                (title, url, hot_rank, self.batch_timestamp)
            )
        
        self.conn.commit()
        return item

    def get_current_hour_start(self):
        """获取当前小时的开始时间"""
        now = datetime.datetime.now()
        hour_start = now.replace(minute=0, second=0, microsecond=0)
        return hour_start

