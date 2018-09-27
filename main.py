#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書メータ読了リスト管理情報取得用
"""


# import*************************
import sys
from bookmetercrawling import BookMeterCrawling
from bookmeterscraping import BookMeterScraping
from bookmeterscraping import BookInfo
from dataanalyzer import DataAnalyzer
from debugprint import DebugPrint
#********************************

# エントリポイント
def main(args : str):
    # データ取得
    scraping = BookMeterScraping(args[1])
    bookInfoList = scraping.execScraping()
    # 解析実行
    analyzer = DataAnalyzer(bookInfoList, args[1])
    # csv出力
    analyzer.outputCSV()
    # 月別読書量グラフ表示
    analyzer.protBarGraphForMonthReads()

# 実行
if __name__ == "__main__":
    DebugPrint.setLogLevel(DebugPrint.LogLevel.Debug)
    #args = sys.argv
    args = []
    args.append('')
    args.append('916192')
    main(args)