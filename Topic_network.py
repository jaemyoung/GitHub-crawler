# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:24:50 2022

@author: user
"""
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv("C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/2332.csv")
data["after_topics"] = data["after_topics"].apply(lambda x : " ".join(x)) #리스트 형태
data["after_topics"][0]
#%%

cv = CountVectorizer(max_features=100, stop_words='english')
tdm = cv.fit_transform(data["after_topics"])
words = cv.get_feature_names()

doc = tdm[0].toarray()
[w for w, c in zip(words, doc.flat) if c > 0]
count = tdm.sum(axis=0)
word_count = list(zip(words, count.flat))

#빈도순 정렬
import operator
word_order = sorted(word_count,key=operator.itemgetter(1), reverse=True)

#문서-문서 행렬로 변환 -> 정규화 필요
matrix = tdm*tdm.T
test = matrix.toarray()
tdm.toarray()

""" 키워드 추출 from title """

data['keyword'] = ''
for idx_line in range(len(data)):
    nouns_list = data['after_topics'].loc[idx_line]
    nouns_list_c = [nouns for nouns in nouns_list if len(nouns) > 1]    # 한글자는 이상한게 많아서 2글자 이상
    data.loc[[idx_line], 'keyword'] = set(nouns_list_c)

""" Edge list 작성 """
from collections import Counter

edge_list = []
for keywords_dict in data['after_topics']:
    keywords = list(keywords_dict)
    num_keyword = len(keywords)
    if num_keyword > 0:
        for i in range(num_keyword-1):
            for j in range(i+1, num_keyword):
                edge_list += [tuple(sorted([keywords[i], keywords[j]]))]    # node 간 위해 sorted 사용
edges = list(Counter(edge_list).items())


""" networkx Graph 작성 """
import networkx as nx
G = nx.Graph((x, y, {'weight': v}) for (x, y), v in edges)

""" Community 추출 """
pip install python-louvain
import community as lv
partition = lv.best_partition(G)
nx.set_node_attributes(G, partition, "community") 

""" Gephi file 작성 """
nx.write_gexf(G, 'community.gexf')

total_data["repo.language"].value_counts()[:10]
