# wb_keams
利用微博热点话题舆情聚类分析
### 提前准备的Python模块
本文的实现使用到了多个第三方模块，主要模块如下所示：
1. jieba  使用最广的分词模块
2. pandas 高效处理大型数据集常用的python模块
3. Scikit-learn 用于机器学习的Python工具包
4. Matplotlib 一个python的图形框架，用于绘制二维图形
5. requests 一个常用的Http库，用来发送网络请求
 
### 第一步，爬取微博数据
一个很简单的微博爬虫程序，爬取网站是微博的手机端搜索页面`https://m.weibo.cn/` （选择手机端是因为手机端简单）。代码使用python简单的request包。

首先，对微博页面进行分析，在微博搜索页面随便输入个关键词，然后`F12`进入谷歌浏览器的审查元素界面，点击NetWork，筛选到XHR选项卡，观察页面返回的接口，和`response`返回的json数据。
![微博审查元素界面](https://img-blog.csdnimg.cn/20200215221915669.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)
发现url规律如下：
```markdown
1.https://m.weibo.cn/api/container/getIndex?containerid=100103type情人节&type=all&queryVal=情人节&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=情人节&page=10

https://m.weibo.cn/api/container/getIndex?containerid=100103type情人节&type=all&queryVal=情人节&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=情人节&page=11
```
通过对微博列表的下拉，实现了分页获取微博数据，除了page参数在一直滚动，其他的参数都是固定不变的。由此可以确定访问接口。

#### 接下来分析页面`response`返回的json数据，将数据格式展开如下
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200215223058479.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)
在本项目中，我们只需要提取微博的内容进行特征提取，所以我们只保存微博的部分有用字段
```markdown
data
  id
  cards
    mblog
      id # 唯一标识
      created_at # 发布时间
      text # 正文
```
具体实现代码：
```python
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import time
import os
import csv
import json

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
class SaveCSV(object):

    def save(self, keyword_list,path, item):
        """
        保存csv方法
        :param keyword_list: 保存文件的字段或者说是表头
        :param path: 保存文件路径和名字
        :param item: 要保存的字典对象
        :return:
        """
        try:
            # 第一次打开文件时，第一行写入表头
            if not os.path.exists(path):
                with open(path, "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
                    writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                    writer.writeheader()  # 写表头的方法

            # 接下来追加写入内容
            with open(path, "a", newline='', encoding='utf-8') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
                writer.writerow(item)  # 按行写入数据
                print("^_^ write success")

        except Exception as e:
            print("write error==>", e)
            # 记录错误数据
            with open("error.txt", "w") as f:
                f.write(json.dumps(item) + ",\n")
            pass

def get_page(page,title): #得到页面的请求，params是我们要根据网页填的，就是下图中的Query String里的参数
    params = {
        'containerid': '100103type=1&q='+title,
        'page': page,#page是就是当前处于第几页，是我们要实现翻页必须修改的内容。
        'type':'all',
        'queryVal':title,
        'featurecode':'20000320',
        'luicode':'10000011',
        'lfid':'106003type=1',
        'title':title
    }
    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(page) 
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

# 解析接口返回的json字符串
def parse_page(json , label):
    res = []
    if json:
        items = json.get('data').get('cards')
        for i in items:
            if i == None:
                continue
            item = i.get('mblog')
            if item == None:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['label'] = label
            weibo['text'] = pq(item.get('text')).text().replace(" ", "").replace("\n" , "")
            res.append(weibo)
    return res

if __name__ == '__main__':

    title = input("请输入搜索关键词：")
    path = "article.csv"
    item_list = ['id','text', 'label']
    s = SaveCSV()
    for page in range(10,20):#循环页面
        try:
            time.sleep(1)         #设置睡眠时间，防止被封号
            json = get_page(page , title )
            results = parse_page(json , title)
            if requests == None:
                continue
            for result in results:
                if result == None:
                    continue
                print(result)
                s.save(item_list, path , result)
        except TypeError:
            print("完成")
            continue
```
将最后结果保存在`csv`文件中，保存的微博数据如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200215224128480.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)

### 第二步，微博数据文本处理
对提取到的微博数据，本文采用jieba分词模块对微博正文进行处理，首先将微博中的数字、字母、特殊符号等使用`正则表达式`去掉，然后使用jieba分词模块对微博正文进行分词。
具体代码如下所示：

```python
# 清洗文本
def clearTxt(line:str):
    if(line != ''):
        line = line.strip()
        # 去除文本中的英文和数字
        line = re.sub("[a-zA-Z0-9]", "", line)
        # 去除文本中的中文符号和英文符号
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line)
        return line
    return None

#文本切割
def sent2word(line):
    segList = jieba.cut(line,cut_all=False)
    segSentence = ''
    for word in segList:
        if word != '\t':
            segSentence += word + " "
    return segSentence.strip()
```
处理完成后数据如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200215225122920.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)
### 第三步，特征向量提取，Kmeans聚类
因为Kmeans模型的输入必须是数值向量类型，所以我们需要把每条由词语组成的句子转换成一个数值型向量，在本文中我们使用了`TF-IDF`算法对文档进行了向量化，把所有的数据转换为词频矩阵作为Kmeans模型的输入，TF-IDF最大特征值选择为20000。
实现代码如下：
```python
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
```

词频矩阵形成后，我们直接调用sklearn的Kmeans模型，对所有数据进行聚类。
>Kmeans模型是一种最为典型的无监督学习聚类算法，将数据集中的样本划分为若干个通常是不相交的子集，每个子集称为一个“簇”(cluster)，通过这样的划分，每个簇可能对应于一些潜在的概念或类别。

随后，我们使用matplotlib来绘制聚类结果，并将每类的前五条数据的信息输出，结果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200215230018299.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200215230040473.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2MDA4MzIx,size_16,color_FFFFFF,t_70)
由结果可以看出，聚类结果划分清晰明确，所以可以推断较好的完成了对微博数据的聚类分析。