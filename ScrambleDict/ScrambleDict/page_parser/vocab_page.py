from bs4 import BeautifulSoup
from .utils import find_all, fetch_text
from .pos_block import POSBlock


# block 的意思是指劍橋網頁上的各個部分的組成結構，就像是一個個的 block 一樣。
class VocabPage(object):
    def __init__(self, vocab, vocab_page_bs: BeautifulSoup):
        self.vocab_page_bs = vocab_page_bs
        self.vocab = vocab
        self.pos_blocks = self.fetch_pos_blocks()

    def fetch_pos_blocks(self):
        pos_blocks = self.vocab_page_bs.select('div.entry-body__el')
        pos_blocks = [POSBlock(block_bs) for block_bs in pos_blocks]
        return pos_blocks