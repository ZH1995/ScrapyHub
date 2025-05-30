from common.pipelines.base_rank_pipeline import BaseRankPipeline


class ThepaperPipeline(BaseRankPipeline):
    """滂湃数据管道"""
    
    def __init__(self, db_settings):
        super().__init__(db_settings)
        self.source = 7  # 来源标识
    
    