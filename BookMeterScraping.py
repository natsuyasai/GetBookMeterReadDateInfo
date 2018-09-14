#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書メータスクレイピング用
"""


# import*************************
import lxml.html
import sys
from typing import List
from BookMeterCrawling import BookMeterCrawling
from DebugPrint import DebugPrint
#********************************

# const *************************
# 本詳細ページURL
BOOK_INFO_URL='https://bookmeter.com/books/'
#********************************

# struct ************************
class BookInfo:
    def __init__(self):
        self.registDate = ''    # 登録日
        self.title = ''         # 本のタイトル
        self.author = ''        # 著者名
        self.page = ''          # ページ数
        self.id = ''

#********************************


class BookMeterScraping:
    def __init__(self, userID: str):
        """ コンストラクタ  
        [I] userID ユーザID  
        """
        # クローリング用
        self.crawler = BookMeterCrawling(userID)


    def execScraping(self) -> List[BookInfo]:
        """ スクレイピング実施  
        [O] スクレイピング結果(list[BookInfo])  
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        # 最大ページ数取得
        maxPage = self.crawler.getPageMax()
        # 全ページ分取得
        htmlPageData:List[lxml.html.HtmlElement] = []
        #for page in range(1, int(maxPage)+1, 1):
        #    htmlPageData.append(self.crawler.execCrawling(page))
        htmlPageData.append(self.crawler.execCrawling(1))

        # 解析実施
        return self.__parseBookInfo(htmlPageData)


    def __parseBookInfo(self, htmlList: List[lxml.html.HtmlElement]) -> List[BookInfo]:
        """ 本情報解析  
        [i] htmlList 全ページ情報
        """
        DebugPrint.TPrint(str(sys._getframe().f_code.co_name))
        bookInfoList:List[BookInfo] = []

        # 全ページ順に解析
        for htmlInfo in htmlList:
            # book__detail取得
            # TODO:1冊分取得したいけど，全要素分取れちゃう・・・
            bookDetailList = htmlInfo.xpath("//div[@class='book__detail']")
            # 一冊分解析
            bookInfoList = self.__parseOnePageBookDetail(bookDetailList[0])
        return bookInfoList


    def __parseOnePageBookDetail(self, bookDetail: lxml.html.HtmlElement) -> List[BookInfo]:
        """ 本情報詳細一冊単位解析  
        [I] bookDetail 本詳細情報  
        [O] 解析結果(BookInfo)
        """
        bookInfoList:List[BookInfo] = []
        # 各種情報取得
        dates = bookDetail.xpath("//div[@class='detail__date']")
        titles = bookDetail.xpath("//div[@class='detail__title']/a")
        authors = bookDetail.xpath("//ul[@class='detail__authors']/li/a")
        pages = bookDetail.xpath("//div[@class='detail__page']")
        for data in range(0, len(titles), 1):
            bookInf = BookInfo()
            bookInf.title = titles[data].text_content().encode("utf-8").decode("utf-8")
            bookInf.id = titles[data].attrib['href'].split('/')[2]
            bookInf.registDate = dates[data].text_content().encode("utf-8").decode("utf-8")
            bookInf.author = authors[data].text_content().encode("utf-8").decode("utf-8")
            bookInf.page = pages[data].text_content().encode("utf-8").decode("utf-8")
            bookInfoList.append(bookInf)
        return bookInfoList
        


# 実行
if __name__ == "__main__":
    DebugPrint.setLogLevel(DebugPrint.LogLevel.Debug)
    scraping = BookMeterScraping('577685')
    scraping.execScraping()
    pass