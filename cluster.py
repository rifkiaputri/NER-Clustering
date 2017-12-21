import numpy as np

from dataset_reader import get_dataset, tokenize
from embedding import get_pca_vectors
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from matplotlib import font_manager as mfm
from numbers import Number


vocabulary = []
vocab_index = {}
vocab_size = 0
doc_size = 0
font_props = mfm.FontProperties(fname='results/SimHei.ttf')


class autovivify_list(dict):
    '''A pickleable version of collections.defaultdict'''
    def __missing__(self, key):
        '''Given a missing key, set initial value to an empty list'''
        value = self[key] = []
        return value

    def __add__(self, x):
        '''Override addition for numeric types when self is empty'''
        if not self and isinstance(x, Number):
          return x
        raise ValueError

    def __sub__(self, x):
        '''Also provide subtraction method'''
        if not self and isinstance(x, Number):
          return -1 * x
        raise ValueError


def build_vocabulary(docs):
    """
    Build vocabulary based on the documents
    :param docs: list of document
    :return: void
    """
    print('Building vocabulary...')
    vocab = set()
    for text in docs:
        words = tokenize(text)
        vocab.update(words)

    global vocabulary
    vocabulary = sorted(list(vocab))
    global vocab_size
    vocab_size = len(vocabulary)
    print('Vocabulary size:', vocab_size)


def cluster_agglomerative(n_cluster):
    return AgglomerativeClustering(linkage='complete', n_clusters=n_cluster)


def cluster_kmeans(n_cluster):
    return KMeans(init='k-means++', n_clusters=n_cluster, n_init=10)


def find_word_clusters(labels_array, cluster_labels):
    cluster_to_words = autovivify_list()
    for c, i in enumerate(cluster_labels):
        cluster_to_words[i].append(labels_array[c])
    return cluster_to_words


def plot_clustering(X, labels, title=None):
    x_min, x_max = np.min(X, axis=0), np.max(X, axis=0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(6, 4))
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], vocabulary[i],
                 color=plt.cm.spectral(labels[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9},
                 fontproperties=font_props)

    plt.xticks([])
    plt.yticks([])
    if title is not None:
        plt.title(title, size=17)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    embedding = get_pca_vectors()
    docs = get_dataset()
    build_vocabulary(docs)

    terms = np.zeros((vocab_size, 2))
    for idx, term in enumerate(vocabulary):
        term_item = term.split()
        for item in term_item:
            try:
                vec = embedding[item]
            except KeyError:
                vec = np.zeros(2)
            terms[idx] = (terms[idx] + vec) / 2

    print('Start clustering...')

    '''
    n_clusters = [3, 4, 5, 6, 7]
    max_score = 0
    optimum_cluster = 0
    for n_cluster in n_clusters:
        clustering = cluster_kmeans(n_cluster)
        print('Fit cluster:', n_cluster)
        clustering.fit(terms)
        silhouette_avg = silhouette_score(terms, clustering.labels_)
        if silhouette_avg > max_score:
            max_score = silhouette_avg
            optimum_cluster = n_cluster
        print('For n_clusters =', n_cluster, 'The average silhouette_score is :', silhouette_avg)

    '''
    optimum_cluster = 3
    print('Number of optimum cluster is=', optimum_cluster)
    clustering = cluster_kmeans(optimum_cluster)
    clustering.fit(terms)

    cluster_to_words = find_word_clusters(vocabulary, clustering.labels_)
    for c in cluster_to_words:
        print(cluster_to_words[c])
        print('Number of elements in cluster:', len(cluster_to_words[c]))
    plot_clustering(terms, clustering.labels_, 'result')


if __name__ == '__main__':
    main()
