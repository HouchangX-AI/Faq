# coding=UTF-8
"""
Author: xiaoyichao
LastEditors: xiaoyichao
Date: 2020-08-13 11:34:47
LastEditTime: 2020-08-17 14:37:45
Description: 用于读取excel表格的类
"""
import pymysql


class SqlData(object):
    def __init__(self):
        self.id = 0
        # self.owner_names = ["领域1"]

    def read_QA_data(self):
        """
        Author: xiaoyichao
        param {type} 
        Description: 读取db中的问答数据
        """
        try:
            db = pymysql.connect(
                host="10.20.23.99",
                user="root",
                passwd="jgyhlb1314",
                db="jgy",
                port=3306,
                charset="utf8",
            )
            cursor = db.cursor()
            sql_select_Query = "select * from question_and_answer"
            cursor.execute(sql_select_Query)
            rows = cursor.fetchall()
            res = []
            for row in rows:
                # print("row", row)
                # q_id, ques, ans, owner_name = row[0], row[1], row[3], "领域1"
                q_id, ques, ans = row[0], row[1].strip("\n"), row[3]
                self.id += 1
                res.append([q_id, ques, ans, self.id])
            return res

        except Exception:
            print("Exception")
            return []


# exceldata = SqlData()
# excel_list = exceldata.read_QA_data()
# print(excel_list)
