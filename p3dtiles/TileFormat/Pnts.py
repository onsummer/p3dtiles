#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable
from . TileBodyTable import BatchTable

class Pnts:
    '''
    3dtiles瓦片数据文件的一种：点云类型，即*.pnts文件
    '''
    def __init__(self, pntsFile):
        buffer = None
        import _io
        if isinstance(pntsFile, _io.BufferedReader):
            buffer = pntsFile.read()
        else:
            with open(pntsFile, 'rb') as file_handle:
                buffer = file_handle.read()

        # 读文件头部
        self.pntsHeader = PntsHeader(buffer[0:28])
        bodySize = self.pntsHeader.featureTableJSONByteLength + self.pntsHeader.featureTableBinaryByteLength + self.pntsHeader.batchTableJSONByteLength + self.pntsHeader.batchTableBinaryByteLength
        # 读数据体
        self.pntsBody = PntsBody(self.pntsHeader, buffer[28:28 + bodySize])

    def toDict(self):
        return {
            "I3dm.Header" : self.pntsHeader.toDict(),
            "I3dm.Body" : self.pntsBody.toDict()
        }

class PntsHeader:
    '''
    pnts瓦片的文件头信息, 可使用pnts的前28字节构造
    '''
    def __init__(self, bufferData:bytes):
        self.fmt = '4s6I'
        self.header = struct.unpack(self.fmt, bufferData)
        # 7个数据
        self.magic = FileHelper.bin2str(self.header[0]) # 常量，'pnts'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个i3dm文件大小包括header和body
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0

    def toDict(self):
        return {
            "magic": self.magic,
            "version": self.version,
            "byteLength": self.byteLength,
            "featureTableJSONByteLength": self.featureTableJSONByteLength,
            "featureTableBinaryByteLength": self.featureTableBinaryByteLength,
            "batchTableJSONByteLength": self.batchTableJSONByteLength,
            "batchTableBinaryByteLength": self.batchTableBinaryByteLength
        }

    def toString(self):
        header_dict = self.toDict()
        return json.dumps(header_dict)
    

class PntsBody:
    '''
    body = featuretable + [batchtable]
    '''
    def __init__(self, header, bufferData):
        _buffer = bufferData
        offset = 0
        # ------ FeatureTable
        ftJSONLen = header.featureTableJSONByteLength
        ftBinLen = header.featureTableBinaryByteLength
        ftJSONBuffer = bufferData[0:ftJSONLen]
        offset += ftJSONLen + ftBinLen
        ftBinBuffer = bufferData[ftJSONLen:offset]
        self.featureTable = FeatureTable(header.magic, ftJSONBuffer, ftBinBuffer)

        # ------ BatchTable
        btJSONLen = header.batchTableJSONByteLength
        btBinLen = header.batchTableBinaryByteLength
        btJSONBuffer = bufferData[offset:offset + btJSONLen]
        offset += btJSONLen
        btBinBuffer = bufferData[offset:offset+btBinLen]
        self.batchTable = BatchTable(header.magic, btJSONBuffer, btBinBuffer, self.featureTable.ftJSON.batchLength)

    def toDict(self):
        '''
        以字典形式，返回PntsBody
        '''
        return {
            "Pnts.Body.FeatureTable": self.featureTable.toDict(),
            "Pnts.Body.BatchTable": self.batchTable.toDict()
        }

    def toString(self):
        '''
        以字典的字符串形式，返回PntsBody
        '''
        return json.dumps(self.toDict())