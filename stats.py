import glob
import operator

tag_count = {}
tag_word_count = {}


def get_stats(filepath):
    total_tokens = 0
    files = glob.glob(filepath)
    for filename in files:
        with open(filename, 'r', encoding='utf8') as f:
            content = f.read()
        
        words = content.splitlines()
        word = ''
        prev_tag = 'O'
        for word_item in words:
            word_items = word_item.split()

            if len(word_items) != 2:
                continue

            total_tokens += 1
            curr_word = word_items[0]
            ne_tag = word_items[1]

            if ne_tag == 'O':
                if word != '':
                    add_to_counter(word, prev_tag)
                prev_tag = ne_tag
                word = ''
            else:
                if prev_tag == ne_tag:
                    word += curr_word
                else:
                    word = curr_word
                prev_tag = ne_tag

    print(tag_count)
    print('Total Tokens:', total_tokens)
    print('Total Documents:', len(files))

    print('Most frequent words:')
    for key, value in tag_word_count.items():
        print(key)
        sorted_words = sorted(value.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_words[0:10])

    print('\n')


def add_to_counter(word, ne_tag):
    if ne_tag not in tag_count:
        tag_count[ne_tag] = 1
        tag_word_count[ne_tag] = {}
        tag_word_count[ne_tag][word] = 1
    else:
        tag_count[ne_tag] += 1
        if word not in tag_word_count[ne_tag]:
            tag_word_count[ne_tag][word] = 1
        else:
            tag_word_count[ne_tag][word] += 1


if __name__ == '__main__':
    print('CL1199')
    get_stats('results/CL1199/*.txt')
    print('CL1667')
    get_stats('results/CL1667/*.txt')
