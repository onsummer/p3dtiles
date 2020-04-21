#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable
from . TileBodyTable import BatchTable

class I3dm:
    '''
    3dtiles瓦片数据文件的一种：实例模型类型，即*.i3dm文件
    '''
    def __init__(self, i3dmFile):
        buffer = None
        import _io
        if isinstance(i3dmFile, _io.BufferedReader):
            buffer = i3dmFile.read()
        else:
            with open(i3dmFile, 'rb') as file_handle:
                buffer = file_handle.read()
        # 读文件头部
        self.i3dmHeader = I3dmHeader(buffer[0:32])
        # 读数据体
        self.i3dmBody = I3dmBody(self.i3dmHeader, buffer[32:self.i3dmHeader.byteLength])

    def toDict(self):
        return {
            "I3dm.Header" : self.i3dmHeader.toDict(),
            "I3dm.Body" : self.i3dmBody.toDict()
        }

class I3dmHeader:
    '''
    i3dm瓦片的文件头信息, 可使用i3dm的前32字节构造
    '''
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.fmt = '4s7I'
        byte = self.file_handle.read(32)
        self.header = struct.unpack(self.fmt, byte)
        # 8个数据
        self.magic = FileHelper.bin2str(self.header[0]) # 常量，'i3dm'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个i3dm文件大小包括header和body
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0
        self.gltfFormat = self.header[7] # 指示body中gltf的格式，0是uri引用，1是嵌入的glb

    def toDict(self):
        return {
            "magic": self.magic,
            "version": self.version,
            "byteLength": self.byteLength,
            "featureTableJSONByteLength": self.featureTableJSONByteLength,
            "featureTableBinaryByteLength": self.featureTableBinaryByteLength,
            "batchTableJSONByteLength": self.batchTableJSONByteLength,
            "batchTableBinaryByteLength": self.batchTableBinaryByteLength,
            "gltfFormat": self.gltfFormat
        }

    def toString(self):
        header_dict = self.toDict()
        return json.dumps(header_dict)
    

class I3dmBody:
    '''
    body = featuretable + [batchtable] + glb
        featuretable = jsonheader + [binbody]
        [batchtable] = [jsonheader] + [binbody]
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

        # ------ GlTF TODO
        self.glb = None

    def toDict(self):
        '''
        以字典形式，返回B3dmBody
        '''
        return {
            "I3dm.Body.FeatureTable": self.featureTable.toDict(),
            "I3dm.Body.BatchTable": self.batchTable.toDict()
        }

    def toString(self):
        '''
        以字典的字符串形式，返回B3dmBody
        '''
        return json.dumps(self.toDict())