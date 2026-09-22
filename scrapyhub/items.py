# scrapyhub/items.py - unified item definition
import scrapy  # pyright: ignore[reportMissingImports]


class RankingItem(scrapy.Item):
    """A normalized trending-topic record."""

    title = scrapy.Field()
    url = scrapy.Field()
    hot_rank = scrapy.Field()
    source = scrapy.Field()


class ItemValidationError(ValueError):
    """Raised when a spider emits an invalid ranking item."""


def validate_ranking_item(item):
    """Validate and normalize one item before it reaches the database.

    Keeping this function independent from Scrapy makes the data contract easy
    to test and prevents malformed records from reaching MySQL.
    """
    title = str(item.get("title", "")).strip()
    url = str(item.get("url", "")).strip()
    source = str(item.get("source", "")).strip()
    hot_rank = item.get("hot_rank")

    if not title:
        raise ItemValidationError("title is required")
    if len(title) > 255:
        raise ItemValidationError("title must be 255 characters or fewer")
    if not url:
        raise ItemValidationError("url is required")
    if not source:
        raise ItemValidationError("source is required")
    if isinstance(hot_rank, bool):
        raise ItemValidationError("hot_rank must be a positive integer")
    try:
        hot_rank = int(hot_rank)
    except (TypeError, ValueError) as exc:
        raise ItemValidationError("hot_rank must be a positive integer") from exc
    if hot_rank < 1:
        raise ItemValidationError("hot_rank must be a positive integer")

    return {
        "title": title,
        "url": url,
        "hot_rank": hot_rank,
        "source": source,
    }