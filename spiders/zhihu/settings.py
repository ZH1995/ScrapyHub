ITEM_PIPELINES = {
    "spiders.zhihu.pipelines.ZhihuPipeline": 300,
}
HTTPERROR_ALLOWED_CODES = [403,401]

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   'Accept-Language': 'zh-CN,zh;q=0.9',
   'Referer': 'https://www.zhihu.com/',
}