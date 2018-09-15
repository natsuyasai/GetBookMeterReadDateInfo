#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
取得データ解析用
"""


# import ************************
from bookmeterscraping import BookInfo
from typing import List
from debugprint import DebugPrint
#********************************

# const *************************
#********************************


class DataAnalyzer:
    def __init__(self, bookInfoList: List[BookInfo]):
        """ コンストラクタ  
        [I] 解析対象データ
        """
        self.__bookInfoList = bookInfoList


    def outputCSV(self):
        """ csv出力
        """
        with open('result.csv', 'a') as csvFile:
            csvFile.write('タイトル\t著者名\t登録日\tページ数\tID\n')
        for info in self.__bookInfoList:
            csvFile.write(
                info.title + '\t'
                + info.author + '\t' 
                + info.registDate + '\t' 
                + info.page + '\t'
                + info.id + '\n')


# 実行
if __name__ == "__main__":
    pass
