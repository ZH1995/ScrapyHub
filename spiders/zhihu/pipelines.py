from common.pipelines.base_rank_pipeline import BaseRankPipeline

class ZhihuPipeline(BaseRankPipeline):
    """知乎数据管道"""
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 2  # 来源标识