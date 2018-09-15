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
    scraping = BookMeterScraping(args)
    bookInfoList = scraping.execScraping()
    # 解析実行
    analyzer = DataAnalyzer(bookInfoList)
    # csv出力
    analyzer.outputCSV()

# 実行
if __name__ == "__main__":
    DebugPrint.setLogLevel(DebugPrint.LogLevel.Debug)
    args = sys.argv
    main('577685')