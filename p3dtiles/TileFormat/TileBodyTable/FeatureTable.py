#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ...FileUtils.FileHelper import FileHelper
import json, struct

class FeatureTable:
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
