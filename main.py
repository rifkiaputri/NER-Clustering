import nltk
import glob

seg = nltk.tokenize.StanfordSegmenter()
seg.default_config('zh')
ner = nltk.tag.StanfordNERTagger('chinese.misc.distsim.crf.ser.gz')


def get_tagged_sentences(filename):
    with open(filename, 'r', encoding='utf8') as f:
        sample = f.read()

    sentences = sample.splitlines()
    tokenized_sentences = [seg.segment(sentence) for sentence in sentences]
    tagged_sentences = [ner.tag(tokenized_sentence.split()) for tokenized_sentence in tokenized_sentences]

    return tagged_sentences


def main():
    files = glob.glob('CL1667/*.txt')
    for file in files:
        print(file)
        tagged_sentences = get_tagged_sentences(file)
        out_filename = 'results/' + file
        with open(out_filename, 'w', encoding='utf8') as f:
            for sentence in tagged_sentences:
                f.write('\n'.join('%s %s' % x for x in sentence))
                f.write('\n')


if __name__ == '__main__':
    main()
