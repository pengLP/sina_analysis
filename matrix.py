# coding:utf-8


import jieba
import pandas as pd
import codecs
import string
import re

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



if __name__ == '__main__':
    df = pd.read_csv('data/article.csv')
    target = codecs.open('data/cut.txt', 'w', encoding='utf-8')
    for i in df['text']:
        line = clearTxt(i)
        seg_line = sent2word(line)
        target.writelines(seg_line + '\n')

