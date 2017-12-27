import glob
import re
import jieba.posseg as pseg

from stopwords_zh import ZH_STOP_WORDS
from jseg import Jieba
from zhon import hanzi

punctuation = hanzi.punctuation
stop_words = set(ZH_STOP_WORDS)
pattern = u'([\u4e00-\u9fff0-9a-zA-Z]|(?<=[0-9])[^\u4e00-\u9fff0-9a-zA-Z]+(?=[0-9]))'
j = Jieba()


def get_dataset():
    """
    Read the dataset and return it as a list.
    :return: list of document name and its content
    """
    print('Reading dataset...')
    #files = glob.glob('datasets/partial/CL1667_0404.txt')
    files = glob.glob('datasets/*/*.txt')
    data = []
    for file in files:
        with open(file, 'r', encoding='utf8') as f:
            data.append(f.read())
    global doc_size
    doc_size = len(data)
    print('Total documents:', doc_size)
    return data


def tokenize(text):
    """
    Tokenize the text
    :param text: text string
    :return: list of words after tokenization
    """
    sentences = text.splitlines()
    tokens = []
    it = 0
    for sentence in sentences:
        pos_token = j.seg(sentence, pos=True)
        print(pos_token)
        seg = pseg.cut(sentence)
        test = []
        for tok in seg:
            test.append((tok.word, tok.flag))
        print('Baru:', test)
        prev_tok = ''
        prev_pos = ''
        for item in pos_token:
            pos_tag = item[1]
            tok = item[0]
            if pos_tag == 'P21' or (pos_tag == 'NN' and tok.isdigit()):
                prev_tok = tok
                prev_pos = pos_tag
            else:
                if pos_tag in ['Nfg', 'Ndabc', 'Nca'] and prev_pos == 'NN':
                    tokens.append(prev_tok + ' ' + tok)
                elif pos_tag in ['Nca'] and prev_pos == 'P21':
                    tokens.append(tok)
                prev_tok = ''
                prev_pos = ''
        it += 1
        if it >= 6:
            quit()
    return tokens


def tokenize_per_sentence(text):
    """
    Tokenize the text
    :param text: text string
    :return: list of words after tokenization
    """
    sentences = text.splitlines()
    tokens = []
    for sentence in sentences:
        seg_tokens = pseg.cut(sentence)
        token = []
        for tok in seg_tokens:
            token.append(tok.word)
        tokens.append(token)
    return tokens
