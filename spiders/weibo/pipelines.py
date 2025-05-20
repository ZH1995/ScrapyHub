from common.pipelines.base_rank_pipeline import BaseRankPipeline


class WeiboPipeline(BaseRankPipeline):
    """微博数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 1  # 来源标识
    
    