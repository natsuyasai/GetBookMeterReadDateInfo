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
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as plotfont
from matplotlib.font_manager import FontProperties
#********************************

# const *************************
# 本詳細ページURL
BOOK_INFO_URL='https://bookmeter.com/books/'
#********************************


class DataAnalyzer:
    def __init__(self, bookInfoList: List[BookInfo], userID: str):
        """ コンストラクタ  
        [I] 解析対象データ
        """
        # 読了本リスト
        self.__bookInfoList = bookInfoList
        # 読了月ごとの冊数
        self.__dateCntDict = self.__createAnalysisAuxiliaryInfo()
        # ユーザID
        self.__userID = userID


    def outputCSV(self):
        """ csv出力
        """
        # 文字列生成
        writeStr = 'タイトル,著者名,登録日,年月,冊数,ページ数,本詳細ページ\n'
        for info in self.__bookInfoList:
            key = self.__createYMKey(info.registDate)
            writeStr +=\
                '"' + info.title + '",'\
                '"'+ info.author + '",' \
                + info.registDate + ',' \
                + key + ','\
                + str(self.__dateCntDict.get(key,0)) + ','\
                + info.page + ','\
                + BOOK_INFO_URL + info.id + '\n'\
        # ファイルへ書き込み
        filename = self.__userID + '.csv'
        with open(filename, 'w', encoding='utf-8_sig') as csvFile:
            csvFile.write(writeStr)



    def protBarGraphForMonthReads(self):
        """ 月別読書量棒グラフプロット
        """
        # dictのkey/valueをそれぞれlistに変換
        bookNumList = []
        dateList = []
        for num in self.__dateCntDict:
            bookNumList.append(self.__dateCntDict[num])
            dateList.append(num)
        # 順番が最新順なので逆順にする
        bookNumList.reverse()
        dateList.reverse()
        # 自分用デバッグコード(初登録時のデータを除外)
        if self.__userID == '577685':
            for i in range(0,3,1):
                del bookNumList[0]
                del dateList[0]

        # リストからnumpyのarrayに変換
        height = numpy.array(bookNumList)
        left = numpy.array(dateList)

        # グラフデータ設定
        filename = self.__userID + '.png'
        self.__createBarGraph(left, height, '年月', '冊数', '月ごとの読書冊数', filename)

    
    def __createBarGraph(self, left: numpy.array, height: numpy.array, xlabel: str, ylabel: str, title:str,  filename: str):
        """ 棒グラフ生成
        [I] left X軸
        [I] height Y軸
        [I] filename ファイル名
        """
        # フォント設定
        import os
        path = os.path.dirname(os.path.abspath(__file__))
        fontprop = FontProperties(fname=path + '/font/NotoSansCJKjp-Medium.otf', size=10)
        # グラフデータ設定
        pyplot.tight_layout()
        sizeX = len(left)*4/10
        sizeY = len(height)*2/10
        pyplot.figure(dpi=100, figsize=(sizeX, sizeY))
        pyplot.title(title, font_properties=fontprop)
        pyplot.xlabel(xlabel, font_properties=fontprop)
        pyplot.ylabel(ylabel, font_properties=fontprop)
        pyplot.bar(x=left, height=height, align='center')
        pyplot.grid(color='gray', linestyle='dotted')
        pyplot.minorticks_on()
        pyplot.xticks(range(len(left)), left,rotation=90)
        pyplot.savefig(filename, format = 'png', dpi=500, bbox_inches='tight')
        #pyplot.show()
         


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
        # 最終データを保持
        key =  self.__createYMKey(prvDate)
        dateCntInfo[key] = prvMonthCnt
        # 日付不明は0とする
        if '日付不明' in dateCntDict:
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
