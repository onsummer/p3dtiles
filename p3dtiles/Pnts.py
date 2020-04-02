#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
from p3dtiles.FileHelper import FileHelper

class Pnts:
    pass

class PntsHeader:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.fmt = '4s6I'
        byte = self.file_handle.read(28)
        self.header = struct.unpack(self.fmt, byte)
        # 7个数据
        self.magic = FileHelper.bin2str(self.header[0]) # 常量，'PNTS'
        self.version = self.header[1] # 常量，目前是1
        self.byteLength = self.header[2] # header + body的当前pnts文件大小
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0

class PntsBody:
    def __init__(self, file_handle):
        pass