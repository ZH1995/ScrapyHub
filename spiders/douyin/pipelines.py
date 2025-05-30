from common.pipelines.base_rank_pipeline import BaseRankPipeline


class DouyinPipeline(BaseRankPipeline):
    """抖音数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 5  # 来源标识
    
    