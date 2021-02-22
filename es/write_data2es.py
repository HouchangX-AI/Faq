# coding=UTF-8
"""
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-01-02 16:55:23
LastEditTime: 2020-08-15 16:01:35
@Description: 将数据写到ES中

"""
from es_operate import ESCURD
from elasticsearch import Elasticsearch
from jieba_befaq import StopwordsBEFAQ
import pymysql

# from read_excel import ExcelData
from read_database import SqlData
import os

# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configparser

dir_name = os.path.abspath(os.path.dirname(__file__))
es_config = configparser.ConfigParser()
es_config.read(os.path.join(dir_name, "es.ini"))
es_server_ip_port = es_config["ServerAddress"]["es_server_ip_port"]


alias_name = es_config["ServerInfo"]["alias_name"]
index_name_1 = es_config["ServerInfo"]["index_name_1"]
index_name_2 = es_config["ServerInfo"]["index_name_2"]
index_name_set = set([index_name_1, index_name_2])

if_es_use_passwd = es_config["ServerAddress"]["if_es_use_passwd"]
if if_es_use_passwd == "1":
    http_auth_user_name = es_config["ServerAddress"]["http_auth_user_name"]
    http_auth_password = es_config["ServerAddress"]["http_auth_password"]
    es_connect = Elasticsearch(
        es_server_ip_port, http_auth=(http_auth_user_name, http_auth_password)
    )
else:

    es_connect = Elasticsearch(es_server_ip_port)

es_faq = ESCURD(es_connect)
stopwords4BEFAQ = StopwordsBEFAQ()


class ReadsSqlData2ES(object):
    def __init__(self):
        # self.exceldata = ExcelData()
        # self.excel_list = self.exceldata.read_QA_data()
        self.sqldata = SqlData()
        self.data_lst = self.sqldata.read_QA_data()

    def write_data2es(self, index_name):
        """
        @Author: xiaoyichao
        @param {type}
        @Description: 将数据写到ES中
        """
        actions = []
        num = 0
        for info in self.data_lst:
            num += 1
            q_id, original_question, answer, id = (info[0], info[1], info[2], info[3])

            process_question = original_question.lower()
            process_question = stopwords4BEFAQ.seg_sentence4faq(
                sentence=process_question
            )
            action_name = "action" + str(num)
            action_name = {}
            action_name["_index"] = index_name
            action_name["_source"] = {
                "q_id": q_id,
                "specific_q_id": id,
                "original_question": original_question,
                "process_question": process_question,
                "original_question_cn_middle": original_question.lower(),
                "original_question_cn_left": original_question.lower(),
                "answer": answer,
            }
            actions.append(action_name)
        es_faq.insert_more(index_name=index_name, actions=actions)

        # for sheet_data in self.excel_list:
        #     actions = []
        #     num = 0
        #     for info in sheet_data:
        #         num += 1
        #         q_id, original_question, answer, id, owner_name = (
        #             info[0],
        #             info[1],
        #             info[2],
        #             info[3],
        #             info[4],
        #         )

        #         process_question = original_question.lower()
        #         process_question = stopwords4BEFAQ.seg_sentence4faq(
        #             sentence=process_question
        #         )
        #         action_name = "action" + str(num)
        #         action_name = {}
        #         action_name["_index"] = index_name
        #         action_name["_source"] = {
        #             "q_id": q_id,
        #             "specific_q_id": id,
        #             "original_question": original_question,
        #             "process_question": process_question,
        #             "original_question_cn_middle": original_question.lower(),
        #             "original_question_cn_left": original_question.lower(),
        #             "answer": answer,
        #             "owner_name": owner_name,
        #         }
        #         actions.append(action_name)
        #     es_faq.insert_more(
        #         index_name=index_name, actions=actions, owner_name=owner_name
        #     )


if __name__ == "__main__":
    # es_faq.del_index(index_name="index_faq_1")
    # es_faq.del_index(index_name="index_faq_2")
    # es_faq.del_index(index_name="index_faq")

    read_sql_data = ReadsSqlData2ES()
    current_index = es_faq.es_get_alias(alias_name=alias_name)
    print("current_index", current_index)
    new_index_set = index_name_set - set([current_index])
    new_index = new_index_set.pop()
    print("new_index", new_index)
    es_faq.del_index(index_name=new_index)
    es_faq.create_index(index_name=new_index)
    read_sql_data.write_data2es(index_name=new_index)
    es_faq.es_put_alias(index_name=new_index, alias_name=alias_name)
    es_faq.es_del_alias(index_name=current_index, alias_name=alias_name)
