from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    datas = np.array([[1,1],[2,3],[4,5],[2,1],[-1,-1],[-2,-3],[-4,-5],[-2,-1]])
    x,y = datas[:,0],datas[:,1]

    # 设置颜色
    cluster_colors = {0: 'r', 1: 'yellow', 2: 'b', 3: 'chartreuse', 4: 'purple', 5: '#FFC0CB', 6: '#6A5ACD',
                      7: '#98FB98'}

    # 设置类名
    cluster_names = {0: u'类0', 1: u'类1', 2: u'类2', 3: u'类3', 4: u'类4', 5: u'类5', 6: u'类6', 7: u'类7'}

    clf = KMeans(n_clusters=2)
    s = clf.fit(datas)
    print(clf.labels_)

    fig, ax = plt.subplots(figsize=(8, 5))  # set size

    df = pd.DataFrame(dict(x=x, y=y, label=clf.labels_))
    groups = df.groupby('label')
    ax.margins(0.02)
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=10, label=cluster_names[name],
                color=cluster_colors[name], mec='none')
    plt.show()



