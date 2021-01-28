import sys
import SocialPsy.Analyse.SSA as SSA
import pandas as pd
import jieba.analyse

import jieba
import jieba.posseg
from collections import defaultdict
import os

# 定义无向有权图
class UndirectWeightGraph:
    d = 0.05

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, start, end, weight):  # 添加无向图边
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):  # 根据文本无向图进行单词权重排序，其中包含训练过程
        ws = defaultdict(float)  # pr值列表
        outSum = defaultdict(float)  # 节点出度列表

        ws_init = 1.0 / (len(self.graph) or 1.0)  # pr初始值
        for word, edge_lst in self.graph.items():  # pr, 出度列表初始化
            ws[word] = ws_init
            outSum[word] = sum(edge[2] for edge in edge_lst)

        sorted_keys = sorted(self.graph.keys())
        for x in range(10):  # 多次循环计算达到马尔科夫稳定
            for key in sorted_keys:
                s = 0
                for edge in self.graph[key]:
                    s += edge[2] / outSum[edge[1]] * ws[edge[1]]
                ws[key] = (1 - self.d) + self.d * s

        min_rank, max_rank = 100, 0

        for w in ws.values():  # 归一化权重
            if min_rank > w:
                min_rank = w
            if max_rank < w:
                max_rank = w
        for key, w in ws.items():
            ws[key] = (w - min_rank) * 1.0 / (max_rank - min_rank)

        return ws

class KeywordExtractor(object):  # 加载停用词表
    stop_words = set()

    def set_stop_words(self, stop_word_path):
        if not os.path.isfile(stop_word_path):
            raise Exception("jieba: file does not exit: " + stop_word_path)
        f = open(stop_word_path, "r", encoding="utf-8")
        for lineno, line in enumerate(f):
            self.stop_words.add(line.strip("\n"))
        return self.stop_words


class TextRank(KeywordExtractor):
    def __init__(self, stop_word_path=None):
        self.tokenizer = self.postokenizer = jieba.posseg.dt
        if not stop_word_path:
            stop_word_path = r"tools/stopwords-master/hit_stopwords.txt"
        self.stop_words = KeywordExtractor.set_stop_words(self, stop_word_path=stop_word_path)
        self.pos_filter = frozenset(('nz','v','vd','vn','l','a','d'))
        self.span = 5

    def pairfilter(self, wp):  # wp 格式为 (flag, word)
        state = (wp.flag in self.pos_filter) and (len(wp.word.strip()) >= 2) and (
                    wp.word.lower() not in self.stop_words)
        # print("1:", state)
        return state

    def textrank(self, sentence, topK=20, withWeight=False, allowPOS=('nz','v','vd','vn','l','a','d')):
        self.pos_filt = frozenset(allowPOS)
        g = UndirectWeightGraph()
        word2edge = defaultdict(int)
        words = tuple(self.tokenizer.cut(sentence))
        for i, wp in enumerate(words):  # 将句子转化为边的形式
            # print(wp.flag, wp.word)
            if self.pairfilter(wp):
                for j in range(i + 1, i + self.span):
                    if j >= len(words):
                        break
                    if not self.pairfilter(words[j]):
                        continue
                    word2edge[(wp.word, words[j].word)] += 1

        for terms, w in word2edge.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        if withWeight:
            tags = sorted(nodes_rank.items(), key=lambda x: x[1], reverse=True)
        else:
            tags = sorted(nodes_rank)
        if topK:
            return tags[: topK]
        else:
            tags

result = []
def get_all(cwd):
    get_dir = os.listdir(cwd)
    for i in get_dir:
        sub_dir = os.path.join(cwd, i)
        if os.path.isdir(sub_dir):
            get_all(sub_dir)
        else:
            result.append(sub_dir)

# 处理标题和摘要，提取关键词
def getKeywords_textrank(text,topK):
    extract_tags = TextRank(stop_word_path="tools/stopwords-master/hit_stopwords.txt").textrank
    return (extract_tags(sentence=text, topK=50, withWeight=True))

if __name__ == '__main__':
    text=["","","","","",""]

    path = r'../Data/data/PeopleDaily'
    #result.append('../Data/data/PeopleDaily/20200121/20200121-01-01.txt')
    get_all(path)

    for filename in result:
        data = SSA.read_file(filename)
        data = " ".join(data)

        mon = int(filename[-14:-12])
        text[mon-1]+=data
        print(filename+" success")

    for i in range(len(text)):
        res = getKeywords_textrank(text[i],50)
        for j in res:
            SSA.write_data('result/month_'+str(i+1)+'_.txt', j[0]+' '+str(int(j[1]*1000)) + '\n')
        print("month "+str(i+1)+" success")
