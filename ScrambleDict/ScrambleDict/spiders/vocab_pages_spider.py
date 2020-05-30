from ..page_parser import VocabPage, fetch_vocab_data
from scrapy import Spider, Request
import os
from bs4 import BeautifulSoup


class VocabPagesSpider(Spider):
    name = 'vocab_pages_spider'
    with open('vocab_urls.csv', 'r') as f:
        start_urls = f.read().split('\n')[1:-1][:100]

    def parse(self, response):
        vocab_page_bs = BeautifulSoup(response.text, 'html.parser')
        vocab = response.url.split('/')[-1]
        self.logger.info(f'trying to parse f{response.url}')
        try:
            vocab_page = VocabPage(vocab, vocab_page_bs)
            vocab_data = fetch_vocab_data(vocab_page)
            yield {vocab: vocab_data}
        except:
            self.logger.error(f'error occured while parsing {response.url}',
                              exc_info=True)