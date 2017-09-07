#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import MeCab
import collections
import re
from gensim import models
from gensim.models.doc2vec import LabeledSentence

INPUT_DOC_DIR = '../staff_wr_copy'
OUTPUT_MODEL = 'doc2vec.model'
PASSING_PRECISION = 93

# 全てのファイルのリストを取得
def get_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.basename(file)
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
    pattern = r"(問題|課題|トラブル|Request)([\s\S]*?)Highlight"
    c = re.compile(pattern, re.IGNORECASE)
    m1 = c.search(extracted_text)
    if m1:    
        tmp_text = m1.group(2)
    else:
        tmp_text = extracted_text

    # メールの件名部分を抽出
    m2 = re.search(r"Subject:([\s\S]*?)(Message|Cc)", extracted_text)     
    if m2:
        tmp_name = m2.group(1)
    else:
        tmp_name = ''

    # 件名部分から日付を取り除く
    tmp_name = re.sub(r'\d{4}.?\d{1,2}.?\d{1,2}.?', '', tmp_name)
    # [***_WR]を取り除く
    tmp_name = re.sub(r'\[.*\]', '', tmp_name)
    # WRを取り除く
    tmp_name = re.sub(r'WR', '', tmp_name)
    # _を空白に置き換える
    tmp_name = re.sub(r'_', ' ', tmp_name)
    # 2つ以上連続した空白を取り除く
    tmp_name = re.sub(r'\s{2,}', '', tmp_name)
    
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
    model = models.Doc2Vec(size=300, alpha=0.0015, window=8, dm=1, sample=1e-6, min_count=1, workers=4)

    model.build_vocab(sentences)
    for x in range(30):
        print(x)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
        ranks = []
       # for doc_id in range(100):
       #     inferred_vector = model.infer_vector(sentences[doc_id].words)
       #     sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
       #     rank = [docid for docid, sim in sims].index(sentences[doc_id].tags[0])
       #     ranks.append(rank)
       # print(collections.Counter(ranks))
       # if collections.Counter(ranks)[0] >= PASSING_PRECISION:
       #     break
    return model

if __name__ == '__main__':
    print("ディレクトリ探索中")
    corpus = list(get_all_files(INPUT_DOC_DIR))
    print("ファイル読み込み中")
    sentences = list(corpus_to_sentences(corpus))
    model = train(sentences)
    model.save(OUTPUT_MODEL)
