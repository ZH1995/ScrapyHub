import datetime
from ..utils.db_utils import DBPoolManager

class BaseMySQLPipeline:
    """MySQL管道基类"""
    
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None
        self.cursor = None
        self.batch_timestamp = None
        self.table_name = ""  # 子类需要设置表名
        self.primary_key = "id"  # 默认主键
    
    @classmethod
    def from_crawler(cls, crawler):
        """从爬虫创建管道"""
        db_settings = crawler.settings.get('MYSQL_SETTINGS', {})
        return cls(db_settings)
    
    def open_spider(self, spider):
        """当爬虫开启时，获取数据库连接"""
        try:
            self.conn = DBPoolManager.get_connection(self.db_settings)
            self.db = self.conn.cursor()
            self.batch_timestamp = datetime.datetime.now()
            spider.logger.info(f"批次开始时间: {self.batch_timestamp}")
            self._create_table()
            spider.logger.info("数据库连接成功")
        except Exception as e:
            spider.logger.error(f"数据库连接失败: {e}")
            raise
    
    def close_spider(self, spider):
        """当爬虫关闭时，关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        spider.logger.info(f"批次结束，所有数据使用相同时间戳: {self.batch_timestamp}")
    
    def _create_table(self):
        """建表语句，子类需要实现"""
        pass
    
    def process_item(self, item, spider):
        """处理爬取到的每个item,子类需要实现"""
        pass