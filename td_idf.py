from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

def labels_to_original(labels, forclusterlist):
    assert len(labels) == len(forclusterlist)
    maxlabel = max(labels)
    numberlabel = [i for i in range(0, maxlabel + 1, 1)]
    numberlabel.append(-1)
    result = [[] for i in range(len(numberlabel))]
    for i in range(len(labels)):
        index = numberlabel.index(labels[i])
        result[index].append(forclusterlist[i])
    return result

if __name__ == '__main__':
    # 分类数
    num = 3

    # 读取语料库
    corpus = []
    txt = open("data/cut.txt", "r", encoding='utf-8').read().split("\n")
    for str in txt:
        corpus.append(str)

    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer(max_features=20000)
    # 该类会统计每个词语的tf-idf权值
    tf_idf_transformer = TfidfTransformer()
    # 将文本转为词频矩阵并计算tf-idf
    tfidf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(corpus))
    # 获取词袋模型中的所有词语
    tfidf_matrix = tfidf.toarray()
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # print(word)
    # # 统计词频
    # print(tfidf)

    # 聚成5类
    clf = KMeans(n_clusters=num)
    s = clf.fit(tfidf_matrix)

    # 每个样本所属的簇
    label = []
    i = 1
    while i <= len(clf.labels_):
        label.append(clf.labels_[i - 1])
        i = i + 1
    # 获取标签聚类
    y_pred = clf.labels_

    # pca降维，将数据转换成二维
    pca = PCA(n_components=2)  # 输出两维
    newData = pca.fit_transform(tfidf_matrix)  # 载入N维

    xs, ys = newData[:, 0], newData[:, 1]
    # 设置颜色
    cluster_colors = {0: 'r', 1: 'yellow', 2: 'b', 3: 'chartreuse', 4: 'purple', 5: '#FFC0CB', 6: '#6A5ACD',
                      7: '#98FB98'}

    # 设置类名
    cluster_names = {0: u'类0', 1: u'类1', 2: u'类2', 3: u'类3', 4: u'类4', 5: u'类5', 6: u'类6', 7: u'类7'}

    df = pd.DataFrame(dict(x=xs, y=ys, label=y_pred, title=corpus))
    groups = df.groupby('label')

    fig, ax = plt.subplots(figsize=(8, 5))  # set size
    ax.margins(0.02)
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=10, label=cluster_names[name],
                color=cluster_colors[name], mec='none')
    plt.show()

    res = labels_to_original(y_pred , corpus)

    for i in range(len(res)):
        for j in range(5):
            print(res[i][j])
        print("=======================")






