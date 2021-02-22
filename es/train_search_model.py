# coding=UTF-8
"""
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-19 17:14:35
LastEditTime: 2020-08-25 18:05:41
@Description: 
"""
# from read_excel import ExcelData
import os
import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search_engines_operate import SearchEngine

# from read_database import SqlData

# sqldata = SqlData()
search_engine = SearchEngine()

search_engine.train_annoy()
search_engine.train_faiss()
