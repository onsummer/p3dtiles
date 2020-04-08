#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
from .. FileUtils.FileHelper import FileHelper

class I3dm:
    '''
    3dtiles瓦片数据文件的一种：实例模型类型，即*.i3dm文件
    '''
    def __init__(self):
        pass

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

class I3dmBody:
    def __init__(self, file_handle):
        pass