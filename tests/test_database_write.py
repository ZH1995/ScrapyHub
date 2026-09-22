from types import SimpleNamespace

from scrapyhub.pipelines import RankingPipeline


class FakeCursor:
    def __init__(self):
        self.queries = []

    def execute(self, sql, params=None):
        self.queries.append((sql, params))

    def fetchone(self):
        return None

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()

    def cursor(self):
        return self.cursor_instance

    def close(self):
        pass


def test_open_spider_creates_table_and_processes_item(monkeypatch):
    connection = FakeConnection()
    monkeypatch.setattr(
        "scrapyhub.pipelines.DBPoolManager.get_connection",
        lambda settings: connection,
    )
    pipeline = RankingPipeline({"DATABASE": "test"})
    spider = SimpleNamespace(name="baidu", logger=SimpleNamespace(info=lambda *_: None, debug=lambda *_: None))

    pipeline.open_spider(spider)
    pipeline.process_item(
        {"title": "Database topic", "url": "https://example.com/db", "hot_rank": 1, "source": "baidu"},
        spider,
    )

    assert "CREATE TABLE IF NOT EXISTS ranking" in connection.cursor_instance.queries[0][0]
    assert any("INSERT INTO ranking" in query for query, _ in connection.cursor_instance.queries)
