from scrapy import Spider, Request
from string import ascii_lowercase
import os
from bs4 import BeautifulSoup
from ScrambleDict.items import URLItem


HOME_URL = 'https://dictionary.cambridge.org/browse/english-chinese-traditional/'

class VocabURLsSpider(Spider):
    name = 'vocab_urls_spider'
    start_urls = [os.path.join(HOME_URL, alphabet) for alphabet in ascii_lowercase]
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    def parse(self, response):
        self.logger.info(f'Parse {response.url}')
        res_bs = BeautifulSoup(response.text, 'html.parser')
        guide_urls = res_bs.findAll('li', {'class': 'han t-i'})
        for gu in guide_urls:
            for hyperlink in gu.findAll('a'):
                url = hyperlink.get('href')
                yield Request(url, callback=self.fetch_vocab_urls, headers=self.headers)
    
    def fetch_vocab_urls(self, response):
        res_bs = BeautifulSoup(response.text, 'html.parser')
        vocab_urls = res_bs.findAll('li', {'class': 'han t-i'})
        for vu in vocab_urls:
            for hyperlink in vu.findAll('a'):
                url_item = URLItem()
                url_item['url'] = hyperlink.get('href')
                yield url_item