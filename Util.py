#!/usr/bin/env python
# -*- coding: utf-8  -*-

#
# 路径，时间，数据库存取公用方法
#
import datetime
import os
import xlrd
import wrapt
import pymysql


class PathMixin:
    def __init__(self):
        self.__root = os.getcwd()
        self.__date = str(datetime.datetime.now())[:10]

    def makedir(self, date):
        pass


class TransportDb:
    def __init__(self):
        self.default_conn = {'host': '192.168.1.47',
                             'port': 3306,
                             'db': 'biods_cmp',
                             'user': 'root',
                             'passwd': 'root123',
                             'charset': 'utf8',
                             'use_unicode': True
                             }
        self.cursor = ''
        self.connect = ''
        self.que_data = ()
        self.db_connect()

    def db_connect(self, param_dict={}):
        """
        功能：连接数据库
        :param param_dict: 参数字典(可给默认值)
        :return: none
        """
        if param_dict == {}:
            self.connect = pymysql.connect(
                host=self.default_conn['host'],  # 数据库地址
                port=self.default_conn['port'],  # 数据库端口
                db=self.default_conn['db'],  # 数据库名
                user=self.default_conn['user'],  # 数据库用户名
                passwd=self.default_conn['passwd'],  # 数据库密码
                charset=self.default_conn['charset'],  # 编码方式
                use_unicode=self.default_conn['use_unicode']
            )
        else:
            self.connect = pymysql.connect(
                host=param_dict['host'],  # 数据库地址
                port=param_dict['port'],  # 数据库端口
                db=param_dict['db'],  # 数据库名
                user=param_dict['user'],  # 数据库用户名
                passwd=param_dict['passwd'],  # 数据库密码
                charset=param_dict['charset'],  # 编码方式
                use_unicode=param_dict['use_unicode']
            )
        self.cursor = self.connect.cursor()

    def query_data(self, sql):
        """
        功能：从数据库中获取数据
        :param sql: sql语句
        :return: 数据列表
        """
        self.cursor.execute(sql)
        self.que_data = self.cursor.fetchall()
        return self.que_data

    def format_data(self):
        pass

    @staticmethod
    def data_to_txt(query_data, doc_name):
        """
        功能：将数据库中的数据写入doc_name.txt(包含path)
        :param doc_name:
        :param query_data:
        """
        with open(doc_name, 'w', encoding='utf-8') as f:
            f.write("\n".join(
                str(i).replace('<br/>', ' ').strip().replace('\r', '').replace('\t', '').replace('\n', '') for i in
                query_data))
        print("Write to txt successfully!")

    def store_data(self, sql):
        """
        新闻数据存入mysql数据库
        :return: None
        """
        # print(sql)
        self.cursor.execute(sql)
        # 提交sql语句
        self.connect.commit()

    # 获取数据字典
    def get_data_dict(self):
        """
        :return: data_dict（字典列表）
        """
        data_key = [i[0] for i in self.que_data]
        data_value = [str(i[1]) + str(i[2]) for i in self.que_data]
        data_dict = []
        for i in range(len(self.que_data)):
            data_dict_one = {data_key[i]: data_value[i]}
            data_dict.append(data_dict_one)
        return data_value, data_dict


# 从excel中按title和全文分别取数据，存为txt
def transfer(source_file, sheetname, target_file, category='title'):
    excel_file = xlrd.open_workbook(source_file)
    title_sheet = excel_file.sheet_by_name(sheetname)
    rows = title_sheet.nrows
    row_data = []

    # 判断是读文章标题还是读文章标题和文章内容的合集
    if category == 'title':
        for i in range(rows):
            lines = title_sheet.row_values(i)
            row_data.append(lines[0].replace("\n", "").replace("<br/>", ""))
        #           row_data = lines[0]
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(row_data))
    else:
        for i in range(rows):
            lines = title_sheet.row_values(i)
            row_data.append("".join(lines[3:5]).replace("\n", "").replace("<br/>", ""))
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(row_data))


# 精确定位文件
class Location:
    def __init__(self):
        self.root_path = ''
        self._ = ''
        self.set_root()
        self._path_list = []
        self._doc_path_list = []
        self.get_path_list()



    # 定义根路径
    def set_root(self, root_path='G:\snowNLP\SentimentAnalysis'):
        """
        :type root_path: object
        """
        self.root_path = root_path

    # TODO: 传入项目目录，进行检索，方式：传入pattern，通过盘符或者其他方式
    def get_path_list(self):
        # 项目主路径
        # self.root_path = 'G:\snowNLP\SentimentAnalysis'
        for root, dirs, files in os.walk(self.root_path):
            for dir in dirs:
                self._path_list.append(os.path.join(root, dir))
            for file in files:
                self._doc_path_list.append(os.path.join(root, file))
        # print(self._path_list, '__________________\n', self._doc_path_list)

    # TODO 不够robust
    def locate(self, doc_name, formation):
        doc_str = doc_name + '.' + formation
        count = 0
        for _ in self._doc_path_list:
            if doc_str in _:
                return _
            elif count == len(self._path_list):
                print("There are something wrong with locate Path! Go check it.")


    # TODO 不够robust
    def find_path(self, path_name):
        count = 0
        for _ in self._path_list:
            if path_name in _:
                self._ = _
                count += 1
                return _
            elif count == len(self._path_list):
                print("There are something wrong with locate Path! Go check it.")



    # 验证遍历目录是否正确
    def print_list(self):
        for i in self._path_list:
            print('\n')
            print(i)


if __name__ == "__main__":
    # db = TransportDb()
    # get_sql = "select V_NEWS_ENC, V_NEWS_TIT, T_NEWS_TEXT from o_news where  left(V_TIME ,10) = '2019-07-01' and " \
    #           "V_SRC_PLF_NM = " \
    #           "'第一财经' "
    # data = db.query_data(get_sql)
    # print(type(data), data)
    a = 1
    b = 2
    c = 3
    a_list = [a, b, c]
    print(a_list)