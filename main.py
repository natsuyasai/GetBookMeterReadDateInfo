#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書メータ読了リスト管理情報取得用
"""


# import*************************
import sys
from bookmeterscraping import BookMeterScraping
from dataanalyzer import DataAnalyzer
# ********************************


# エントリポイント
def main(args: list):
    # データ取得
    # TODO: 1件ずつデータ取得しては解析を実行し、指定した年のみ取得するようにしておきたい
    scraping = BookMeterScraping(args[1])
    bookInfoList = scraping.execScraping()
    # 解析実行
    analyzer = DataAnalyzer(bookInfoList, args[1])
    # csv出力
    analyzer.outputCSV()
    # 月別読書量グラフ表示
    if len(args) >= 3:
        targetYear = args[2]
        analyzer.protBarGraphForMonthReads(targetYear)
    else:
        analyzer.protBarGraphForMonthReads(False)


# 実行
if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print('example: python main.py 12345 2020')
    else:
        main(args)
