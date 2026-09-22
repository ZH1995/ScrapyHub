import json

from scrapy.http import HtmlResponse  # pyright: ignore[reportMissingImports]

from scrapyhub.spiders.baidu_spider import BaiduSpider
from scrapyhub.spiders.weibo_spider import WeiboSpider


def test_baidu_spider_parses_ranked_html():
    body = b'''
    <div class="category-wrap_iQLoo horizontal_1eKyQ">
      <div class="c-single-text-ellipsis">First topic</div>
      <a class="title_dIF3B" href="https://example.com/?a=1&amp;b=2">link</a>
    </div>
    <div class="category-wrap_iQLoo horizontal_1eKyQ">
      <div class="c-single-text-ellipsis">Second topic</div>
      <a class="title_dIF3B" href="https://example.com/second">link</a>
    </div>
    '''
    response = HtmlResponse(url="https://top.baidu.com/board?tab=realtime", body=body, encoding="utf-8")

    items = list(BaiduSpider().parse(response))

    assert [(item["title"], item["hot_rank"]) for item in items] == [
        ("First topic", 1),
        ("Second topic", 2),
    ]
    assert items[0]["url"] == "https://example.com/?a=1&b=2"


def test_weibo_spider_parses_json_and_builds_search_url():
    body = json.dumps(
        {"data": {"realtime": [{"word": "A topic", "rank": 0, "topic_flag": 1}]}}
    ).encode()
    response = HtmlResponse(url="https://www.weibo.com/ajax/side/hotSearch", body=body, encoding="utf-8")

    items = list(WeiboSpider().parse(response))

    assert items[0]["title"] == "A topic"
    assert items[0]["hot_rank"] == 1
    assert "q=%23A%20topic%23" in items[0]["url"]
