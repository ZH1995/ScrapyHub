# ScrapyHub

ScrapyHub是一个基于Scrapy框架的多网站数据采集系统，目前包含微博热搜榜单爬虫，通过定时爬取存储热搜数据，可用于数据分析和趋势研究。

## 🚀 功能特点

- **多站点数据采集**：目前支持微博热搜榜爬取，未来可扩展更多网站
- **自动化定时采集**：每5分钟爬取一次微博热搜榜单
- **数据去重**：在同一小时内对相同热搜条目进行更新而非重复插入
- **结构化数据存储**：将热搜数据存储在MySQL数据库中

## 📋 项目结构

```
ScrapyHub/
├── README.md                 # 项目说明文档
├── requirements.txt          # 项目依赖包
├── scrapy.cfg                # Scrapy配置文件
├── spiders/                  # 爬虫项目目录
    ├── weibo/                # 微博爬虫项目
        ├── __init__.py
        ├── items.py          # 数据项定义
        ├── middlewares.py    # 中间件
        ├── pipelines.py      # 数据管道
        ├── settings.py       # 项目设置
        ├── local_settings.py # 本地配置(不提交到Git)
        └── spiders/          # 爬虫目录
            ├── __init__.py
            └── weibo_spider.py # 微博热搜爬虫
```

## 🛠️ 环境配置

### 依赖安装

1. 创建并激活虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# 在Windows上:
venv\Scripts\activate
# 在macOS/Linux上:
source venv/bin/activate
```

2. 安装项目依赖：

```bash
pip install scrapy pymysql
```

### 数据库配置

1. 创建名为`hot_news`的MySQL数据库
2. 复制`local_settings.py.example`为local_settings.py并配置数据库连接信息：

```python
MYSQL_SETTINGS = {
    'HOST': 'localhost',
    'USER': 'your_username',
    'PASSWORD': 'your_password',
    'DATABASE': 'hot_news'
}
```

## 🕸️ 爬虫运行

### 运行微博热搜爬虫

```bash
# 在项目根目录下执行
scrapy crawl weibo
```

### 定时任务配置

使用crontab（Linux/macOS）或任务计划程序（Windows）设置定时任务：

```bash
# 每5分钟运行一次爬虫 (Linux/macOS crontab示例)
*/5 * * * * cd /path/to/ScrapyHub && /path/to/venv/bin/python -m scrapy crawl weibo
```

## 📊 数据结构

微博热搜数据表结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 自增主键 |
| title | VARCHAR(255) | 热搜标题 |
| url | VARCHAR(255) | 热搜链接 |
| hot_rank | INT | 热搜排名 |
| created_at | TIMESTAMP | 创建时间 |

## 🔧 常见问题

### 无法连接到数据库

检查local_settings.py中的数据库配置是否正确，确保MySQL服务正在运行。

### 爬虫无法获取数据

微博可能更新了API或反爬策略，请检查weibo_spider.py中的请求URL和headers是否需要更新。

## 📝 待办事项

- [ ] 添加更多网站的爬虫
- [ ] 增强数据分析功能
- [ ] 添加Web界面展示热搜趋势
- [ ] 优化数据库结构，支持更复杂的查询

## 📜 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request来改进项目。

---

**注意**：请遵守网站的robots.txt规则和使用条款，合理设置爬取频率，避免对目标网站造成不必要的负担。