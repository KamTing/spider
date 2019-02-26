# -*- coding: utf-8 -*-
import scrapy


class TemperatureSpiderSpider(scrapy.Spider):
    name = 'temperature_spider'

    # http: // www.it1352.com / 697592.html
    # allowed_domains = ['tianqi.com']
    # start_urls = ['http://lishi.tianqi.com/guangzhou/index.html']

    allowed_domains = ['it1352.com']
    start_urls = ['http://www.it1352.com/697592.html']

    def parse(self, response):

        print(response.text)
        url_list = response.xpath('//div[@id="tool_site"]/div[2]/ul/li/a/@href').extract()

        print(url_list)
        for url in url_list:
            print(url)

