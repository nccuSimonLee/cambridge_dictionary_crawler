import json
import os

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

def main():
    with open('vocab_data.json', 'r') as f:
        vocab_data = json.load(f)
    
    vocab_data = filter_out_no_data(vocab_data)

    final_json = convert_vocab_data_to_final_json(vocab_data)
    with open('cambridge.word.888.json', 'w') as f:
        json.dump(final_json, f)


if __name__ == '__main__':
    main()