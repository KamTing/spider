# -*- coding: utf-8 -*-
import scrapy
from weathersplier.items import WeathersplierItem


class WeatherSpiderSpider(scrapy.Spider):

    name = 'weather_spider'
    allowed_domains = ['aqistudy.cn']  # 爬取的域名，不会超出这个顶级域名
    base_url = "https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%B9%BF%E5%B7%9E"
    # base_url = "https://www.aqistudy.cn/historydata/daydata.php?city=%E5%B9%BF%E5%B7%9E&month=2014-01"
    # daydata.php?city = 广州 & month = 2013 - 12

    # base_url = "https://www.aqistudy.cn/historydata/daydata.php?city=%E5%B9%BF%E5%B7%9E&month=2014-01"
    # base_url = "https://www.aqistudy.cn/historydata/daydata.php?city=广州&month=2014-01"
    # "https://www.aqistudy.cn/historydata/monthdata.php?city=广州"
    start_urls = [base_url]

    # def parse(self, response):
    #     print('爬取城市信息....')
    #     url_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/@href").extract()  # 全部链接
    #     city_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/text()").extract()  # 城市名称
    #     for url, city in zip(url_list, city_list):
    #
    #         # 目前只获取广州的数据
    #         if(city == "广州"):
    #             print("爬取到{}城市".format(city))
    #             url = self.base_url + "%E5%B9%BF%E5%B7%9E"
    #             print("url-{}".format(url))
    #             yield scrapy.Request(url=url, callback=self.parse_month, meta={'city': city})

    def parse(self, response):
        # print(response.text)
        # https: // www.aqistudy.cn / historydata / monthdata.php?city = 广州

        # print('爬取{}月份...'.format(response.meta['city']))
        # url_list = response.xpath('//tbody/tr/td/a/@href').extract()

        url_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td/a/@href').extract()
        print(url_list)

        for url in url_list:
            url = "https://www.aqistudy.cn/historydata/" + url

            print('monthurl-{}'.format(url))
            # yield scrapy.Request(url=url, callback=self.parse_day, meta={'city': response.meta['city']})
            # if url.find('2017') > 0 or url.find('2018') > 0:
            if url.find('2017') > 0 or url.find('2018') > 0:
                print("进入parse_day的url-{}".format(url))
                yield scrapy.Request(url=url, callback=self.parse_day)

    def parse_day(self, response):
        print('爬取最终数据...')
        item = WeathersplierItem()
        node_list = response.xpath('//tr')
        node_list.pop(0)  # 去除第一行标题栏
        for node in node_list:
            item['data'] = node.xpath('./td[1]/text()').extract_first()

            # item['city'] = response.meta['city']
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]/text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()

            # print(node.xpath('./td[1]/text()').extract_first())
            # print(item)
            yield item

    # name = 'weather_spider'
    # allowed_domains = ['www.aqistudy.cn']
    # start_urls = ['https://www.aqistudy.cn/historydata/daydata.php?city=%E5%B9%BF%E5%B7%9E&month=201509']
    #
    # def start_requests(self):
    #     yield Request('https://www.aqistudy.cn/historydata/daydata.php?city=%E5%B9%BF%E5%B7%9E&month=201509',
    #                   callback=self.parse)
    #
    # def parse(self, response):
    #     tr_list = response.xpath("/html/body/div[3]/div[1]/div[1]/table/tbody/tr")
    #
    #     print(tr_list)
    #     for i in tr_list:
    #         weather_item = WeathersplierItem
    #         weather_item['date'] = i.xpath(".//td[1]//text()").extract_first()
    #         # print(i.xpath(".//td[1]//text()").extract_first())
