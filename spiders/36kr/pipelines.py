from common.pipelines.base_rank_pipeline import BaseRankPipeline


class Kr36Pipeline(BaseRankPipeline):
    """36氪数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 4  # 来源标识
    
    