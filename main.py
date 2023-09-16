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
    args = sys.argv
    main(args)
