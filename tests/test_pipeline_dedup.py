from types import SimpleNamespace

from scrapyhub.pipelines import RankingPipeline


class FakeCursor:
    def __init__(self, existing=None):
        self.existing = existing
        self.queries = []

    def execute(self, sql, params=None):
        self.queries.append((sql, params))

    def fetchone(self):
        return self.existing


def spider():
    return SimpleNamespace(name="weibo", logger=SimpleNamespace(debug=lambda *_: None))


def test_existing_record_is_updated_instead_of_inserted():
    pipeline = RankingPipeline({})
    pipeline.cursor = FakeCursor(existing=(42,))

    item = {"title": "Topic", "url": "https://example.com", "hot_rank": 2, "source": "weibo"}
    result = pipeline.process_item(item, spider())

    assert result["hot_rank"] == 2
    assert len(pipeline.cursor.queries) == 2
    assert pipeline.cursor.queries[1][0].lstrip().startswith("UPDATE ranking")
    assert pipeline.cursor.queries[1][1][0] == 2


def test_missing_record_is_inserted():
    pipeline = RankingPipeline({})
    pipeline.cursor = FakeCursor(existing=None)

    pipeline.process_item(
        {"title": "New topic", "url": "https://example.com/new", "hot_rank": 1, "source": "baidu"},
        spider(),
    )

    assert len(pipeline.cursor.queries) == 2
    assert pipeline.cursor.queries[1][0].lstrip().startswith("INSERT INTO ranking")
    assert pipeline.cursor.queries[1][1] == ("New topic", "https://example.com/new", 1, pipeline.batch_timestamp, 3)
