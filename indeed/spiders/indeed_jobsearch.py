from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time 
import sys
import random
import os
from string import join

from indeed.items import indeedItem

#chrome stuff
chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

class indeedSpider(InitSpider):
    name = "indeed_jobsearch"
    allowed_domains = ["indeed.com"]
    search_page = 'http://www.indeed.com/'

    start_urls=['http://www.indeed.com/']

    def __init__(self,whatsearch="data science scientist",wheresearch="united states"):
    #def __init__(self,whatsearch="\"data scientist\"",wheresearch="united states"):
        InitSpider.__init__(self)
        self.verificationErrors = []

        #login selenium
        self.driver = webdriver.Chrome(chromedriver)
        self.itemcount=0
        self.whatsearch=whatsearch
        self.wheresearch=wheresearch
        self.pagecount = 0
        self.maxcount=0
        self.rooturl =''

    def parse(self, response):
        if response.url == 'http://www.indeed.com/':
            self.driver.get(response.url)
            element = self.driver.find_element_by_id("what")
            element.send_keys(self.whatsearch)
            element = self.driver.find_element_by_id("where")
            element.clear()
            element.send_keys(self.wheresearch)
            element.submit()

            #load search results
            WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_id('searchCount').is_displayed())
            element=self.driver.find_element_by_id("searchCount")
            jobcount=element.text.split()[-1]
            self.maxcount = int(join(jobcount.split(','),''))

            self.rooturl = self.driver.current_url
            print '#Total jobcount: %s'%jobcount.strip(',')
            yield Request(self.driver.current_url, callback=self.parse)

        try: #identify results page
            WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_id('searchCount').is_displayed())
            element = self.driver.find_element_by_xpath('//tr/td[2]/div[5]/h2/a')
            self.pagecount+=1
            print '#%d'%self.pagecount

            title = element.get_attribute("title")
            url = element.get_attribute("href")

            #capture total result count and print
            element=self.driver.find_element_by_id("searchCount")

            #capture the 10 results on this page
            x=range(5,15)
            E1=['//div[{0}]/h2[@class="jobtitle"]/a[@itemprop="title"]'.format(str(i)) for i in x]
            E2=['//div[{0}]/span/span[@itemprop="name"]'.format(str(i)) for i in x]
            E3=['//tr/td[2]/div[{0}]/span[2]/span/span[@itemprop="addressLocality"]'.format(str(i)) for i in x]

            for i in range(len(E1)):
                #print i
                try:
                    element = self.driver.find_element_by_xpath(E1[i])
                    title = element.get_attribute("title")
                    url = element.get_attribute("href")

                    element = self.driver.find_element_by_xpath(E2[i])
                    company = element.text

                    element = self.driver.find_element_by_xpath(E3[i])
                    location = element.text
                 
                    item = indeedItem()

                    item ['title'] = title
                    item ['url'] = url
                    item ['location'] = location
                    item ['company'] = company
            
                    yield item
                except: pass

            jobcount = self.pagecount*10
            nexturl = '%s&start=%d'%(self.rooturl,jobcount)


            print '#jobcount=%d maxcount=%d'%(jobcount,self.maxcount)
            if jobcount<=self.maxcount: #max number of reported results
                self.driver.get(nexturl)
                WebDriverWait(self.driver,10).until(lambda x: x.find_element_by_id('searchCount').is_displayed())
                yield Request(self.driver.current_url, callback=self.parse)
     
        except: pass
