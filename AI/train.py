#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import MeCab
import collections
import re
from gensim import models
from gensim.models.doc2vec import LabeledSentence

INPUT_DOC_DIR = '../../staff_wr/'
OUTPUT_MODEL = 'doc2vec.model'
PASSING_PRECISION = 93

# 全てのファイルのリストを取得
def get_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.basename(path)
            m = re.match(r'\d+\.mes\.utf', filename)
            if m:
                yield os.path.join(root, file)

# ファイルから文章を返す
def read_document(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

# 青空文庫ファイルから作品部分のみ抜き出す
def trim_doc(doc):
    extracted_text = re.sub(r'(-|=)', '', doc)

    # Request-Highlight間を抽出
    m1 = re.search(r"Request([\s\S]*?)Highlight", extracted_text)
    if m1:
        tmp_text = m1.group(1)
    else:
        tmp_text = extracted_text

    # メールの件名部分を抽出
    m2 = re.search(r"Subject:([\s\S]*?)(Message|Cc)", extracted_text)     
    if m2:
        tmp_name = m2.group(1)
    else:
        tmp_name = ''

    # 件名部分から日付を取り除く(部署＋名前の抽出)
    m3 = re.search(r"\d{4}.?\d{,2}.?\d{,2}.?(.*)-?", tmp_name)  
    if m3:
        tmp_name = m3.group(1)

    # 部署＋名前から空白を取り除く
    tmp_name = re.sub(r'\s', "", tmp_name)     
    
    return (tmp_text, tmp_name)


# 文章から単語に分解して返す
def split_into_words(doc, name=''):
    mecab = MeCab.Tagger("-Ochasen")
    valid_doc, valid_name = trim_doc(doc)
    lines = mecab.parse(valid_doc).splitlines()
    words = []
    for line in lines:
        chunks = line.split('\t')
        if len(chunks) > 3 and (chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
            words.append(chunks[0])
    return (words, name+","+valid_name) #name+valid_name?

# ファイルから単語のリストを取得
def corpus_to_sentences(corpus):
    docs = [read_document(x) for x in corpus]
    for idx, (doc, name) in enumerate(zip(docs, corpus)):
        sys.stdout.write('\r前処理中 {} / {}'.format(idx, len(corpus)))
        words, name = split_into_words(doc, name)
       # name += "testest"
        if len(words) > 0:
            yield LabeledSentence(words=words, tags=[name])

# 学習
def train(sentences):
    model = models.Doc2Vec(size=400, alpha=0.0015, sample=1e-4, min_count=1, workers=4)
    model.build_vocab(sentences)
    for x in range(30):
        print(x)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        ranks = []
        for doc_id in range(100):
            inferred_vector = model.infer_vector(sentences[doc_id].words)
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
            rank = [docid for docid, sim in sims].index(sentences[doc_id].tags[0])
            ranks.append(rank)
        print(collections.Counter(ranks))
        if collections.Counter(ranks)[0] >= PASSING_PRECISION:
            break
    return model

if __name__ == '__main__':
    corpus = list(get_all_files(INPUT_DOC_DIR))
    sentences = list(corpus_to_sentences(corpus))
    print()
    model = train(sentences)
    model.save(OUTPUT_MODEL)
