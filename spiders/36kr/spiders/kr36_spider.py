from pathlib import Path
import scrapy
import datetime
from ..items import Kr36Item

class Kr36Spider(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['https://36kr.com/hot-list/zonghe/2025-05-22/2']

    def __init__(self, *args, **kwargs):
        super(Kr36Spider, self).__init__(*args, **kwargs)
        # 获取当前日期，生成日期字符串，格式为'YYYY-MM-DD'
        self.current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.total_pages = 5  # 36kr通常有5页
        self.logger.info(f"今天日期: {self.current_date}，计划抓取{self.total_pages}页")
    
    def start_requests(self):
        """生成所有页的请求"""
        # 生成所有页面的URL
        for page_num in range(1, self.total_pages + 1):
            url = f'https://36kr.com/hot-list/zonghe/{self.current_date}/{page_num}'
            self.logger.info(f"开始抓取页面: {url}")
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                meta={'page': page_num}  # 传递页码信息用于计算全局排名
            )
    
    def parse(self, response):
        """解析单个页面的内容"""
        page = response.meta.get('page', 1)
        self.logger.info(f"正在解析第{page}页")
        
        # 尝试从页面的JSON数据中获取内容 (更可靠的方法)
        json_data = self.extract_json_data(response)
        if json_data:
            return self.parse_json_data(json_data, page)
        
        # 如果JSON提取失败，回退到HTML解析
        self.logger.info("未能从JSON获取数据，尝试从HTML解析")
        
        # 36kr榜单结构分析 - 多种可能的选择器
        selectors = [
            'div.hotlist-item-toptwo, div.hotlist-item-other',  # 主要选择器
            'div.hotlist-main-item',                            # 备选选择器1
            'div.article-wrapper',                              # 备选选择器2
            'div.kr-flow-article-item'                          # 备选选择器3
        ]
        
        hot_items = []
        for selector in selectors:
            hot_items = response.css(selector)
            if hot_items:
                self.logger.info(f"使用选择器 '{selector}' 找到 {len(hot_items)} 个榜单条目")
                break
        
        # 如果还是没有找到，尝试查找窗口状态中的数据
        if not hot_items:
            self.logger.warning("尝试从页面window.initialState中提取数据")
            return self.extract_from_script(response)
        
        # 计算当前页的第一个条目的全局排名
        base_rank = (page - 1) * 20
        
        for local_rank, item in enumerate(hot_items, 1):
            # 计算全局排名
            global_rank = base_rank + local_rank
            
            # 提取标题 - 尝试多种选择器
            title_selectors = [
                'a.article-item-title::text', 
                'p.title::text',
                'a.article-item-title::text', 
                'p.title-wrapper a::text'
            ]
            
            title = None
            for selector in title_selectors:
                title = item.css(selector).get()
                if title:
                    break
                    
            # 如果常规选择器失败，尝试更激进的方法
            if not title:
                title = item.css('*::text').re_first(r'[\w\s\u4e00-\u9fa5]{10,}')
                
            # 提取链接 - 尝试多种选择器
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
                self.logger.warning(f"跳过无标题或链接的条目")
                continue
                
            self.logger.info(f"抓取条目: #{global_rank} - {title}")
            
            yield Kr36Item(
                title=title.strip(),
                url=link,
                hot_rank=global_rank
            )

    def extract_json_data(self, response):
        """尝试从window.initialState中提取JSON数据"""
        try:
            # 提取包含initialState的脚本
            script = response.xpath('//script[contains(text(), "window.initialState")]/text()').get()
            if script:
                import re
                import json
                # 使用正则表达式提取JSON部分
                match = re.search(r'window\.initialState\s*=\s*(\{.*\})', script, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    return data
        except Exception as e:
            self.logger.error(f"从脚本提取JSON数据失败: {e}")
        return None

    def parse_json_data(self, data, page):
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
                        link = f"https://36kr.com/{route.replace('?', '/').replace('=', '/')}"
                        
                        yield Kr36Item(
                            title=title.strip(),
                            url=link,
                            hot_rank=rank
                        )
        except Exception as e:
            self.logger.error(f"解析JSON数据失败: {e}")

    def extract_from_script(self, response):
        """尝试从页面脚本中提取数据"""
        try:
            # 查找包含文章数据的脚本
            script_text = response.xpath('//script[contains(text(), "articleList")]/text()').get()
            if script_text:
                import re
                import json
                # 使用正则表达式提取文章列表
                match = re.search(r'"itemList":\s*(\[.*?\])', script_text, re.DOTALL)
                if match:
                    items_json = match.group(1)
                    items = json.loads(items_json)
                    
                    for item in items:
                        title = item.get('widgetTitle')
                        route = item.get('route')
                        rank = item.get('rank')
                        
                        if title and route:
                            link = f"https://36kr.com/{route.replace('?', '/').replace('=', '/')}"
                            
                            yield Kr36Item(
                                title=title.strip(),
                                url=link,
                                hot_rank=rank
                            )
        except Exception as e:
            self.logger.error(f"从脚本提取数据失败: {e}")