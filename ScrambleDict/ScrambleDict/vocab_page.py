from bs4 import BeautifulSoup


# block 的意思是指劍橋網頁上的各個部分的組成結構，就像是一個個的 block 一樣。

class VocabPage(object):
    def __init__(self, vocab_page_bs: BeautifulSoup):
        self.vocab_page_bs = vocab_page_bs
        self.url = vocab_page_bs.url
        self.vocab = self.url.split('/')[-1]
        self.pos_blocks = []


class POSBlock(object):
    def __init__(self, pos_block_bs: BeautifulSoup):
        self.pos_block_bs = pos_block_bs
        self.pos_tag = ''
        self.big_sense_blocks = []


class BigSenseBlock(object):
    def __init__(self, big_sense_block_bs: BeautifulSoup):
        self.big_sense_block_bs = big_sense_block_bs
        self.guideword = ''
        self.sense_blocks = []
        self.phrase_blocks = []
        self.extra_sents = []


class SenseBlock(object):
    def __init__(self, sense_block_bs: BeautifulSoup):
        self.sense_block_bs = sense_block_bs
        self.en_def = ''
        self.ch_def = ''
        self.level = ''
        self.examples = []


class PhraseBlock(object):
    def __init__(self, phrase_block_bs: BeautifulSoup):
        self.phrase_block_bs = phrase_block_bs
        self.term = ''
        self.en_def = ''
        self.ch_def = ''
        self.level = ''
        self.examples = []