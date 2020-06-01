from bs4 import BeautifulSoup
from .utils import find_all, fetch_text
from .pos_block import POSBlock, PhraseVerbBlock, IdiomBlock


# block 的意思是指劍橋網頁上的各個部分的組成結構，就像是一個個的 block 一樣。
class VocabPage(object):
    def __init__(self, vocab, vocab_page_bs: BeautifulSoup):
        self.vocab_page_bs = vocab_page_bs
        self.vocab = vocab
        self.pos_blocks = self.fetch_pos_blocks()

    def fetch_pos_blocks(self):
        pos_blocks = self.vocab_page_bs.select('div.entry-body__el')
        if pos_blocks:
            pos_blocks = [PhraseVerbBlock(block_bs) if block_bs.select('.pv-block') else POSBlock(block_bs)
                        for block_bs in pos_blocks]
        else:
            pos_blocks = self.vocab_page_bs.findAll('div', {'class': 'pr idiom-block'})[0]
            pos_blocks = find_all(pos_blocks, 'idiom-block')
            pos_blocks = [IdiomBlock(block_bs) for block_bs in pos_blocks]
        return pos_blocks