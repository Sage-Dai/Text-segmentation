#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
    stopword处理
    :param:source_file: 输入文件的文件名（包含后缀）
           target_file: 输出文件
    :return: 分词后的文本
"""

import codecs
from collections import Counter
from Util import Location


class StopwordProcess:
    def __init__(self):
        # 默认情感词典位置
        self.stopkey_index = 'E:\workfile\de-duplicate\dicts\\'
        self.baidu_stopkey_txt = self.stopkey_index + 'baidu_stopword.txt'
        self.__stopkey = self.__get_stopkey()

    def exclude_word(self, line, stopkey):
        word_list = line.split()
        sentence = ''
        for word in word_list:
            word = word.strip()
            if word not in stopkey:
                if word != '\t':
                    sentence += word + " "
        return sentence.strip()

    def stopword(self, source_file, target_file):
        stopkey = self.__get_stopkey()
        with codecs.open(source_file, 'r', encoding='utf-8') as sourcef, \
                codecs.open(target_file, 'w', encoding='utf-8') as targetf:
            line_num = 1
            line = sourcef.readline()
            while line:
                print("------Processing ", line_num, 'article-----------Do not rush,take it easy')
                sentence = self.exclude_word(line, stopkey)
                targetf.writelines(sentence + '\n')
                line_num += 1
                line = sourcef.readline()
            print('Good job!')

    def stopword_RAM(self, input_data):
        stopkey = self.__get_stopkey()
        line_num = 1
        for i in input_data:
            sentence = self.exclude_word(i[1], stopkey)
            line_num += 1
            print('---We are processing', line_num, ' article---.Don''t rush,take it easy!')
            i[1] = sentence
        print('Good job!There are ', line_num, ' lines!')
        return input_data

    # 计算词频top_num，返回freq_num数值的top词频
    @staticmethod
    def count_freq(source_file, freq_num):
        with codecs.open(source_file, 'r', encoding='utf-8') as f:
            line = f.read()
            word_list = line.replace("\n", "").split(" ")
            word_counter = Counter(word_list)
            sum_num = sum(word_counter.values())
        print(word_counter.most_common(freq_num))
        return word_counter.most_common(freq_num)

    # 获取停用词(默认百度停用词，维护中)
    def __get_stopkey(self, stopkey_txt=r'E:\workfile\de-duplicate\dicts\stopwords\baidu_stopword.txt'):
        stopkey = [w.strip() for w in codecs.open(stopkey_txt, 'r', encoding='utf-8').readlines()]
        return stopkey


if __name__ == "__main__":
#    lo = Location()
#    input = lo.locate("1", "txt")
#    StopwordProcess.count_freq(input, freq_num=40)
    sp = StopwordProcess()
    sp.stopword("E:/workfile/textrank/data_out.txt","E:/workfile/textrank/data_out_out.txt")
