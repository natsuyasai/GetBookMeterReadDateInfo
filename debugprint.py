#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
デバッグ用標準出力
"""

# import ************************
import enum
# ********************************

# funcname : str(sys._getframe().f_code.co_name)


class DebugPrint:
    # ログ種別
    class LogLevel(enum.IntEnum):
        Error = 0
        Trace = 1
        Debug = 2

    # ログレベル
    LOG_LEVEL = LogLevel.Error

    def __init__(self):
        """ コンストラクタ
        """
        DebugPrint.LOG_LEVEL = DebugPrint.LogLevel.Error

    # デバッグログ
    @staticmethod
    def DPrint(funcStr: str, logStr: str):
        if DebugPrint.LOG_LEVEL >= DebugPrint.LogLevel.Debug:
            print(funcStr + ' : ' + logStr)

    # エラーログ
    @staticmethod
    def EPrint(funcStr: str, logStr: str):
        if DebugPrint.LOG_LEVEL >= DebugPrint.LogLevel.Error:
            print(funcStr + ' : ' + logStr)

    # トレースログ
    @staticmethod
    def TPrint(funcStr: str):
        if DebugPrint.LOG_LEVEL >= DebugPrint.LogLevel.Trace:
            print(funcStr)

    # ログレベル設定
    @staticmethod
    def setLogLevel(logLevel: LogLevel):
        DebugPrint.LOG_LEVEL = logLevel
            