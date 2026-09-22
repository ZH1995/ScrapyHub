import pytest  # pyright: ignore[reportMissingImports]

from scrapyhub.items import ItemValidationError, validate_ranking_item


def test_valid_item_is_normalized():
    item = validate_ranking_item(
        {"title": "  Topic  ", "url": " https://example.com/topic ", "hot_rank": "3", "source": "demo"}
    )

    assert item == {
        "title": "Topic",
        "url": "https://example.com/topic",
        "hot_rank": 3,
        "source": "demo",
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("title", ""),
        ("url", ""),
        ("source", ""),
        ("hot_rank", 0),
        ("hot_rank", "not-a-number"),
    ],
)
def test_invalid_item_is_rejected(field, value):
    item = {"title": "Topic", "url": "https://example.com", "hot_rank": 1, "source": "demo"}
    item[field] = value

    with pytest.raises(ItemValidationError):
        validate_ranking_item(item)
