import json
import os
import pandas as pd

def filter_out_no_data(vocab_data):
    home_url = 'https://dictionary.cambridge.org/dictionary/english-chinese-traditional'
    no_data_url = []
    vocab_data_remain = []
    for vd in vocab_data:
        vocab, data = list(vd.items())[0]
        if data:
            vocab_data_remain.append(vd)
        else:
            no_data_url.append(os.path.join(home_url, vocab))
    with open('have_no_data_urls.txt', 'w') as f:
        for url in no_data_url:
            f.write(url + '\n')
    print('write the urls without data to `have_no_data_urls.txt`.')
    return vocab_data_remain

def convert_vocab_data_to_final_json(vocab_data):
    final_json = {}
    for vd in vocab_data:
        vocab, data = list(vd.items())[0]
        final_json[vocab] = data
    return final_json

def collect_examples(camb_dict):
    sense_examples = []
    phrase_examples = []
    extra_examples = []
    for vocab, pos_dict in camb_dict.items():
        for pos_tag, pos_blocks in pos_dict.items():
            for pos_block in pos_blocks:
                for big_sense_block in pos_block['big_sense']:
                    data = [vocab, pos_tag, pos_block['headword'],
                            big_sense_block['guideword']]
                    cur_sense_examples = collect_sense_examples(data, big_sense_block['sense'])
                    sense_examples.extend(cur_sense_examples)
                    cur_phrase_examples = collect_phrase_examples(data, big_sense_block['phrase'])
                    phrase_examples.extend(cur_phrase_examples)
                    cur_extra_examples = collect_extra_examples(data, big_sense_block['extra_sents'])
                    extra_examples.extend(cur_extra_examples)
    return (sense_examples, phrase_examples, extra_examples)

def collect_sense_examples(big_sense_data, sense_blocks):
    sense_examples = []
    for sense_block in sense_blocks:
        sense_data = big_sense_data + [sense_block['en_def'], sense_block['ch_def'],
                                       sense_block['level'], sense_block['gcs']]
        if not sense_block['examples']:
            sense_examples.append(sense_data + ['', ''])
        else:
            for example in sense_block['examples']:
                sense_examples.append(sense_data + [example['en'], example['ch']])
    return sense_examples

def collect_phrase_examples(big_sense_data, phrase_blocks):
    phrase_examples = []
    for phrase_block in phrase_blocks:
        phrase_data = big_sense_data + [phrase_block['term'],
                                        phrase_block['level']]
        for sense_block in phrase_block['sense']:
            sense_data = phrase_data + [sense_block['en_def'],
                                        sense_block['ch_def']]
            if not sense_block['examples']:
                phrase_examples.append(sense_data + ['', ''])
            else:
                for example in sense_block['examples']:
                    phrase_examples.append(sense_data + [example['en'],
                                                         example['ch']])
    return phrase_examples

def collect_extra_examples(big_sense_data, extra_sents):
    extra_examples = [big_sense_data + [sent] for sent in extra_sents]
    return extra_examples

def main():
    with open('vocab_data.json', 'r') as f:
        vocab_data = json.load(f)
    
    vocab_data = filter_out_no_data(vocab_data)

    final_json = convert_vocab_data_to_final_json(vocab_data)
    with open('cambridge.word.888.json', 'w') as f:
        json.dump(final_json, f)

    sense_examples, phrase_examples, extra_examples = collect_examples(final_json)
    basic_columns = ['vocab', 'pos_tag', 'headword', 'guideword']
    sense_columns = basic_columns + ['en_def', 'ch_def', 'level', 'gcs', 'en', 'ch']
    sense_examples = pd.DataFrame(sense_examples, columns=sense_columns)
    sense_examples.to_csv('sense_examples.tsv', index=False, sep='\t')

    phrase_columns = basic_columns + ['term', 'level', 'en_def', 'ch_def', 'en', 'ch']
    phrase_examples = pd.DataFrame(phrase_examples, columns=phrase_columns)
    phrase_examples.to_csv('phrase_examples.tsv', index=False, sep='\t')

    extra_exp_columns = basic_columns + ['en']
    extra_examples = pd.DataFrame(extra_examples, columns=extra_exp_columns)
    extra_examples.to_csv('extra_examples.tsv', index=False, sep='\t')
    return

if __name__ == '__main__':
    main()