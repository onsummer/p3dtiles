#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

"""
[实验性质]

3dTiles数据规范中测试规范

VectorData瓦片格式属于实验性质，将来极有可能被改动。
"""

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable, BatchTable

class Vctr:
    def __init__(self, vctrFile):
        self.vctrFile = vctrFile
        buffer = None
        import _io
        if isinstance(vctrFile, _io.BufferedReader):
            buffer = vctrFile.read()
        else:
            with open(vctrFile, 'rb') as file_handle:
                buffer = file_handle.read()

        self.b3dmHeader = VctrHeader(buffer[0:44])
        self.b3dmBody = VctrBody(self.b3dmHeader, buffer[44:self.b3dmHeader.byteLength])

class VctrHeader:
    '''
    vctr瓦片的文件头信息, 可使用vctr的前44字节构造
    '''
    def __init__(self, bufferData:bytes):
        fmt = '4s10I' # vctr死格式，官方规范没更改请勿改动
        self.header = struct.unpack(fmt, bufferData)
        self.magic = 'vctr' # 常量，'b3dm'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个b3dm文件大小包括header和body
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小 不能为0
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在 
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0
        self.polygonIndicesByteLength = self.header[7] # 多边形的索引数据长度
        self.polygonPositionsByteLength = self.header[8] # 多边形的坐标数据长度
        self.polylinePositionsByteLength = self.header[9] # 多折线的坐标数据长度
        self.pointPositionsByteLength = self.header[10] # 点坐标数据长度

class VctrBody:
    def __init__(self, header:dict, bufferData:bytes):
        _buffer = bufferData
        offset = 0
        pass
