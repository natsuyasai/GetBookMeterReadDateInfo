#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書メータクローリング用
"""


# import ************************
import requests
import lxml.html

import sys
import time

from debugprint import DebugPrint
# ********************************

# const *************************
# ユーザ読了情報URL
BOOK_METER_USER_URL_BGN = 'https://bookmeter.com/users/'
BOOK_METER_USER_URL_END = '/books/read?page='
# ex)https://bookmeter.com/users/577685/books/read?page=1
REQUEST_RETRY_NUM = 5   # リクエストリトライ回数
REQUEST_WAIT_TIME = 1  # リトライ待ち時間(s)
# ********************************


class BookMeterCrawling:
    def __init__(self, userID: str):
        """ コンストラクタ
        [I] userID ユーザID
        """
        # ユーザID
        self.__userID = userID
        # 最大ページ数
        self.__pageMax = self.__getLastPageNum()

    def execCrawling(self, page: int) -> lxml.html.HtmlElement:
        """ クローリング実行
        [I] page 検索実施ページ番号
        [O] リクエスト結果(lxml.html.HtmlElement)
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        # URL生成
        userURL = BOOK_METER_USER_URL_BGN
        userURL += self.__userID
        userURL += BOOK_METER_USER_URL_END
        userURL += str(page)

        # データ取得
        requestResult = requests.get(userURL, headers=self.__createRequestHeader())
        for reTry in range(0, REQUEST_RETRY_NUM, 1):
            if requestResult.status_code != requests.codes['ok']:
                # 一定時間待ってから再度取得
                # wait
                time.sleep(REQUEST_WAIT_TIME * (reTry + 1))
                # 再実行
                requestResult = requests.get(userURL, headers=self.__createRequestHeader())

        # HTMLパース
        htmlRoot = lxml.html.fromstring(requestResult.content)
        return htmlRoot

    def getPageMax(self) -> int:
        """ 最大ページ数取得
        [O] 最大ページ数
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        return self.__pageMax

    def __createRequestHeader(self) -> dict:
        """ リクエストヘッダ生成
        リクエスト用のヘッダ情報を返す
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        return {'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36'}

    def __getLastPageNum(self) -> int:
        """ 対象ユーザの読了リスト最大ページ数取得
        [O] 最大ページ数
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        # 情報取得
        userURL = BOOK_METER_USER_URL_BGN + self.__userID + BOOK_METER_USER_URL_END + '1'
        requestResult = requests.get(userURL, headers=self.__createRequestHeader())
        # HTMLパース
        htmlRoot = lxml.html.fromstring(requestResult.content)
        # ページ切り替え部取得
        paginationLinkList = htmlRoot.xpath("//a[@class='bm-pagination__link']")
        # '最後'となっている箇所の'href'部から最終ページ番号を取得する
        for paginationLink in paginationLinkList:
            DebugPrint.DPrint(str(sys._getframe().f_code.co_name), paginationLink.text_content().encode('utf-8').decode('utf-8'))
            if (paginationLink.text_content().encode('utf-8').decode('utf-8') == "最後"):
                hrefStr = paginationLink.attrib['href']
                # 最後のhref要素をイコールで分割する.
                # page=xxとなっているため，最終要素がページ番号となる 
                return hrefStr.split('=')[1]
        return 1


# 実行
if __name__ == "__main__":
    DebugPrint.setLogLevel(DebugPrint.LogLevel.Debug)
    crawling = BookMeterCrawling('577685')
    crawling.execCrawling(1)
