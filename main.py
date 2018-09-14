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
from debugprint import DebugPrint
#********************************

# エントリポイント
def main(args : str):
    # 解析実行
    scraping = BookMeterScraping(args)
    bookInfoList = scraping.execScraping()
    for info in bookInfoList:
        print(info.title)
        print(info.author)
        print(info.registDate)
        print(info.page)
        print(info.id)
        
    pass


# 実行
if __name__ == "__main__":
    DebugPrint.setLogLevel(DebugPrint.LogLevel.Debug)
    args = sys.argv
    main('577685')