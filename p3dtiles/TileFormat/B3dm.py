#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils.FileHelper import FileHelper
from . TileBodyTable.FeatureTable import FeatureTable
from . TileBodyTable.BatchTable import BatchTable
from . GlTF import glb

class B3dm:
    '''
    3dtiles瓦片数据文件的一种：批量模型类型，即*.b3dm文件
    '''
    def __init__(self, b3dmFile):
        buffer = None
        import _io
        if isinstance(b3dmFile, _io.BufferedReader):
            buffer = b3dmFile.read()
        else:
            with open(b3dmFile, 'rb') as file_handle:
                buffer = file_handle.read()
        # 读文件头部
        self.b3dmHeader = B3dmHeader(buffer[0:28])
        # 读数据体
        self.b3dmBody = B3dmBody(self.b3dmHeader, buffer[28:self.b3dmHeader.byteLength])

    def toDict(self):
        return {
            "B3dm.Header" : self.b3dmHeader.toDict(),
            "B3dm.Body" : self.b3dmBody.toDict()
        }

class B3dmHeader:
    '''
    b3dm瓦片的文件头信息, 可使用b3dm的前28字节构造
    '''
    def __init__(self, bufferData:bytes):
        fmt = '4s6I' # b3dm死格式，官方规范没更改请勿改动
        self.header = struct.unpack(fmt, bufferData)
        # 7个数据
        self.magic = 'b3dm' # 常量，'b3dm'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个b3dm文件大小包括header和body
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

class B3dmBody:
    '''
    body = featuretable + [batchtable] + glb
        featuretable = jsonheader + [binbody]
        [batchtable] = [jsonheader] + [binbody]
    '''
    def __init__(self, header:dict, bufferData:bytes):
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

        # ------ GlTF TODO
        bodySize = header.featureTableJSONByteLength + header.featureTableBinaryByteLength + header.batchTableJSONByteLength + header.batchTableBinaryByteLength
        self.glb = glb(bufferData[bodySize:])

    def toDict(self):
        '''
        以字典形式，返回B3dmBody
        '''
        return {
            "B3dm.Body.FeatureTable": self.featureTable.toDict(),
            "B3dm.Body.BatchTable": self.batchTable.toDict(),
            "B3dm.Body.glTF": self.glb.toDict()[0], # 测试性质
            "B3dm.Body.glTF_Bin": self.glb.toDict()[1] # 测试性质
        }

    def toString(self):
        '''
        以字典的字符串形式，返回B3dmBody
        '''
        return json.dumps(self.toDict())
