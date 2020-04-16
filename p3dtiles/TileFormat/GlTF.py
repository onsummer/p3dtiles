#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json, os, base64
from ..FileUtils.FileHelper import FileHelper
import _io


class glTF:
    """
    glTF JSON
    """
    def __init__(self, file):
        self.data = None
        if isinstance(file, _io.BufferedReader):
            self.data = json.load(file)
        if isinstance(file, str):
            if os.path.isfile(file):
                self.data = json.load(open(file, 'rb'))
            else:
                self.data = json.loads(file)

class glb:
    """
    读取Binary glTF
    """
    def __init__(self, file):
        if isinstance(file, bytes):
            self.header = glbHeader(file[0:12])
            gltfChunkSize = struct.unpack('I', file[12:16])[0]
            self.gltfChunk = gltfChunk(file[12:12 + 8 + gltfChunkSize])
            # gltfBinaryDataSize = struct.unpack('I', file[12 + 8 + gltfChunkSize:12 + 8 + gltfChunkSize + 4])[0]
            self.gltfBinaryData = gltfBinaryData(file[12 + 8 + gltfChunkSize:], self.header.version)
        if isinstance(file, _io.BufferedReader):
            pass
        if os.path.isfile(file):
            # self.data = open(file, 'rb').read()
            pass
    
    def toDict(self):
        return (self.gltfChunk.chunkData.data, FileHelper.bin2str(self.gltfBinaryData.encodedBinary))

class glbHeader:
    def __init__(self, buffer:bytes):
        self.magic = 'glTF'
        self.version = struct.unpack('I', buffer[4:8])[0]
        self.length = struct.unpack('I', buffer[8:12])[0]

class gltfChunk:
    def __init__(self, buffer:bytes):
        self.chunkDataBytelength = struct.unpack('I', buffer[0:4])[0]
        self.chunkType = struct.unpack('I', buffer[4:8])[0]
        gltfStr = struct.unpack(str(self.chunkDataBytelength) + 's', buffer[8:self.chunkDataBytelength + 8])[0]
        self.chunkData = glTF(FileHelper.bin2str(gltfStr))

class gltfBinaryData:
    def __init__(self, buffer:bytes, version:int):
        self.encodedBinary = None
        
        # 遇到过version是1的glTF
        if version != 2:
            self.encodedBinary = base64.b64encode(buffer)
        else:
            self.length = struct.unpack('I', buffer[0:4])[0]
            self.chunkType = struct.unpack('I', buffer[4:8])[0]
            self.chunkData = buffer[8:8 + self.length]
            self.encodedBinary = base64.b64encode(self.chunkData)
