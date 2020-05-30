from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .utils import find_all
from .big_sense_block import BigSenseBlock



class POSBlockAPI(ABC):
    def __init__(self, pos_block_bs: BeautifulSoup):
        self.pos_block_bs = pos_block_bs
        self.pos_tag = self.fetch_pos_tag()
        self.big_sense_blocks = self.fetch_big_sense_blocks()
        return

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

    def fetch_pos_tag(self):
        header_block_bs = find_all(self.pos_block_bs, 'pos-header')[0]
        pos_tag_block_bs = header_block_bs.select('.pos')
        pos_tag = pos_tag_block_bs[0].text if pos_tag_block_bs else ''
        return pos_tag

    def fetch_big_sense_blocks(self):
        body_block_bs = find_all(self.pos_block_bs, 'pos-body')[0]
        big_sense_blocks = find_all(body_block_bs, 'dsense')
        big_sense_blocks = [BigSenseBlock(block_bs) for block_bs in big_sense_blocks]
        return big_sense_blocks