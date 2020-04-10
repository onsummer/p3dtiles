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
        self.tableType = header.magic # 指示当前要素表的类型，以便解构ftJSON
        # ftJSON
        ftJSONLength = header.featureTableJSONByteLength
        self.ftJSON = _ftJSON(buffer, 0, ftJSONLength)
        # ftBinary，可能为空
        ftBinaryLength = header.featureTableBinaryByteLength
        self.ftBinary = {}
        self.isBinaryEmpty = None
        if ftBinaryLength == 0:
            self.isBinaryEmpty = True
        else:
            self.ftBinary = _ftBinary(buffer, ftJSONLength, ftJSONLength + ftBinaryLength, self.ftJSON)

    def toDict(self):
        ftBin = {}
        if self.isBinaryEmpty == False:
            ftBin = self.ftBinary.toDict()
        return {
            "FeatureTable.JSON": self.ftJSON.toDict(),
            "FeatureTable.Binary": ftBin
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
        self.rtc_center = FileHelper.hasVal(self.JSON, "RTC_CENTER")
    
    def toDict(self):
        return self.JSON

    def toString(self):
        return self.JSONStr

class _ftBinary:
    '''
    FeatureTable Binary Body；要素表身，还没写完
    '''
    def __init__(self, buffer, fromOffset, toOffset, ftJSON):
        self._ftJSON = ftJSON
        self.binData = buffer[fromOffset: toOffset]

    def parseFtJSON(self, ftJSON):
        for key in ftJSON:
            byteOffset = FileHelper.hasVal(ftJSON[key], "byteOffset")
            componentType = FileHelper.hasVal(ftJSON[key], "componentType")
            if isinstance(componentType, dict) == False:
                # 解析ftBinary
                fmt = str(byteOffset) + 'I'
                # 对于b3dm，只有'BATCH_LENGTH'和'RTC_CENTER'两个
                # https://github.com/CesiumGS/3d-tiles/blob/master/specification/schema/b3dm.featureTable.schema.json
                struct.unpack(fmt, self.binData)
                pass

    def toDict(self):
        '''
        TODO
        '''
        return {}
