from collections import defaultdict


def find_all(bs, _class):
    return bs.findAll(attrs={'class': _class}, recursive=False)


def fetch_text(bs, _class):
    text_block = find_all(bs, _class)
    text = text_block[0].text if text_block else ''
    return text

def fetch_vocab_data(vocab_page):
    vocab_data = defaultdict(lambda: [])
    for pos_block in vocab_page.pos_blocks:
        pos_data = fetch_pos_data(pos_block)
        for pos_tag in pos_block.pos_tag:
            vocab_data[pos_tag].append(pos_data)
    return vocab_data

def fetch_pos_data(pos_block):
    big_sense_data_list = [fetch_big_sense_data(big_sense_block)
                           for big_sense_block in pos_block.big_sense_blocks]
    pos_data = {
        'headword': pos_block.headword,
        'big_sense': big_sense_data_list,
    }
    return pos_data

def fetch_big_sense_data(big_sense_block):
    big_sense_data = {
        'guideword': big_sense_block.guideword,
        'sense': [fetch_sense_data(sense_block)
                  for sense_block in big_sense_block.sense_blocks],
        'phrase': [fetch_phrase_data(phrase_block)
                   for phrase_block in big_sense_block.phrase_blocks],
        'extra_sents': big_sense_block.extra_sents
    }
    return big_sense_data

def fetch_sense_data(sense_block):
    sense_data = {
        'en_def': sense_block.en_def,
        'ch_def': sense_block.ch_def,
        'level': sense_block.level,
        'examples': sense_block.examples
    }
    return sense_data

def fetch_phrase_data(phrase_block):
    phrase_data = {
        'term': phrase_block.term,
        'level': phrase_block.level,
        'sense': phrase_block.sense_list
    }
    return phrase_data