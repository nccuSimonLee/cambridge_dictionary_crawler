from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .utils import find_all
from .big_sense_block import BigSenseBlock



class POSBlockAPI(ABC):
    def __init__(self, pos_block_bs: BeautifulSoup):
        self.pos_block_bs = pos_block_bs
        self.headword = self.fetch_head_word()
        self.pos_tag = self.fetch_pos_tag()
        self.big_sense_blocks = self.fetch_big_sense_blocks()
        return

    @abstractmethod
    def fetch_head_word(self):
        pass

    @abstractmethod
    def fetch_pos_tag(self):
        pass

    @abstractmethod
    def fetch_big_sense_blocks(self):
        pass


class POSBlock(POSBlockAPI):
    def __init__(self, pos_block_bs: BeautifulSoup):
        super(POSBlock, self).__init__(pos_block_bs)
        return

    def fetch_head_word(self):
        header_bs = self.pos_block_bs.select('.pos-header')
        title_bs = header_bs[0].select('.di-title')[0]
        head_word = title_bs.select('.dpos-h_hw')[0].text
        return head_word

    def fetch_pos_tag(self):
        header_block_bs = find_all(self.pos_block_bs, 'pos-header')[0]
        pos_tag_block_bs = header_block_bs.select('.pos')
        pos_tag = [pos_tag.text for pos_tag in pos_tag_block_bs]
        if not pos_tag:
            pos_tag = ['']
        return pos_tag

    def fetch_big_sense_blocks(self):
        body_block_bs = find_all(self.pos_block_bs, 'pos-body')[0]
        big_sense_blocks = find_all(body_block_bs, 'dsense')
        big_sense_blocks = [BigSenseBlock(block_bs) for block_bs in big_sense_blocks]
        return big_sense_blocks


class PhraseVerbBlock(POSBlockAPI):
    def __init__(self, pos_block_bs: BeautifulSoup):
        self.pv_block_bs = pos_block_bs.select('.pv-block')
        assert len(self.pv_block_bs) == 1
        self.pv_block_bs = self.pv_block_bs[0]
        super(PhraseVerbBlock, self).__init__(pos_block_bs)
        return

    def fetch_head_word(self):
        title_bs = self.pv_block_bs.select('.di-title')[0]
        head_word = title_bs.select('.dpos-h_hw')[0].text
        return head_word
    
    def fetch_pos_tag(self):
        info_block_bs = find_all(self.pv_block_bs, 'di-info')[0]
        header_block_bs = find_all(info_block_bs, 'pos-header')[0]
        pos_tag_block_bs = header_block_bs.select('.pos')
        pos_tag = [pos_tag.text for pos_tag in pos_tag_block_bs]
        if not pos_tag:
            pos_tag = ['']
        return pos_tag

    def fetch_big_sense_blocks(self):
        body_block_bs = find_all(self.pv_block_bs, 'dpv-body')[0]
        big_sense_blocks = find_all(body_block_bs, 'dsense')
        big_sense_blocks = [BigSenseBlock(block_bs) for block_bs in big_sense_blocks]
        return big_sense_blocks


class IdiomBlock(POSBlockAPI):
    def __init__(self, pos_block_bs: BeautifulSoup):
        super(IdiomBlock, self).__init__(pos_block_bs)

    def fetch_head_word(self):
        title_bs = self.pos_block_bs.select('.di-title')[0]
        head_word = title_bs.select('.dpos-h_hw')[0].text
        return head_word 

    def fetch_pos_tag(self):
        return ['idiom']
    
    def fetch_big_sense_blocks(self):
        body_block_bs = find_all(self.pos_block_bs, 'didiom-body')[0]
        big_sense_blocks = find_all(body_block_bs, 'dsense')
        big_sense_blocks = [BigSenseBlock(block_bs) for block_bs in big_sense_blocks]
        return big_sense_blocks