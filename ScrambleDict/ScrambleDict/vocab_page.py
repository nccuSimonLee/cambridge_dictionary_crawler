from bs4 import BeautifulSoup


# block 的意思是指劍橋網頁上的各個部分的組成結構，就像是一個個的 block 一樣。

def find_all(bs, _class):
    return bs.findAll(attrs={'class': _class}, recursive=False)


class VocabPage(object):
    def __init__(self, vocab, vocab_page_bs: BeautifulSoup):
        self.vocab_page_bs = vocab_page_bs
        self.vocab = vocab
        self.pos_blocks = self.fetch_pos_blocks()

    def fetch_pos_blocks(self):
        pos_blocks = self.vocab_page_bs.select('div.entry-body__el')
        pos_blocks = [POSBlock(block_bs) for block_bs in pos_blocks]
        return pos_blocks


class POSBlock(object):
    def __init__(self, pos_block_bs: BeautifulSoup):
        self.pos_block_bs = pos_block_bs
        self.pos_tag = self.fetch_pos_tag()
        self.big_sense_blocks = self.fetch_big_sense_blocks()
        return

    def fetch_pos_tag(self):
        header_block_bs = find_all(self.pos_block_bs, 'pos-header')[0]
        pos_tag = header_block_bs.select('.pos')[0].text
        return pos_tag

    def fetch_big_sense_blocks(self):
        body_block_bs = find_all(self.pos_block_bs, 'pos-body')[0]
        big_sense_blocks = find_all(body_block_bs, 'dsense')
        big_sense_blocks = [BigSenseBlock(block_bs) for block_bs in big_sense_blocks]
        return big_sense_blocks


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


def fetch_def_and_examples(sense_block_bs: BeautifulSoup):
    sense_head_block_bs = find_all(sense_block_bs, 'ddef_h')[0]
    en_def = find_all(sense_head_block_bs, 'ddef_d')[0].text
    sense_body_block_bs = find_all(sense_block_bs, 'ddef_b')[0]
    ch_def = find_all(sense_body_block_bs, 'dtrans')[0].text
    example_blocks_bs = find_all(sense_body_block_bs, 'dexamp')
    example_sents = fetch_example_sents(example_blocks_bs)
    return (en_def, ch_def, example_sents)

def fetch_example_sents(example_blocks_bs: BeautifulSoup):
    example_sents = []
    for block_bs in example_blocks_bs:
        en_sent = find_all(block_bs, 'deg')[0].text
        ch_sent = find_all(block_bs, 'dtrans')[0].text
        example_sents.extend([en_sent, ch_sent])
    return example_sents


class SenseBlock(object):
    def __init__(self, sense_block_bs: BeautifulSoup):
        self.sense_block_bs = sense_block_bs
        self.en_def, self.ch_def, self.examples = fetch_def_and_examples(sense_block_bs)
        self.level = self.fetch_sense_level()

    def fetch_sense_level(self):
        sense_head_block_bs = find_all(self.sense_block_bs, 'ddef_h')[0]
        info_block_bs = find_all(sense_head_block_bs, 'ddef-info')
        level = ''
        if info_block_bs:
            level_block_bs = find_all(info_block_bs[0], 'dxref')
            level = level_block_bs[0].text.strip() if level_block_bs else ''
        return level


class PhraseBlock(object):
    def __init__(self, phrase_block_bs: BeautifulSoup):
        self.phrase_block_bs = phrase_block_bs
        self.term, self.level = self.fetch_term_and_level()
        self.sense_list = [self.fetch_phrase_sense_data(sense_block_bs)
                           for sense_block_bs in self.fetch_phrase_sense_blocks_bs()]

    def fetch_term_and_level(self):
        phrase_head_block_bs = find_all(self.phrase_block_bs, 'dphrase_h')[0]
        term = find_all(phrase_head_block_bs, 'dphrase-title')[0].text
        info_block_bs = find_all(phrase_head_block_bs, 'dphrase-info')
        level = ''
        if info_block_bs:
            level_block_bs = find_all(info_block_bs[0], 'dxref')
            level = level_block_bs[0].text if level_block_bs else ''
        return (term, level)

    def fetch_phrase_sense_blocks_bs(self):
        body_block_bs = find_all(self.phrase_block_bs, 'dphrase_b')[0]
        phrase_sense_blocks_bs = find_all(body_block_bs, 'ddef_block')
        return phrase_sense_blocks_bs

    def fetch_phrase_sense_data(self, sense_block_bs):
        en_def, ch_def, examples = fetch_def_and_examples(sense_block_bs)
        phrase_sense_data = {
            'en_def': en_def,
            'ch_def': ch_def,
            'examples': examples
        }
        return phrase_sense_data