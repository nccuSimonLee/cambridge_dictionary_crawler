def find_all(bs, _class):
    return bs.findAll(attrs={'class': _class}, recursive=False)


def fetch_text(bs, _class):
    text_block = find_all(bs, _class)
    text = text_block[0].text if text_block else ''
    return text