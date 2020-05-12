#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

""" [实验性质]3dTiles数据规范中测试规范
VectorData瓦片格式属于实验性质，将来极有可能被改动。

"""

import struct, json
from .. FileUtils import FileHelper
from . TileBodyTable import FeatureTable, BatchTable

class Vctr:
    ''' 3dtiles瓦片数据文件的一种：矢量数据类型，即*.vctr文件
    '''
    def __init__(self, vctrFile):
        buffer = None
        import _io
        if isinstance(vctrFile, bytes):
            buffer = vctrFile
        elif isinstance(vctrFile, _io.BufferedReader):
            buffer = vctrFile.read()
        else:
            with open(vctrFile, 'rb') as fileHandle:
                buffer = fileHandle.read()

        header = struct.unpack('4s10I', buffer[0:44])
        self.header = {
            "magic": 'vctr',
            "version": header[1],
            "byteLength": header[2],
            "featureTableJSONByteLength": header[3],
            "featureTableBinaryByteLength": header[4],
            "batchTableJSONByteLength": header[5],
            "batchTableBinaryByteLength": header[6],
            "polygonIndicesByteLength": header[7],
            "polygonPositionsByteLength": header[8],
            "polylinePositionsByteLength": header[9],
            "pointPositionsByteLength": header[10],
        }
        self.body = VctrBody(self.header, buffer[44:self.header["byteLength"]])
    
    def toDict(self) -> dict:
        return {
            "Vctr.Header" : self.header,
            "Vctr.Body" : self.body.toDict()
        }
        
class VctrBody:
    # TODO
    def __init__(self, header:dict, bufferData:bytes):
        _buffer = bufferData
        offset = 0
        pass
    
    def toDict(self) -> dict:
        '''
        以字典形式，返回VctrBody
        '''
        b3dmDict = {}
        return b3dmDict