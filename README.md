# ScrapyHub

ScrapyHub是一个基于Scrapy框架的多网站数据采集系统，目前包含微博、百度、36氪、知乎热搜榜单爬虫，通过定时爬取存储热搜数据，可用于数据分析和趋势研究。

## 🚀 功能特点

- **多站点数据采集**：目前支持微博、百度、36氪热榜爬取，未来可扩展更多网站
- **自动化定时采集**：每5分钟爬取一次微博热搜榜单
- **数据去重**：在三天内对相同热搜条目进行更新而非重复插入
- **结构化数据存储**：将热搜数据存储在MySQL数据库中

## 📋 项目结构

```
ScrapyHub/
├── README.md                 # 项目说明文档
├── requirements.txt          # 项目依赖包
├── scrapy.cfg                # Scrapy配置文件
├── env.sh                    # 环境变量配置脚本
├── run.sh                    # 爬虫运行脚本
├── common/                   # 通用组件目录
│   ├── __init__.py
│   ├── middleware/           # 中间件目录
│   │   ├── __init__.py
│   │   └── user_agent.py     # 随机User-Agent中间件
│   ├── pipelines/            # 公共数据管道
│   │   ├── __init__.py
│   │   ├── base_mysql_pipeline.py  # MySQL基础管道
│   │   └── base_rank_pipeline.py   # 榜单数据管道基类
│   ├── settings/             # 公共设置
│   │   ├── __init__.py
│   │   └── base_settings.py  # 基础设置
│   └── utils/                # 工具函数
│       ├── __init__.py
│       ├── db_utils.py       # 数据库工具
│       └── time_utils.py     # 时间处理工具
├── logs/                     # 日志目录
│   ├── weibo.log
│   └── baidu.log
├── spiders/                  # 爬虫项目目录
│   ├── __init__.py
│   ├── weibo/                # 微博爬虫项目
│   │   ├── __init__.py
│   │   ├── items.py          # 数据项定义
│   │   ├── pipelines.py      # 数据管道
│   │   ├── settings.py       # 项目设置
│   │   ├── local_settings.py # 本地配置(不提交到Git)
│   │   └── spiders/          # 爬虫目录
│   │       ├── __init__.py
│   │       └── weibo_spider.py # 微博热搜爬虫
│   └── baidu/                # 百度爬虫项目
│       ├── __init__.py
│       ├── items.py          # 数据项定义
│       ├── pipelines.py      # 数据管道
│       ├── settings.py       # 项目设置
│       └── spiders/          # 爬虫目录
│           ├── __init__.py
│           └── baidu_spider.py # 百度热榜爬虫
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
pip install -r requirements.txt
```

### 数据库配置

1. 创建名为`hot_list`的MySQL数据库
2. 使用环境变量配置数据库
```bash
# 编辑 env_example.sh 文件
export MYSQL_HOST=your_host
export MYSQL_PORT=your_port
export MYSQL_USER=your_user
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=ranking
export MYSQL_CHARSET=utf8mb4

# 重命名为env.sh
mv env_example.sh env.sh

# 加载环境变量
source env.sh
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
| source | TINYINT | 来源表示（1-微博，2-知乎，3-百度） |
| batch_timestamp | TIMESTAMP | 爬取批次时间 |
| created_at | TIMESTAMP | 记录创建时间 |

## 🔧 常见问题

### 无法连接到数据库

检查env.sh中的数据库配置是否正确，确保MySQL服务正在运行。

### 爬虫无法获取数据

微博可能更新了API或反爬策略，请检查weibo_spider.py中的请求URL和headers是否需要更新。

## 📝 待办事项

- [x] 添加知乎的爬虫
- [x] 添加百度的爬虫
- [x] 添加36氪的爬虫
- [ ] 解决知乎爬虫身份校验问题
- [ ] 增强数据分析功能
- [x] 优化数据库结构，支持更复杂的查询

## 📜 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request来改进项目。

## ⚠️ 免责声明

本项目仅供学习和研究使用，不得用于任何商业用途。

使用本项目抓取的数据，请遵守相关网站的使用条款和robots.txt规则。

请合理设置爬虫的抓取频率和并发数，避免对目标网站造成不必要的负担。

抓取的数据仅供个人研究、学习使用，请勿用于违反相关法律法规的活动。

本项目开发者不对使用者因使用本项目而产生的任何法律责任负责。

如果您的行为因使用本项目而导致任何纠纷，责任由使用者自行承担。

如相关网站或平台明确声明禁止爬虫访问，请立即停止使用本项目访问该网站。

使用本项目即表示您已阅读并同意上述免责声明。如不同意，请立即停止使用本项目。