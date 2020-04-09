#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

from ...FileUtils.FileHelper import FileHelper
import json, struct
from .DataTypeTranslator import *

class BatchTable:
    '''
    3dtiles每个tile数据文件的batchtable数据
    '''
    DEFAULT = {
        "BatchTable.JSON": {},
        "BatchTable.Binary": {}
    }
    def __init__(self, buffer, header, batchLength):
        self.buffer = buffer
        self.tableType = header.magic
        btBinaryLength = header.batchTableBinaryByteLength
        # 计算btJSON起始偏移量
        startOffset = header.featureTableJSONByteLength + header.featureTableBinaryByteLength
        toOffset = startOffset + header.batchTableJSONByteLength

        self.btJSON = {}
        self.btBinary = {}
        self.isBinaryEmpty = True

        if header.batchTableJSONByteLength != 0:
            self.btJSON = _btJSON(self.buffer, startOffset, toOffset)
            if header.batchTableBinaryByteLength != 0:
                self.isBinaryEmpty = False
                self.btBinary = _btBinary(self.buffer, toOffset, toOffset + btBinaryLength, self.btJSON.JSON, batchLength)

    def toDict(self):
        btJSON = self.btJSON
        btBinary = self.btBinary
        if isinstance(self.btJSON, dict) == False:
            btJSON = self.btJSON.toDict()
        if isinstance(self.btBinary, dict) == False:
            btBinary = self.btBinary.toDict()
        return {
            "BatchTable.JSON": btJSON,
            "BatchTable.Binary": btBinary
        }

class _btJSON:
    '''
    BatchTable JSON Header；批量表头
    考虑返回一个{}？
    '''
    def __init__(self, buffer, fromOffset, toOffset):
        self.binJSON = buffer[fromOffset : toOffset]
        self.JSONStr = FileHelper.bin2str(self.binJSON)
        self.JSON = json.loads(self.JSONStr)

    def toDict(self):
        return self.JSON

    def toString(self):
        return self.JSONStr

class _btBinary:
    '''
    BatchTable Binary Body；批量表身，写的不太好，可以优化
    '''
    def __init__(self, buffer, fromOffset, toOffset, btJSON, batchLength):
        self.ls = self.fmtFactory(btJSON, batchLength)
        self.data = self.unpackList(self.ls, buffer[fromOffset: toOffset])

    def fmtFactory(self, btJSON, batchLength):
        ls = []
        for batch_id in btJSON:
            value_type = btJSON[batch_id]["componentType"]
            cmpt_type = btJSON[batch_id]["type"]

            cmpt_count = getCmptCount(cmpt_type)
            fmt_str, bytesize = getCTypeFmtStr(value_type)

            fmt = str(batchLength * cmpt_count) + fmt_str
            offset = batchLength * cmpt_count * bytesize
            ls.append([batch_id, fmt, offset])

        return ls
            
    def unpackList(self, ls, buffer):
        data = {}
        offset = 0
        for batch_cmpt in ls:
            sub_buffer = buffer[offset:offset + batch_cmpt[2]]
            offset = offset + batch_cmpt[2]
            data[batch_cmpt[0]] = (struct.unpack(batch_cmpt[1], sub_buffer))
        return data

    def toDict(self):
        return self.data