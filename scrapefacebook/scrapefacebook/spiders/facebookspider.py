# -*- coding: utf-8 -*-

# Code is written by Vaibhav sharma




import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
import time

class FacebookspiderSpider(scrapy.Spider):
    name = 'facebookspider'

    def start_requests(self):

        yield SeleniumRequest(
            url="https://www.facebook.com/",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            # meta={'index': index},
            dont_filter=True
        )


    def parse(self, response):

        driver = response.meta['driver']

        driver.find_element_by_xpath("//*[@id='email']").clear()
        search_input1 = driver.find_element_by_xpath("//*[@id='email']")
        search_input1.send_keys('') # user email id
        # time.sleep(3)
        driver.find_element_by_xpath("//*[@id='pass']").clear()
        search_input2 = driver.find_element_by_xpath("//*[@id='pass']")
        search_input2.send_keys('') # user password
        # time.sleep(3)
        search_button = driver.find_element_by_xpath("//*[@id='loginbutton']")
        search_button.click()

        time.sleep(10)
        html = driver.page_source
        response_obj = Selector(text=html)
        url=response_obj.xpath("//*[@id='mount_0_0']/div/div/div[1]/div[2]/div[4]/div[1]/div[4]/a/@href").get()
        # search_button = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div/div[1]/div[2]/div[4]/div[1]/div[4]/a")
        # search_button.click()
        # time.sleep(10)
        yield SeleniumRequest(
            url="https://www.facebook.com"+url,
            wait_time=1000,
            screenshot=True,
            callback=self.parse_friends,
            # meta={'index': index},
            dont_filter=True
        )

    def parse_friends(self,response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        # button = response_obj.xpath('//*[@id="mount_0_0"]/div/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div[1]/a[3]')
        # search_button = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div[1]/a[3]")
        # search_button.click()

        url = response_obj.xpath("//*[@id='mount_0_0']/div/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div[1]/a[3]/@href").get()
        yield SeleniumRequest(
            url=url,
            wait_time=1000,
            screenshot=True,
            callback=self.parse_friendsdetails,
            # meta={'index': index},
            dont_filter=True
        )




    def parse_friendsdetails(self,response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)

        friends = response_obj.xpath('//*[@id="mount_0_0"]/div/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[4]/div/div/div/div/div/div[3]/div/div[2]/div[1]/a')
        for friend in friends:
            name = friend.xpath('.//span/text()').get()
            yield {
                'name': name
            }
        time.sleep(5)

# Code is written by Vaibhav sharma