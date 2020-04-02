#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
from p3dtiles.FileHelper import FileHelper

class Cmpt:
    pass

class CmptHeader:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.fmt = '4s3I'
        byte = self.file_handle.read(16)
        self.header = struct.unpack(self.fmt, byte)
        # 4个数据
        self.magic = FileHelper.bin2str(self.header[0]) # 应为'CMPT'
        self.version = self.header[1] # 应为1
        self.byteLength = self.header[2] # 整个文件体积，包括header和body
        self.tilesLength = self.header[3] # Composite中tile的数量，位于body

class CmptBody:
    def __init__(self, file_handle):
        pass