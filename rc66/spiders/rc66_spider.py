# -*- coding: utf-8 -*-
import scrapy
from rc66.items import Rc66Item


class Rc66Spider(scrapy.Spider):
	 name = 'rc66'
	 allowed_domains = ['66rc.com']
	 start_urls = [
	 	'http://www.66rc.com/jilin/'
	 ]

	 def parse_item(self, response):
	 	sel = scrapy.Selector(response)
	 	li_list = sel.xpath("//table[@class='box'][@width='100%']/tr/td/ul/li")
	 	for li in li_list:
	 		item = Rc66Item()
	 		item['title'] = self.format_title(li.css("a::text")[0].extract().encode('utf-8'))
	 		item['link'] = li.xpath("a/@href")[0].extract()
	 		date = li.css("span::text").extract()
	 		if 0 == len(date):
	 			date = li.css("font::text").extract()
	 		item['date'] = date[0]
	 		yield item

	 def parse(self, response):
	 	sel = scrapy.Selector(response)
	 	op_list = sel.xpath("//table[@class='boxb']/tr/td/div/ul/li/select/option")
	 	for op in op_list:
	 		label_a = op.xpath("@value")[0].extract()
	 		print "asdasdasdasdasda1231111111111111111111"
	 		sub_url = "http://www.66rc.com/jilin/" + label_a
	 		print sub_url
	 		yield scrapy.Request(sub_url, callback=self.parse_item)

	 def format_title(self, title):
	 	title_list = title.split('|')
	 	new_title = title_list[1]
	 	new_title = new_title.strip('')
	 	return new_title

