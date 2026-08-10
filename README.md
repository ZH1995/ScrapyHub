

# ScrapyHub

ScrapyHub是一个基于Scrapy 2.14框架的多网站热榜数据采集系统，目前支持微博、百度、抖音、华尔街见闻、澎湃等热搜榜单爬取，通过定时采集存储热榜数据，可用于数据分析和趋势研究。

## 🚀 功能特点

- **统一项目架构**：采用单一Scrapy项目，多Spider设计，便于管理和维护
- **多站点数据采集**：支持微博、百度、抖音、华尔街见闻、澎湃等热榜爬取
- **智能数据去重**：3天内相同条目自动更新而非重复插入
- **连接池管理**：使用DBUtils实现数据库连接池，提升性能
- **环境配置分离**：通过.env文件管理敏感配置，提高安全性
- **统一Pipeline**：所有爬虫共享数据处理逻辑，减少代码重复

## 📋 项目结构

```
ScrapyHub/
├── .env                      # 环境变量配置(不提交到Git)
├── .env.example              # 环境变量配置模板
├── .gitignore                # Git忽略文件配置
├── README.md                 # 项目说明文档
├── requirements.txt          # Python依赖包
├── scrapy.cfg                # Scrapy配置文件
├── run.py                    # 单个爬虫运行脚本
├── run_all.py                # 批量运行所有爬虫
├── logs/                     # 日志目录
│   ├── weibo.log
│   ├── baidu.log
│   ├── douyin.log
│   ├── wallstreetcn.log
│   └── thepaper.log
└── scrapyhub/                # 主项目包
    ├── __init__.py
    ├── settings.py           # 统一配置文件
    ├── items.py              # Item定义
    ├── middlewares.py        # 中间件
    ├── pipelines.py          # 数据管道
    ├── spiders/               # 爬虫目录
    │   ├── __init__.py
    │   ├── weibo_spider.py   # 微博热搜
    │   ├── baidu_spider.py   # 百度热榜
    │   ├── kr36_spider.py    # 36氪热榜
    │   ├── douyin_spider.py  # 抖音热榜
    │   ├── wallstreetcn_spider.py  # 华尔街见闻
    │   └── thepaper_spider.py      # 澎湃新闻
    └── utils/                # 工具函数
        ├── __init__.py
        ├── db_utils.py       # 数据库连接池管理
        └── time_utils.py     # 时间处理工具
```

## 🛠️ 环境配置

### 系统要求

- Python 3.13+
- MySQL 5.7+

### 依赖安装

1. **创建并激活虚拟环境**

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

2. **安装项目依赖**

```bash
pip install -r requirements.txt
```

### 数据库配置

1. **创建数据库**

```sql
CREATE DATABASE hot_list CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. **配置环境变量**

复制 [.env.example](.env.example) 为 `.env` 并填入实际配置：

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置（填入实际的数据库信息）
vim .env
```

`.env` 文件内容示例：

```env
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=hot_list
MYSQL_CHARSET=utf8mb4

# 日志级别
LOG_LEVEL=INFO
```

## 🕸️ 爬虫运行

### 运行单个爬虫

使用 [run.py](run.py) 脚本运行指定爬虫：

```bash
# 赋予脚本可执行权限
chmod +x run.py
chmod +x run_all.py

# 查看帮助
python run.py

# 运行微博热搜爬虫
python run.py weibo

# 运行百度热榜爬虫
python run.py baidu

# 运行抖音热榜爬虫
python run.py douyin

# 运行华尔街见闻爬虫
python run.py wallstreetcn

# 运行澎湃新闻爬虫
python run.py thepaper
```

### 批量运行所有爬虫

使用 [run_all.py](run_all.py) 一次性运行所有爬虫：

```bash
python run_all.py
```

### 使用Scrapy命令

也可以直接使用Scrapy命令行：

```bash
# 列出所有爬虫
scrapy list

# 运行指定爬虫
scrapy crawl weibo
```

## ⏰ 定时任务配置

### Linux/macOS (Crontab)

