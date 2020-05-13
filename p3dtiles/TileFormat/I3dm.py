#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable, BatchTable
from . GlTF import glb

class I3dm:
    ''' 3dtiles瓦片数据文件的一种：实例模型类型，即*.i3dm文件
    '''
    def __init__(self, i3dmFile):
        buffer = None
        import _io
        if isinstance(i3dmFile, bytes):
            buffer = i3dmFile
        elif isinstance(i3dmFile, _io.BufferedReader):
            buffer = i3dmFile.read()
        else:
            with open(i3dmFile, 'rb') as fileHandle:
                buffer = fileHandle.read()
        # 读文件头部 和 数据体

        header = struct.unpack('4s7I', buffer[0:32])
        self.header = {
            "magic": 'i3dm',
            "version": header[1],
            "byteLength": header[2],
            "featureTableJSONByteLength": header[3],
            "featureTableBinaryByteLength": header[4],
            "batchTableJSONByteLength": header[5],
            "batchTableBinaryByteLength": header[6],
            "gltfFormat": header[7]
        }
        self.body = I3dmBody(self.header, buffer[32:])

    def toDict(self) -> dict:
        return {
            "I3dm.Header" : self.header,
            "I3dm.Body" : self.body.toDict()
        }

    def getGlb(self, path):
        self.body.glb.save2File(path)

    def getGltf(self, path, mergeBin = False):
        """ 从b3dm中获取gltf部分

            params:
                path: gltf文件的保存路径
                mergeBin: 是否把二进制数据融合至gltf文件内
        """
        self.body.glb.save2GltfFile(path, mergeBin, False)

class I3dmBody:
    '''
    body = featuretable + [batchtable] + glb
        featuretable = jsonheader + [binbody]
        [batchtable] = [jsonheader] + [binbody]
    '''
    def __init__(self, header, bufferData):
        offset = 0
        # ------ FeatureTable
        ftJSONLen = header['featureTableJSONByteLength']
        ftBinLen = header['featureTableBinaryByteLength']
        ftJSONBuffer = bufferData[0:ftJSONLen]
        offset += ftJSONLen + ftBinLen
        ftBinBuffer = bufferData[ftJSONLen:offset]
        self.featureTable = FeatureTable(header['magic'], ftJSONBuffer, ftBinBuffer)

        # ------ BatchTable
        btJSONLen = header['batchTableJSONByteLength']
        btBinLen = header['batchTableBinaryByteLength']
        btJSONBuffer = bufferData[offset:offset + btJSONLen]
        offset += btJSONLen
        btBinBuffer = bufferData[offset:offset+btBinLen]
        self.batchTable = BatchTable(header['magic'], btJSONBuffer, btBinBuffer, self.featureTable.ftJSON)

        # ------ GlTF
        bodySize = header['featureTableJSONByteLength'] + header['featureTableBinaryByteLength'] + header['batchTableJSONByteLength'] + header['batchTableBinaryByteLength']
        self.glbBytes = bufferData[bodySize:]
        self.glb = glb(self.glbBytes)

    def toDict(self) -> dict:
        '''
        以字典形式，返回B3dmBody
        '''
        return {
            "I3dm.Body.FeatureTable": self.featureTable.toDict(),
            "I3dm.Body.BatchTable": self.batchTable.toDict()
        }

    def toString(self) -> str:
        '''
        以字典的字符串形式，返回B3dmBody
        '''
        return json.dumps(self.toDict())