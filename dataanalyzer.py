#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
取得データ解析用
"""


# import ************************
from bookmeterscraping import BookInfo
from typing import List
from debugprint import DebugPrint
import datetime
import sys
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
        dateCntList = self.__createAnalysisAuxiliaryInfo()
        with open('result.csv', 'a', encoding='utf-8_sig') as csvFile:
            csvFile.write('タイトル,著者名,登録日,年月,冊数,ページ数,ID\n')
            for info in self.__bookInfoList:
                key = self.__createYMKey(info.registDate)
                csvFile.write(
                    '"' + info.title + '",'
                    '"'+ info.author + '",' 
                    + info.registDate + ',' 
                    + key + ','
                    + str(dateCntList[key]) + ','
                    + info.page + ','
                    + info.id + '\n')



    def protBarGraph(self):
        """ 棒グラフプロット
        """
        pass
        

    def __createDateCntList(self) -> dict:
        """ 月ごとの冊数カウント
        [O] カウント値
        """
        cntDict = {}
        cnt = 1
        # 前回月
        prvMonth = 0
        # 全てdatetime型に変換し，月ごとにカウントアップしていく
        for info in self.__bookInfoList:
            # 不明の場合は0とする
            if info.registDate == '日付不明':
                cntDict[info.registDate] = 0
                continue
            # datetime形式に変換
            dateInf = datetime.datetime.strptime(info.registDate, '%Y/%m/%d')
            # 月が変わればカウンタをリセットし，前回月を更新する
            if prvMonth != dateInf.month:
                cnt = 1
                prvMonth = dateInf.month
            cntDict[info.registDate] = cnt
            cnt += 1
        return cntDict

    
    def __createAnalysisAuxiliaryInfo(self) -> dict:
        """ 解析補助情報生成
        [O] 解析補助情報
        """
        # 月ごとのカウント値
        dateCntDict = self.__createDateCntList()
        dateCntInfo = {}
        prvMonthCnt = 0
        prvDate = ''
        # 全データから年月ごとの最大値を持った辞書を生成
        for dateStr in dateCntDict:
            # 今回データが前回値以下なら月が切り替わっているためカウント値を登録する
            if prvMonthCnt >= dateCntDict[dateStr]:
                if prvDate != '日付不明' and prvDate != '': # 初回は飛ばす
                    # 日付不明でなければ，年月をキーとして，その月の冊数を保持する
                    key =  self.__createYMKey(prvDate)
                    dateCntInfo[key] = prvMonthCnt
                    DebugPrint.DPrint(str(sys._getframe().f_code.co_name), key)
                else:
                    DebugPrint.DPrint(str(sys._getframe().f_code.co_name), 'None')
            # 今回値を保持
            prvMonthCnt = dateCntDict[dateStr]
            prvDate = dateStr
        dateCntInfo['日付不明'] = 0
        return dateCntInfo


    
    def __createYMKey(self, dateStr: str) -> str:
        """ 年月を組合せたキー用文字列生成
        [I] 日付文字列
        [O] キー文字列
        """
        if dateStr == '日付不明':
            return dateStr
        else:
            date = datetime.datetime.strptime(dateStr, '%Y/%m/%d')
            return str(date.year) + '{:02d}'.format(date.month)




# 実行
if __name__ == "__main__":
    pass
