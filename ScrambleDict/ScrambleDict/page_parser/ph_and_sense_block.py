from bs4 import BeautifulSoup
from .utils import find_all, fetch_text


def fetch_def_and_examples(sense_block_bs: BeautifulSoup):
    sense_head_block_bs = find_all(sense_block_bs, 'ddef_h')[0]
    en_def = fetch_text(sense_head_block_bs, 'ddef_d')
    sense_body_block_bs = find_all(sense_block_bs, 'ddef_b')[0]
    ch_def = fetch_text(sense_body_block_bs, 'dtrans')
    example_blocks_bs = find_all(sense_body_block_bs, 'dexamp')
    example_sents = fetch_example_sents(example_blocks_bs)
    return (en_def, ch_def, example_sents)

def fetch_example_sents(example_blocks_bs: BeautifulSoup):
    example_sents = []
    for block_bs in example_blocks_bs:
        en_sent = fetch_text(block_bs, 'deg')
        ch_sent = fetch_text(block_bs, 'dtrans')
        example_sents.append({'en': en_sent,
                              'ch': ch_sent})
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
            level = fetch_text(info_block_bs[0], 'dxref').strip()
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
            level = fetch_text(info_block_bs[0], 'dxref').strip()
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