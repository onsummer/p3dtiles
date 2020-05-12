#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

'''
tileset.json的类描述
'''
import json,os,struct
import math
from .TileFormat import * 
from .FileUtils import FileHelper

# TODO
class Tileset:
    def __init__(self, tilesetFilePath:str):
        buffer = None

        with open(tilesetFilePath, 'rb') as fileHandle:
            buffer = fileHandle.read()
        self.baseUrl = os.path.dirname(tilesetFilePath)
        self.dict = json.loads(FileHelper.bin2str(buffer))

    def toDict(self) -> dict:
        return self.dict

    def toString(self) -> str:
        return json.dumps(self.toDict())

    def setTransform(self, matrix):
        # TODO
        pass

    def buildTileset(self):
        # TODO 遍历children，解析所有的瓦片数据
        root = self.dict['root']
        contentTileFilePath = os.path.join(self.baseUrl, root['uri'])
        with open(contentTileFilePath, 'rb') as fileHandle:
            bufferData = fileHandle.read()
            contentFileType = struct.unpack("4s", bufferData[0:4])
            if contentFileType == 'b3dm':
                tile = B3dm(bufferData)
            elif contentFileType == 'i3dm':
                tile = I3dm(bufferData)
            elif contentFileType == 'pnts':
                tile = Pnts(bufferData)
            elif contentFileType == 'cmpt':
                tile = Cmpt(bufferData)
            elif contentFileType == 'vctr':
                tile = Vctr(bufferData)
            else:
                pass

        while FileHelper.hasVal(root, 'children'):
            # 递归
            # self.buildTileset(root[children]) 
            # for循环children，每一个瓦片先判断是否有children，如果没有就content['uri']，构建瓦片数据
            # 如果有children，再次self.buildTileset(root[children])
            pass

        self.tree = {}
        pass
