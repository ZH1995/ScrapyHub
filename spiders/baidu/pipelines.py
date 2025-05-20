from common.pipelines.base_rank_pipeline import BaseRankPipeline


class BaiduPipeline(BaseRankPipeline):
    """百度数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 3  # 来源标识
    
    