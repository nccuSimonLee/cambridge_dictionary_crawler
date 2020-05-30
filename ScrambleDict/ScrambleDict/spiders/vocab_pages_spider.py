from ..page_parser import VocabPage, fetch_vocab_data
from ..set_logger import set_config_and_get_logger
from scrapy import Spider, Request
import os
from bs4 import BeautifulSoup

logger = set_config_and_get_logger('VOCAB_PAGES_SPIDER')

class VocabPagesSpider(Spider):
    name = 'vocab_pages_spider'
    with open('vocab_urls.csv', 'r') as f:
        start_urls = f.read().split('\n')[1:-1]

    def parse(self, response):
        vocab_page_bs = BeautifulSoup(response.text, 'html.parser')
        vocab = response.url.split('/')[-1]
        logger.info(f'trying to parse {response.url}')
        try:
            vocab_page = VocabPage(vocab, vocab_page_bs)
            vocab_data = fetch_vocab_data(vocab_page)
            yield {vocab: vocab_data}
        except:
            logger.error(f'error occured while parsing {response.url}',
                           exc_info=True)