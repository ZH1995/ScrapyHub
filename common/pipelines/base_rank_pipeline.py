from .base_mysql_pipeline import BaseMySQLPipeline
from itemadapter import ItemAdapter
from ..utils.time_utils import get_days_ago

class BaseRankPipeline(BaseMySQLPipeline):
    """榜单管道基类，子类需要继承此类"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.table_name = "ranking"
        self.primary_key = "id"  # 默认主键
        self.source = 0 # 来源标识，子类需要设置
    
    def _create_table(self):
        """创建热榜表"""
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                hot_rank INT,
                source tinyint DEFAULT 0,
                batch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_batch_timestamp (batch_timestamp),
                INDEX idx_title (title)
            )
        '''
        self.db.execute(sql)
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        url = adapter.get('url')
        hot_rank = adapter.get('hot_rank')
        
        # 获取三天前的开始时间
        three_days_ago = get_days_ago()
        
        # 检查是否在三天内已经存在相同标题的记录
        sql = f'''
            SELECT {self.primary_key} FROM {self.table_name} 
            WHERE source = %s AND title = %s AND batch_timestamp >= %s
        '''
        self.db.execute(sql, (self.source, title, three_days_ago))
        result = self.db.fetchone()
        
        if result:
            # 更新已有记录，使用批次时间戳
            sql = f'''
                UPDATE {self.table_name} 
                SET hot_rank = %s, batch_timestamp = %s, created_at = NOW()
                WHERE {self.primary_key} = %s
            '''
            self.db.execute(sql, (hot_rank, self.batch_timestamp, result[0]))
        else:
            # 插入新记录，使用批次时间戳
            sql = f'''
                INSERT INTO {self.table_name} 
                (title, url, hot_rank, batch_timestamp, created_at, source) 
                VALUES (%s, %s, %s, %s, NOW(), %s)
            '''
            self.db.execute(sql, (title, url, hot_rank, self.batch_timestamp, self.source))
        
        return item