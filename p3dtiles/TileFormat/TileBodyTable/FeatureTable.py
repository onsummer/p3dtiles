#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

from ...FileUtils.FileHelper import FileHelper
import json, struct

class FeatureTable:
    '''
    3dtiles每个tile数据文件的featuretable数据
    '''
    def __init__(self, buffer, header):
        self.buffer = buffer
        ftJSONLength = header.featureTableJSONByteLength
        ftBinaryLength = header.featureTableJSONByteLength
        self.ftJSON = _ftJSON(buffer, 0, ftJSONLength)
        self.ftBinary = _ftBinary(buffer, ftJSONLength, ftJSONLength + ftBinaryLength, self.ftJSON)

    def toDict(self):
        return {
            "FeatureTable.JSON": self.ftJSON.toDict(),
            "FeatureTable.Binary": self.ftBinary.toDict()
        }

    def toString(self):
        return json.dumps(self.toDict())

class _ftJSON:
    '''
    FeatureTable JSON Header；要素表头
    '''
    def __init__(self, buffer, fromOffset, toOffset):
        self.binJSON = buffer[fromOffset:toOffset]
        self.JSONStr = FileHelper.bin2str(self.binJSON)
        self.JSON = json.loads(self.JSONStr)
        self.batch_length = FileHelper.hasVal(self.JSON, "BATCH_LENGTH")
    
    def toDict(self):
        return self.JSON

    def toString(self):
        return self.JSONStr

class _ftBinary:
    '''
    FeatureTable Binary Body；要素表身
    '''
    def __init__(self, buffer, fromOffset, toOffset, ftJSON):
        if fromOffset == toOffset:
            self.binData = None
        self.binData = buffer[fromOffset: toOffset]

    def toDict(self):
        if self.binData == None:
            return {}
        else:
            '''
            TODO
            '''
            return {
                "INFO": "COMMING SOON"
            }
