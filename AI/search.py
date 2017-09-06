#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import MeCab
import train
from gensim import models
from gensim.models.doc2vec import LabeledSentence

MODEL_PATH = './doc2vec.model'

def _search_similar_texts(model, words, topn=10):
    x = model.infer_vector(words)
    most_similar_texts = model.docvecs.most_similar([x], topn=topn)
    sim_list = []
    for similar_text in most_similar_texts:
        tmp_sim_list = similar_text[0].split(",")
        tmp_sim_list.append(similar_text[1])
        tmp_sim_list = tuple(tmp_sim_list)
        sim_list.append(tmp_sim_list)
    return sim_list

# 似た文章を探す
def search_similar_docs(wr_text, topn=10):
    '''
    (ドキュメントのパス, 部署名前, 類似度)のタプルのリストを返す
    '''
    w, n = train.split_into_words(search_str)
    words = LabeledSentence(words=w, tags=[n]).words
    model = models.Doc2Vec.load(MODEL_PATH)
    sim_list = _search_similar_texts(model, words, topn=topn)
    return sim_list
    
if __name__ == '__main__':
    pass
#    print("test document: " + INPUT_PATH)
#    search_str = train.read_document(INPUT_PATH)
#    print(train.trim_doc(search_str))
#    print("================\n\n")
#    for path, name, sim in search_similar_docs(search_str):
#        print(path)
#        
#        text, _ = train.trim_doc(train.read_document(path))
#        print(text)
#        print("-------------\n\n")
