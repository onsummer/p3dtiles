#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json, os, base64
from ..FileUtils import FileHelper
import _io

class gltf:
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
    def __init__(self, bufferData):
        if isinstance(bufferData, bytes):
            self.bytes = bufferData
            self.start(self.bytes)
        elif isinstance(bufferData, _io.BufferedReader):
            self.bytes = bufferData.read()
            self.start(self.bytes)
        elif isinstance(bufferData, str):
            if os.path.isfile(bufferData):
                self.bytes = open(bufferData, 'rb').read()
                self.start(self.bytes)
        else:
            raise Exception('error')
        
    def start(self, bufferData: bytes):
        self.header = glbHeader(bufferData[0:12])
        gltfChunkSize = struct.unpack('I', bufferData[12:16])[0]
        self.gltfChunk = gltfChunk(bufferData[12:12 + 8 + gltfChunkSize])
        # gltfBinaryDataSize = struct.unpack('I', bufferData[12 + 8 + gltfChunkSize:12 + 8 + gltfChunkSize + 4])[0]
        self.gltfBinaryData = gltfBinaryData(bufferData[12 + 8 + gltfChunkSize:], self.header.version)

    def toDict(self) -> dict:
        return (self.gltfChunk.chunkData.data, FileHelper.bin2str(self.gltfBinaryData.encodedBinary))

    def save2File(self, path):
        FileHelper.save2File(path, self.bytes)

    def save2GltfFile(self, path, mergeBin = False, minified = True):
        gltf = self.gltfChunk.chunkData.data # dict
        gltfBinary = self.gltfBinaryData.chunkData # bytes
        if mergeBin:
            gltf['buffers'][0]['uri'] = "data:application/octet-stream;base64," + self.gltfBinaryData.encodedBinary
            FileHelper.save2jsonfile(path, gltf, minified)
        else:
            gltf['buffers'][0]['uri'] = "data.bin"
            import os
            FileHelper.save2jsonfile(path, gltf, minified)
            FileHelper.save2File(os.path.join(os.path.dirname(path), "data.bin"), gltfBinary)

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
        self.chunkData = gltf(FileHelper.bin2str(gltfStr))

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
