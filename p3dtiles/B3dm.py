#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct, json
from p3dtiles.FileHelper import FileHelper

class B3dm:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        # 读文件头部
        byte = self.file_handle.read(28)
        self.b3dmHeader = B3dmHeader(byte)
        # 读数据体
        byte = self.file_handle.read(self.b3dmHeader.byteLength - 28)
        # b3dmBody = B3dmBody(self.b3dmHeader, byte)

    def toDict(self):
        # TODO
        # 返回元组，包括文件头json[dict类型]，ftJSON，btJSON
        # 考虑返回字符串的二进制要素表和批量表数据
        header_dict = self.b3dmHeader.toDict()
        # ft_dict = self.b3dmBody.toDict()
        # bt_dict = self.b3dmBody.toDict()
        # return (header_dict, ft_dict, bt_dict)
        return (header_dict, )

class B3dmHeader:
    def __init__(self, buffer_data):
        fmt = '4s6I'
        self.header = struct.unpack(fmt, buffer_data)
        # 7个数据
        self.magic = FileHelper.bin2str(self.header[0]) # 常量，'b3dm'
        self.version = self.header[1] # 版本，目前是1
        self.byteLength = self.header[2] # 整个b3dm文件大小包括header和body
        self.featureTableJSONByteLength = self.header[3] # featureTable JSON的大小
        self.featureTableBinaryByteLength = self.header[4] # featureTable 二进制的大小
        self.batchTableJSONByteLength = self.header[5] # batchTable JSON的大小，0为不存在 
        self.batchTableBinaryByteLength = self.header[6] # batchTable 二进制大小，若上面是0这个也是0

    def toDict(self):
        header_dict = {}
        header_dict['magic'] = self.magic
        header_dict['version'] = self.version
        header_dict['byteLength'] = self.byteLength
        header_dict['featureTableJSONByteLength'] = self.featureTableJSONByteLength
        header_dict['featureTableBinaryByteLength'] = self.featureTableBinaryByteLength
        header_dict['batchTableJSONByteLength'] = self.batchTableJSONByteLength
        header_dict['batchTableBinaryByteLength'] = self.batchTableBinaryByteLength
        return header_dict

    def toString(self):
        header_dict = self.toDict()
        header_jsonstr = json.dumps(header_dict)
        return header_jsonstr


class B3dmBody:
    '''
    body = featuretable + batchtable + glb
        featuretable = jsonheader[header.featureTableJSONByteLength] + binbody[header.featureTableBinaryByteLength]
        batchtable = jsonheader[header.batchTableJSONByteLength] + binbody[header.batchTableBinaryByteLength]
    ftJSONHeader根据 'header.featureTableJSONByteLength' + 's'，用unpack解构，然后用str解码成utf-8即可
    btJSONHeader同理
    '''
    def __init__(self, header, buffer_data):
        self.header = header
        fmt = ''
        pass