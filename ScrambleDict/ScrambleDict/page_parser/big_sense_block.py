from .utils import find_all
from bs4 import BeautifulSoup
from .ph_and_sense_block import SenseBlock, PhraseBlock


class BigSenseBlock(object):
    def __init__(self, big_sense_block_bs: BeautifulSoup):
        self.big_sense_block_bs = big_sense_block_bs
        self.guideword = self.fetch_guide_word()
        self.sense_blocks = self.fetch_sense_blocks()
        self.phrase_blocks = self.fetch_phrase_blocks()
        self.extra_sents = self.fetch_extra_examples()

    def fetch_guide_word(self):
        if 'dsense-noh' in self.big_sense_block_bs['class']:
            return ''
        header_block_bs = find_all(self.big_sense_block_bs, 'dsense_h')[0]
        guide_word = find_all(header_block_bs, 'dsense_gw')[0].text.strip()
        return guide_word

    def fetch_sense_blocks(self):
        body_block_bs = find_all(self.big_sense_block_bs, 'dsense_b')[0]
        sense_blocks = find_all(body_block_bs, 'ddef_block')
        sense_blocks = [SenseBlock(block_bs) for block_bs in sense_blocks]
        return sense_blocks

    def fetch_extra_examples(self):
        body_block_bs = find_all(self.big_sense_block_bs, 'dsense_b')[0]
        extra_ex_block_bs = find_all(body_block_bs, 'daccord')
        if extra_ex_block_bs:
            extra_examples = [exp_block_bs.text
                            for exp_block_bs in extra_ex_block_bs[0].select('li.dexamp')]
        else:
            extra_examples = []
        return extra_examples

    def fetch_phrase_blocks(self):
        body_block_bs = find_all(self.big_sense_block_bs, 'dsense_b')[0]
        phrase_blocks = find_all(body_block_bs, 'dphrase-block')
        phrase_blocks = [PhraseBlock(block_bs) for block_bs in phrase_blocks]
        return phrase_blocks