#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable, BatchTable

class Pnts:
    '''
    3dtiles瓦片数据文件的一种：点云类型，即*.pnts文件
    '''
    def __init__(self, pntsFile):
        buffer = None
        import _io
        if isinstance(pntsFile, bytes):
            buffer = pntsFile
        elif isinstance(pntsFile, _io.BufferedReader):
            buffer = pntsFile.read()
        else:
            with open(pntsFile, 'rb') as file_handle:
                buffer = file_handle.read()

        # 读文件头部、数据体
        header = struct.unpack('4s6I', buffer[0:28])
        self.header = {
            "magic": 'pnts',
            "version": header[1],
            "byteLength": header[2],
            "featureTableJSONByteLength": header[3],
            "featureTableBinaryByteLength": header[4],
            "batchTableJSONByteLength": header[5],
            "batchTableBinaryByteLength": header[6],
        }
        self.body = PntsBody(self.header, buffer[28:])

    def toDict(self) -> dict:
        return {
            "Pnts.Header" : self.header,
            "Pnts.Body" : self.body.toDict()
        }

class PntsBody:
    '''
    body = featuretable + [batchtable]
    '''
    def __init__(self, header, bufferData):
        offset = 0
        # ------ FeatureTable
        ftJSONLen = header['featureTableJSONByteLength']
        ftBinLen = header['featureTableBinaryByteLength']
        ftJSONBuffer = bufferData[0:ftJSONLen]
        offset += ftJSONLen + ftBinLen
        ftBinBuffer = bufferData[ftJSONLen:offset]
        self.featureTable = FeatureTable(header['magic'], ftJSONBuffer, ftBinBuffer)

        # ------ BatchTable
        btJSONLen = header['batchTableJSONByteLength']
        btBinLen = header['batchTableBinaryByteLength']
        btJSONBuffer = bufferData[offset:offset + btJSONLen]
        offset += btJSONLen
        btBinBuffer = bufferData[offset:offset+btBinLen]
        self.batchTable = BatchTable(header['magic'], btJSONBuffer, btBinBuffer, self.featureTable.ftJSON.pointsLength)

    def toDict(self) -> dict:
        '''
        以字典形式，返回PntsBody
        '''
        return {
            "Pnts.Body.FeatureTable": self.featureTable.toDict(),
            "Pnts.Body.BatchTable": self.batchTable.toDict()
        }

    def toString(self) -> str:
        '''
        以字典的字符串形式，返回PntsBody
        '''
        return json.dumps(self.toDict())