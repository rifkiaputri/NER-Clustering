import gensim
from config import word2vec_config, model_path
from dataset_reader import get_dataset, tokenize_per_sentence
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize


def train_model():
    docs = get_dataset()
    sentences = []
    print('Tokenizing sentences...')
    for text in docs:
        tokenizer_result = tokenize_per_sentence(text)
        for item in tokenizer_result:
            if len(item) != 0:
                sentences.append(item)

    print('Training Word2Vec...')
    model = gensim.models.Word2Vec(sentences, **word2vec_config)
    model.save(model_path)
    print('Word2Vec model saved in', model_path, 'directory.')


def test_load_model():
    model = gensim.models.Word2Vec.load(model_path)
    print(model.most_similar('19 日', topn=10))


def get_pca_vectors():
    pc_number = 2
    pca = PCA(n_components=pc_number)
    model = gensim.models.Word2Vec.load(model_path)
    vec_list = [model[i] for i in model.wv.vocab.keys()]
    # you should always normalize vectors before running PCA
    normalized_vec = normalize(vec_list)
    pca.fit(normalized_vec)
    reduced_vec = pca.transform(normalized_vec)
    pca_vectors = {word: vec for word, vec in zip(model.wv.vocab.keys(), reduced_vec)}
    return pca_vectors


if __name__ == '__main__':
    train_model()
