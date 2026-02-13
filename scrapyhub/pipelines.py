# scrapyhub/pipelines.py
from datetime import datetime, timedelta

from .utils.db_utils import DBPoolManager


class RankingPipeline:
    """统一的排行榜数据管道"""
    
    SOURCE_MAP = {
        'weibo': 1,
        'zhihu': 2,
        'baidu': 3,
        '36kr': 4,
        'douyin': 5,
        'wallstreetcn': 6,
        'thepaper': 7,
        'zhihu': 8,
        'toutiao': 9
    }
    
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.batch_timestamp = datetime.now()
        self.conn = None
        self.cursor = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MYSQL_SETTINGS'))
    
    def open_spider(self, spider):
        """爬虫开启时初始化"""
        try:
            self.conn = DBPoolManager.get_connection(self.db_settings)
            self.cursor = self.conn.cursor()
            self._ensure_table()
            spider.logger.info(f"数据库连接成功，批次时间: {self.batch_timestamp}")
        except Exception as e:
            spider.logger.error(f"数据库连接失败: {e}")
            raise
    
    def close_spider(self, spider):
        """爬虫关闭时清理"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        spider.logger.info(f"批次结束，时间戳: {self.batch_timestamp}")
    
    def process_item(self, item, spider):
        """处理每个item"""
        source_id = self.SOURCE_MAP.get(item.get('source', spider.name), 0)
        three_days_ago = datetime.now() - timedelta(days=3)
        
        # 打印输出进行调试
        #spider.logger.info(f"Item: {item}")
        #return item

        # 检查是否存在
        check_sql = """
            SELECT id FROM ranking 
            WHERE source = %s AND title = %s AND batch_timestamp >= %s
        """
        self.cursor.execute(check_sql, (source_id, item['title'], three_days_ago))
        result = self.cursor.fetchone()
        
        if result:
            # 更新已有记录
            update_sql = """
                UPDATE ranking 
                SET hot_rank = %s, batch_timestamp = %s, created_at = NOW()
                WHERE id = %s
            """
            self.cursor.execute(update_sql, (item['hot_rank'], self.batch_timestamp, result[0]))
            spider.logger.debug(f"更新记录: {item['title']}")
        else:
            # 插入新记录
            insert_sql = """
                INSERT INTO ranking 
                (title, url, hot_rank, batch_timestamp, created_at, source) 
                VALUES (%s, %s, %s, %s, NOW(), %s)
            """
            self.cursor.execute(insert_sql, (
                item['title'], 
                item.get('url', ''), 
                item['hot_rank'], 
                self.batch_timestamp, 
                source_id
            ))
            spider.logger.debug(f"插入新记录: {item['title']}")
        return item
    
    def _ensure_table(self):
        """确保表存在"""
        create_sql = '''
            CREATE TABLE IF NOT EXISTS ranking (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                url VARCHAR(512) NOT NULL,
                hot_rank INT,
                source TINYINT DEFAULT 0,
                batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_batch_timestamp (batch_timestamp),
                INDEX idx_title (title),
                INDEX idx_source (source)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        '''
        self.cursor.execute(create_sql)