# scrapyhub/spiders/kr36_spider.py
import scrapy
import json
import re
import datetime
from ..items import RankingItem


class Kr36Spider(scrapy.Spider):
    """36氪热榜爬虫"""
    name = '36kr'
    allowed_domains = ['36kr.com']
    
    custom_settings = {
        'LOG_FILE': 'logs/36kr.log',
    }
    
    def __init__(self, *args, **kwargs):
        super(Kr36Spider, self).__init__(*args, **kwargs)
        # 获取当前日期
        self.current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.total_pages = 5  # 36kr通常有5页
        self.logger.info(f"今天日期: {self.current_date}，计划抓取{self.total_pages}页")
    
    def start_requests(self):
        """生成所有页的请求"""
        for page_num in range(1, self.total_pages + 1):
            url = f'https://36kr.com/hot-list/zonghe/{self.current_date}/{page_num}'
            self.logger.info(f"开始抓取页面: {url}")
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                meta={'page': page_num}
            )
    
    def parse(self, response):
        """解析单个页面的内容"""
        page = response.meta.get('page', 1)
        self.logger.info(f"正在解析第{page}页")
        
        # 尝试从页面的JSON数据中获取内容
        json_data = self._extract_json_data(response)
        if json_data:
            yield from self._parse_json_data(json_data, page)
            return
        
        # 如果JSON提取失败，回退到HTML解析
        self.logger.info("未能从JSON获取数据，尝试从HTML解析")
        
        # 36kr榜单结构 - 多种可能的选择器
        selectors = [
            'div.hotlist-item-toptwo, div.hotlist-item-other',
            'div.hotlist-main-item',
            'div.article-wrapper',
            'div.kr-flow-article-item'
        ]
        
        hot_items = []
        for selector in selectors:
            hot_items = response.css(selector)
            if hot_items:
                self.logger.info(f"使用选择器 '{selector}' 找到 {len(hot_items)} 个榜单条目")
                break
        
        if not hot_items:
            self.logger.warning("未找到榜单条目")
            return
        
        # 计算当前页的第一个条目的全局排名
        base_rank = (page - 1) * 20
        
        for local_rank, item in enumerate(hot_items, 1):
            global_rank = base_rank + local_rank
            
            # 提取标题
            title_selectors = [
                'a.article-item-title::text',
                'p.title::text',
                'p.title-wrapper a::text'
            ]
            
            title = None
            for selector in title_selectors:
                title = item.css(selector).get()
                if title:
                    break
            
            # 提取链接
            link_selectors = [
                'a.article-item-title::attr(href)',
                'a.article_link::attr(href)',
                'p.title-wrapper a::attr(href)',
                'a::attr(href)'
            ]
            
            link = None
            for selector in link_selectors:
                link = item.css(selector).get()
                if link:
                    break
            
            # 如果链接是相对路径，转换为绝对URL
            if link and not link.startswith('http'):
                link = f'https://36kr.com{link}'
            
            # 跳过没有标题或链接的条目
            if not title or not link:
                continue
            
            yield RankingItem(
                title=title.strip(),
                url=link,
                hot_rank=global_rank,
                source=self.name
            )
    
    def _extract_json_data(self, response):
        """尝试从window.initialState中提取JSON数据"""
        try:
            script = response.xpath('//script[contains(text(), "window.initialState")]/text()').get()
            if script:
                match = re.search(r'window\.initialState\s*=\s*(\{.*\})', script, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    return data
        except Exception as e:
            self.logger.error(f"从脚本提取JSON数据失败: {e}")
        return None
    
    def _parse_json_data(self, data, page):
        """从JSON数据中提取榜单条目"""
        try:
            if 'hotListDetail' in data and 'articleList' in data['hotListDetail']:
                items = data['hotListDetail']['articleList'].get('itemList', [])
                self.logger.info(f"从JSON数据中找到 {len(items)} 个榜单条目")
                
                for item in items:
                    title = item.get('widgetTitle')
                    route = item.get('route')
                    rank = item.get('rank')
                    
                    if title and route:
                        link = f"https://36kr.com/{route}"
                        
                        yield RankingItem(
                            title=title.strip(),
                            url=link,
                            hot_rank=rank,
                            source=self.name
                        )
        except Exception as e:
            self.logger.error(f"解析JSON数据失败: {e}")