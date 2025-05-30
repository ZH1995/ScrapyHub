from common.pipelines.base_rank_pipeline import BaseRankPipeline


class WallstreetcnPipeline(BaseRankPipeline):
    """华尔街见闻数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 6  # 来源标识
    
    