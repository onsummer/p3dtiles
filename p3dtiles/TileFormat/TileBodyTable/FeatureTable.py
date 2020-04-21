#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

from ...FileUtils import FileHelper
from .DataTypeTranslator import *
import json, struct

class FeatureTable:
    '''
    3dtiles每个tile数据文件的featuretable数据
    '''
    def __init__(self, tableType:str, ftJSONBuffer:bytes, ftBinaryBuffer:bytes):
        self.tableType = tableType
        self.ftJSON = _FtJSON(self.tableType, ftJSONBuffer)
        self.ftBinary = _FtBinary(self.tableType, ftBinaryBuffer, self.ftJSON.toDict())

    def toDict(self) -> dict:
        return {
            "FeatureTable.JSON": self.ftJSON.toDict(),
            "FeatureTable.Binary": self.ftBinary.toDict()
        }

    def toString(self) -> str:
        return json.dumps(self.toDict())

class _FtJSON:
    def __init__(self, tableType:str, bufferData:bytes):
        self.tableType = tableType
        self._ftJSON = json.loads(FileHelper.bin2str(bufferData))
        self.isRefBinaryBody = False
        # 其实不需要获取这些东西，只需要在DataTypeTranslator里进行数据翻译就行
        # 最重要的是获取BatchLength、PointLength、InstanceLength
        if tableType.lower() == 'b3dm':
            self.checkB3dmFtJSON()
        elif tableType.lower() == 'i3dm':
            self.checkI3dmFtJSON()
        elif tableType.lower() == 'pnts':
            self.checkPntsFtJSON()
        else:
            pass
    
    def checkB3dmFtJSON(self):
        '''
        解构b3dm.body.ftJSON
        '''
        self.batchLength = FileHelper.hasVal(self._ftJSON, 'BATCH_LENGTH')
        if self.batchLength == None:
            raise Exception("b3dm.FeatureTable: does not have [BATCH_LENGTH]")

    def checkI3dmFtJSON(self):
        '''
        检测i3dm.body.ftJSON
        '''
        self.instancesLength = FileHelper.hasVal(self._ftJSON, 'INSTANCES_LENGTH')
        if self.instancesLength == None:
            raise Exception("i3dm.FeatureTable: does not have [INSTANCES_LENGTH]")
        
        position = FileHelper.hasVal(self._ftJSON, 'POSITION')
        positionQuantized = FileHelper.hasVal(self._ftJSON, 'POSITION_QUANTIZED')
        if position == None & positionQuantized == None:
            raise Exception("i3dm.FeatureTable: must have one of [POSITION],[POSITION_QUANTIZED]. Now all miss.")
        
        normalUp = FileHelper.hasVal(self._ftJSON, 'NORMAL_UP')
        normalRight = FileHelper.hasVal(self._ftJSON, 'NORMAL_RIGHT')
        if normalUp == None & normalRight == None:
            raise Exception("i3dm.FeatureTable: [NORMAL_UP] & [NORMAL_RIGHT] must all exist.")

        normalUpOct32p = FileHelper.hasVal(self._ftJSON, 'NORMAL_UP_OCT32P')
        normalRightOct32p = FileHelper.hasVal(self._ftJSON, 'NORMAL_RIGHT_OCT32P')
        if normalUpOct32p == None & normalRightOct32p == None:
            raise Exception("i3dm.FeatureTable: [NORMAL_UP_OCT32P] & [NORMAL_RIGHT_OCT32P] must all exist.")

        quantizedVolumeOffset = FileHelper.hasVal(self._ftJSON, 'QUANTIZED_VOLUME_OFFSET')
        quantizedVolumeScale = FileHelper.hasVal(self._ftJSON, 'QUANTIZED_VOLUME_SCALE')
        if positionQuantized != None:
            if quantizedVolumeOffset == None or quantizedVolumeScale == None:
                raise Exception("i3dm.FeatureTable: while [POSITION_QUANTIZED] existed, [QUANTIZED_VOLUME_OFFSET] and [QUANTIZED_VOLUME_SCALE] must all exist, now one of them missed or all missed.")

    def checkPntsFtJSON(self):
        '''
        检测pnts.body.ftJSON
        '''
        self.pointsLength = FileHelper.hasVal(self._ftJSON, 'POINTS_LENGTH')
        if self.pointsLength == None:
            raise Exception("pnts.FeatureTable: must have [POINTS_LENGTH], now miss.")
        
        position = FileHelper.hasVal(self._ftJSON, 'POSITION')
        positionQuantized = FileHelper.hasVal(self._ftJSON, 'POSITION_QUANTIZED')
        if position == None and positionQuantized == None:
            raise Exception("pnts.FeatureTable: [POSITION] and [POSITION_QUANTIZED] must exit one, now all missed.")
        quantizedVolumeOffset = FileHelper.hasVal(self._ftJSON, 'QUANTIZED_VOLUME_OFFSET')
        quantizedVolumeScale = FileHelper.hasVal(self._ftJSON, 'QUANTIZED_VOLUME_SCALE')
        if positionQuantized != None:
            if quantizedVolumeOffset == None or quantizedVolumeScale == None:
                raise Exception("pnts.FeatureTable: while [POSITION_QUANTIZED] exist, [QUANTIZED_VOLUME_OFFSET] and [QUANTIZED_VOLUME_SCALE] must exist.")

        batchId = FileHelper.hasVal(self._ftJSON, 'BATCH_ID')
        batchLength = FileHelper.hasVal(self._ftJSON, 'BATCH_LENGTH')
        if batchId != None:
            if batchLength == None:
                raise Exception("pnts.FeatureTable: while [BATCH_ID] exist, [BATCH_LENGTH] can not be None.")

    def toDict(self) -> dict:
        return self._ftJSON

    def toString(self) -> str:
        return json.dumps(self._ftJSON)