```bash
# 编辑crontab
crontab -e

# 每10分钟运行一次微博爬虫
*/10 * * * * cd /opt/ScrapyHub && /opt/ScrapyHub/.venv/bin/python /opt/ScrapyHub/run.py weibo >> logs/weibo.log 2>&1

# 每小时运行一次所有爬虫
0 * * * * cd /opt/ScrapyHub && /opt/ScrapyHub/.venv/bin/python /opt/ScrapyHub/run_all.py >> /opt/ScrapyHub/logs/run_all.log 2>&1

# 重启cron服务
sudo service cron restart
```

### 日志轮转配置

防止日志文件过大：

```bash
# 安装logrotate
sudo apt install logrotate -y

# 创建配置文件
sudo vim /etc/logrotate.d/scrapyhub
```

配置内容：

```
/path/to/ScrapyHub/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 user user
}
```

## 📊 数据结构

数据库表 `ranking` 结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 自增主键 |
| title | VARCHAR(255) | 热搜标题 |
| url | VARCHAR(512) | 热搜链接 |
| hot_rank | INT | 排名 |
| source | TINYINT | 来源（1-微博，2-知乎，3-百度，4-36氪，5-抖音，6-华尔街见闻，7-澎湃） |
| batch_timestamp | TIMESTAMP | 批次时间戳 |
| created_at | TIMESTAMP | 记录创建时间 |

索引：
- `idx_batch_timestamp`: 批次时间索引
- `idx_title`: 标题索引
- `idx_source`: 来源索引

## 🔧 技术架构

### 核心组件

1. **Items** ([scrapyhub/items.py](scrapyhub/items.py))
   - `RankingItem`: 统一的排行榜数据项

2. **Pipelines** ([scrapyhub/pipelines.py](scrapyhub/pipelines.py))
   - `RankingPipeline`: 统一的数据处理管道，支持去重和批次管理

3. **Middlewares** ([scrapyhub/middlewares.py](scrapyhub/middlewares.py))
   - `RandomUserAgentMiddleware`: 随机User-Agent中间件

4. **Utils** ([scrapyhub/utils/](scrapyhub/utils/))
   - [`db_utils.py`](scrapyhub/utils/db_utils.py): 数据库连接池管理
   - [`time_utils.py`](scrapyhub/utils/time_utils.py): 时间处理工具

### 设计特点

- **单一职责**：每个Spider只负责数据采集，数据处理统一交给Pipeline
- **配置分离**：敏感配置通过环境变量管理
- **连接池**：使用DBUtils连接池，提升数据库操作性能
- **批次管理**：每次运行使用统一的batch_timestamp标识批次
- **自动去重**：3天内相同来源+标题的数据自动更新而非重复插入

## 🐛 常见问题

### 1. 数据库连接失败

**问题**：运行爬虫时报数据库连接错误

**解决**：
- 检查 [.env](.env) 中的数据库配置是否正确
- 确认MySQL服务正在运行
- 确认数据库已创建且用户有权限

### 2. 爬虫无法获取数据

**问题**：爬虫运行但没有数据入库

**解决**：
- 目标网站可能更新了API或反爬策略
- 查看对应的日志文件（如 `logs/weibo.log`）
- 检查网络连接是否正常
- 考虑增加下载延迟 ([scrapyhub/settings.py](scrapyhub/settings.py) 中的 `DOWNLOAD_DELAY`)

### 3. 日志文件过大

**问题**：logs目录占用空间过大

**解决**：
- 配置logrotate进行日志轮转
- truncate -s 0 /path/to/your.log 将文件截断为0字节

### 4. 36氪爬虫获取不到数据

**问题**：36氪榜单页面结构变化

**解决**：
- 36氪的选择器可能需要更新
- 查看 [scrapyhub/spiders/kr36_spider.py](scrapyhub/spiders/kr36_spider.py) 中的选择器配置
- 尝试访问目标URL检查页面结构

## 📝 开发指南

### 添加新爬虫

1. **创建Spider文件**

```
# scrapyhub/spider/example_spider.py
import scrapy
from ..items import RankingItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/hot']
    
    custom_settings = {
        'LOG_FILE': 'logs/example.log',
    }
    
    def parse(self, response):
        # 解析逻辑
        for item in response.css('.hot-item'):
            yield RankingItem(
                title=item.css('.title::text').get(),
                url=item.css('a::attr(href)').get(),
                hot_rank=item.css('.rank::text').get(),
                source=self.name
            )
```
