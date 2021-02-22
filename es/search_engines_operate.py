# coding=UTF-8
"""
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-19 17:14:35
LastEditTime: 2020-08-25 17:50:47
@Description: 训练annoy文件，不用faiss 是因为faiss不支持float64，最大精度floa32. 
也有利用annoy 检索的功能
"""

from annoy import AnnoyIndex
import faiss
from faiss import normalize_L2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from faq.get_question_vecs import ReadVec2bin

dir_name = os.path.abspath(os.path.dirname(__file__))
read_vec2bin = ReadVec2bin()


class SearchEngine(object):
    def train_annoy(self):
        bert_vecs = read_vec2bin.read_bert_vecs()
        annoy_index_path = os.path.join(dir_name, "./search_model/annoy.index")
        tc_index = AnnoyIndex(f=512, metric="angular")

        if os.path.exists(os.path.join(dir_name, "./search_model")) is False:
            os.mkdir(os.path.join(dir_name, "./search_model"))

        if os.path.exists(annoy_index_path):
            os.remove(annoy_index_path)
            print("删除旧的 annoy.index文件")

        for i, vec in enumerate(bert_vecs):
            tc_index.add_item(i, vec)
        tc_index.build(100)
        tc_index.save(annoy_index_path)
        print("写入 annoy.index文件")

    def train_faiss(self):
        bert_vecs = read_vec2bin.read_bert_vecs()
        d = 512  # dimension
        nb = len(bert_vecs)  # database size
        faiss_index_path = os.path.join(dir_name, "./search_model/faiss.index")
        training_vectors = bert_vecs.astype("float32")
        normalize_L2(training_vectors)
        index = faiss.IndexFlatIP(d)
        index.train(training_vectors)
        index.add(training_vectors)
        if os.path.exists(os.path.join(dir_name, "./search_model")) is False:
            os.mkdir(os.path.join(dir_name, "./search_model"))

        if os.path.exists(faiss_index_path):
            os.remove(faiss_index_path)
            print("删除旧的 faiss.index文件")

        faiss.write_index(index, faiss_index_path)
        print("写入 faiss.index文件")