class _FtBinary:
    def __init__(self, tableType:str, bufferData:bytes, ftJSON:dict):
        self.tableType = tableType
        self._buffer = bufferData
        self._ftJSON = ftJSON
        self.data = {}

        if len(bufferData) == 0:
            return

        if tableType == 'b3dm':
            self._itemsCount = ftJSON['BATCH_LENGTH']
            self.buildB3dmFtBinary()
        elif tableType == 'i3dm':
            self._itemsCount = ftJSON['INSTANCES_LENGTH']
            self.buildI3dmFtBinary()
        elif tableType == 'pnts':
            self._itemsCount = ftJSON['POINTS_LENGTH']
            self.buildPntsFtBinary()

    def buildPntsFtBinary(self):
        POINT_SCHEMA_KEYS = ["POSITION", "POSITION_QUANTIZED", "RGBA", "RGB", "RGB565", "NORMAL", "NORMAL_OCT16P", "BATCH_ID"]
        GLOBAL_SCHEMA_KEYS = ["POINTS_LENGTH", "RTC_CENTER", "QUANTIZED_VOLUME_OFFSET", "QUANTIZED_VOLUME_SCALE", "CONSTANT_RGBA", "BATCH_LENGTH"]

        keys = self._ftJSON.keys()
        for key in keys:
            # 点属性，引用ftBinary，进一步解析
            if key in POINT_SCHEMA_KEYS:
                # 需要判断batchId这个有三种值类型的属性
                batchIdCmptType = None
                if key == "BATCH_ID":
                    batchIdCmptType = self._ftJSON[key]["componentType"].upper()
                
                # 获取点要素的类型元数据，即"组件元素值类型, 组件元素个数"
                typeInfo = getPntsPointPropertyDataType(key, batchIdCmptType)
                # 获取"组件元素值类型"对应的类型元数据，即"C语言结构体类型, byte长度"
                fmtInfo = getCTypeFmtStr(typeInfo[0])

                # 拼凑unpack所需的结构字符串 即 {点数 * 组件元素个数)个 C语言结构体类型
                fmtStr = str(self._itemsCount * typeInfo[1]) + fmtInfo[0] 
                
                # 获取buffer对应的切片
                bufferLength = self._itemsCount * typeInfo[1] * fmtInfo[1]
                bufferSub = self._buffer[self._ftJSON[key]["byteOffset"]:self._ftJSON[key]["byteOffset"] + bufferLength]
                
                # 解构成当前key的数据（返回元组）
                dataItem = struct.unpack(fmtStr, bufferSub)
                # 绑定到data上
                self.data[key] = list(dataItem)
            
            # 全局属性，通常直接写在ftJSON里，直接获取
            elif key in GLOBAL_SCHEMA_KEYS:
                self.data[key] = self._ftJSON[key]
            else:
                pass

    def buildI3dmFtBinary(self):
        pass

    def buildB3dmFtBinary(self):
        pass

    def toDict(self) -> dict:
        return self.data