#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct
from . import B3dm, I3dm, Pnts
from .. FileUtils import FileHelper

class Cmpt:
    ''' 3dtiles瓦片数据文件的一种：复合类型，即*.cmpt文件

        params:
            cmptFile: 可以是open()返回值，也可以是文件路径，也可以是二进制字节变量
    '''
    def __init__(self, cmptFile):
        buffer = None
        import _io
        if isinstance(cmptFile, _io.BufferedReader):
            buffer = cmptFile.read()
        elif isinstance(cmptFile, bytes):
            buffer = cmptFile
        else:
            with open(cmptFile, 'rb') as fileHandle:
                buffer = fileHandle.read()

        header = struct.unpack('4s3I', buffer[0:16])
        self.header = {
            "magic": 'cmpt',
            "version": header[1],
            "byteLength": header[2],
            "tilesLength": header[3]
        }
        self.body = CmptBody(self.header, buffer[16:])

""" Cmpt类型瓦片的数据体
"""
class CmptBody:
    """
        params:
            header: cmpt的文件头
            bufferData: 二进制字节数据
    """
    def __init__(self, header:dict, bufferData:bytes):
        byteOffset = 0
        unparseBufferData = bufferData
        self.tiles = []
        
        for i in range(header["tilesLength"]):
            tile = None
            magic, version, byteLength = struct.unpack('4s2I', unparseBufferData[0:12])

            if magic == 'b3dm':
                tile = B3dm(unparseBufferData[byteOffset : byteOffset + byteLength])
            elif magic == 'i3dm':
                tile = I3dm(unparseBufferData[byteOffset : byteOffset + byteLength])
            elif magic == 'pnts':
                tile = Pnts(unparseBufferData[byteOffset : byteOffset + byteLength])
            else:
                # 还是cmpt，TODO
                pass

            # 解析完一个后，byteOffset和unparseBufferData都要变化
            unparseBufferData = bufferData[byteOffset + byteLength:]
            byteOffset += byteLength
            self.tiles.append(tile)


