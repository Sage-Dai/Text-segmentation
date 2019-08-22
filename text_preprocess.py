#!/usr/bin/env python
# -*- coding: utf-8  -*-
import jieba
import codecs
import re
from collections import Counter
from Util import Location


class TextPreprocess:
    """
    文本分词的输入输出
    """

    def text_process(self, source_file, target_file, user_dict):
        text_file = codecs.open(source_file, 'r', encoding='utf-8')
        target = codecs.open(target_file, 'w', encoding='utf-8')

        line_num = 1
        line = text_file.readline()
        while line:
            print('---We are processing', line_num, ' article---.Don''t rush,take it easy!')
            line = self.clean_text(line)
            seg_line = self.cut_words(line, user_dict)
            target.writelines(seg_line + '\n')
            line_num += 1
            line = text_file.readline()
        print('Good job!There are ', line_num, ' lines!')
        text_file.close()
        target.close()

    def text_pre_process_RAM(self, input_data, user_dict, login_diary=None):
        """

        :rtype: List
        """
        if login_diary is not None:
            target = codecs.open(login_diary, 'w', encoding='utf-8')
            line_num = 1

            for i in input_data:
                print('---We are processing', line_num, ' article---.Do not rush,take it easy!')
                line = self.clean_text(i[1])
                seg_line = self.cut_words(line, user_dict)
                target.writelines(seg_line + '\n')
                line_num += 1
            print('Good job!There are ', line_num, ' lines!')
            target.close()
        line_num = 1
        # t_p_p_list = []
        for i in input_data:
            line = self.clean_text(i[1])
            seg_line = self.cut_words(line, user_dict)
            # t_p_p_list.append(seg_line)
            i[1] = seg_line
            line_num += 1
            print('---We are processing', line_num, ' article---.Don''t rush,take it easy!')
        print('Good job!There are ', line_num, ' lines!')
        return input_data

    @staticmethod
    def clean_text(line):
        if line != '':
            line = line.strip()
            # 去除文本中的英文和数字
            line = re.sub("[a-zA-Z0-9]", "", line)
            # 去除文本中的中文符号和英文符号
            line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line)
        return line

    """
    分开词汇
    """

    @staticmethod
    def cut_words(line, user_dict):
        jieba.load_userdict(user_dict)
        seg_list = jieba.cut(line, cut_all=False)
        seg_sentance = ''
        for word in seg_list:
            if word != '\t':
                seg_sentance += word + " "
        return seg_sentance.strip()

    @staticmethod
    def count_freq(source_file, freq_num):
        with codecs.open(source_file, 'r', encoding='utf-8') as f:
            line = f.read()
            word_list = line.replace("\n", "").split(" ")
            word_counter = Counter(word_list)
            sum_num = sum(word_counter.values())
        print(word_counter.most_common(freq_num))
        return word_counter.most_common(freq_num)


if __name__ == "__main__":
     test = TextPreprocess()
     test.text_process("E:/workfile/textrank/data.txt", "E:/workfile/textrank/data_out.txt",'E:/workfile/user.dict' )  
#    lo = Location()
#    input = lo.locate("1", "txt")
#    TextPreprocess.count_freq(input, freq_num=40)
#    a = [[1,2],[3,4]]

