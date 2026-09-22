# ScrapyHub

> 从多个平台采集热榜话题，并存入 MySQL 进行分析。

[英文 README](README.md) · [架构图](docs/architecture.svg) · [运行示例](docs/run-log.svg) · [MIT License](LICENSE)

ScrapyHub 是一个基于 Scrapy 的多站点热榜采集项目，适合开发者、数据分析师、研究人员和学生使用。每个站点由独立 Spider 负责采集，统一 Pipeline 负责格式校验、去重和入库。

## 支持的网站

微博、知乎、百度、36Kr、抖音、华尔街见闻、澎湃新闻、头条、Bilibili、掘金。

## 快速开始

```bash
cp .env.example .env
docker compose up -d
python run_all.py
```

Docker Compose 会启动 MySQL 8.4，并使用 `mysql_data` volume 持久化数据。Python 程序在宿主机运行，通过 `127.0.0.1:3306` 连接数据库。首次运行时 Pipeline 会自动创建 `ranking` 表。

不使用 Docker 时，可以准备 MySQL 后执行：

```bash
python -m venv .venv
python -m pip install -r requirements.txt
cp .env.example .env
python run_all.py
```

调试单个 Spider：

```bash
python run.py weibo
scrapy list
```

## 数据格式

```json
{
  "title": "示例热搜话题",
  "url": "https://example.com/topic",
  "hot_rank": 1,
  "source": "weibo"
}
```

同一来源、同一标题在最近三天内再次出现时会更新原记录，而不是重复插入。

![数据库结果](docs/database-result.svg)

## 文档图片

- [项目整体架构图](docs/architecture.svg)
- [数据库表结构图](docs/database-schema.svg)
- [爬虫运行日志示例](docs/run-log.svg)
- [数据库结果示例](docs/database-result.svg)

## 测试

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

测试覆盖 Spider 解析、数据格式校验、Pipeline 去重，以及模拟数据库连接下的建表和写入逻辑。

## Responsible Use

This project is intended for learning, research and authorized data collection.
Please respect each website's terms of service, robots.txt, rate limits and applicable laws.

请勿用于绕过访问控制、规避反爬机制或采集私人数据。部署定时采集前，请确认自己有权访问、处理和存储相关数据。

## 配置说明

`.env.example` 中提供了完整配置模板。请勿提交 `.env` 或生产环境凭据。项目默认遵守 robots.txt，并设置了较保守的请求延迟。

## 许可证

本项目采用 [MIT License](LICENSE)。
