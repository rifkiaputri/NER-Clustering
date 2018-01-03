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
    files = glob.glob('datasets/partial/*.txt')
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
    for sentence in sentences:
        #pos_token = j.seg(sentence, pos=True)
        seg = pseg.cut(sentence)
        pos_token = []
        for tok in seg:
            pos_token.append((tok.word, tok.flag))
        prev_tok = ''
        prev_pos = ''
        for item in pos_token:
            pos_tag = item[1]
            tok = item[0]
            if (pos_tag == 'm' and tok.isdigit()) or pos_tag == 'n':
                prev_tok = tok
                prev_pos = pos_tag
            elif pos_tag in ['nt', 'ns', 'nr']:
                if pos_tag == 'n':
                    tokens.append(prev_tok)
                tokens.append(tok)
                prev_tok = ''
                prev_pos = ''
            else:
                if (pos_tag == 'm' and prev_pos == 'm') or (pos_tag == 'nr' and prev_pos == 'n') or (pos_tag == 'n' and prev_pos == 'n'):
                    tokens.append(prev_tok + ' ' + tok)
                elif prev_pos == 'n' and pos_tag != 'n':
                    tokens.append(prev_tok)
                prev_tok = ''
                prev_pos = ''
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
