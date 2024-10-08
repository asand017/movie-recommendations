# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals # type: ignore

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter # type: ignore

import random
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import ssl
import logging
# from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

class RottenTomatoesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
   
        # logging.debug(f'RESPONSE: {response.body}')
        # print("request: " + response.request.url)
        # print("response metadata: " + response.meta.get('real_title'))
        # print("response test: " + response.text)

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RottenTomatoesDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# class CustomClientContextFactory(ScrapyClientContextFactory):
#     def __init__(self):
#         self.sslcontext = ssl.create_default_context()

#         # Disable only hostname verification
#         self.sslcontext.check_hostname = False

#         # Keep certificate validation enabled
#         self.sslcontext.verify_mode = ssl.CERT_REQUIRED

#     def getContext(self, hostname=None, port=None):
#         return self.sslcontext

class MovieValidateMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # print("request: " + request.url)
        # print("response: " + response.)

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# class CustomClientContextFactory(ScrapyClientContextFactory):
#     def __init__(self):
#         self.sslcontext = ssl.create_default_context()

#         # Disable only hostname verification
#         self.sslcontext.check_hostname = False

#         # Keep certificate validation enabled
#         self.sslcontext.verify_mode = ssl.CERT_REQUIRED

#     def getContext(self, hostname=None, port=None):
#         return self.sslcontext

# class RotateUserAgentMiddleware:
#     user_agents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
#         # Add more user agents here
#     ]

#     def process_request(self, request, spider):
#         request.headers['User-Agent'] = random.choice(self.user_agents)

class ProxyMiddleware:
    def __init__(self):
        self.proxies = fetch_free_proxies()
        # Alternatively, load proxies from a file
        # with open('proxies.txt', 'r') as f:
        #     self.proxies = [line.strip() for line in f]

    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            request.meta['proxy'] = f"http://{proxy}"
            spider.log(f'Using proxy: {proxy}')

def fetch_free_proxies():
    url = 'https://www.free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    
    for row in soup.find('table').find_all('tr')[1:]:
        cols = row.find_all('td')
        if cols[4].text == 'elite proxy' and cols[6].text == 'yes':
            proxy = f"{cols[0].text}:{cols[1].text}"
            proxies.append(proxy)
    
    return proxies