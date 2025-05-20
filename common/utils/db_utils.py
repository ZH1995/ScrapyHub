import pymysql
from dbutils.pooled_db import PooledDB

# 模块级全局变量
_pool = None

class DBPoolManager:
    """数据库连接池管理器"""
    
    @classmethod
    def get_connection(cls, db_settings):
        """获取数据库连接"""
        global _pool
        if _pool is None:
            _pool = PooledDB(
                creator=pymysql,
                maxconnections=10,  # 最大连接数
                mincached=2,        # 初始化时创建的连接数
                maxcached=5,        # 最多空闲连接数
                blocking=True,      # 连接池满时是否阻塞等待
                host=db_settings['HOST'],
                port=db_settings.get('PORT', 3306),
                user=db_settings['USER'],
                password=db_settings['PASSWORD'],
                database=db_settings['DATABASE'],
                charset=db_settings.get('CHARSET', 'utf8mb4'),
                autocommit=True
            )
        return _pool.connection()