#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

from ...FileUtils.FileHelper import FileHelper
import json, struct

class FeatureTable:
    '''
    3dtiles每个tile数据文件的featuretable数据
    '''
    def __init__(self, tableType, ftJSONBuffer, ftBinaryBuffer):
        self.tableType = tableType
        self.ftJSON = _FtJSON(self.tableType, ftJSONBuffer)
        self.ftBinary = _FtBinary(self.tableType, ftBinaryBuffer, self.ftJSON)

    def toDict(self):
        return {
            "FeatureTable.JSON": self.ftJSON.toDict(),
            "FeatureTable.Binary": self.ftBinary.toDict()
        }

    def toString(self):
        return json.dumps(self.toDict())

class _FtJSON:
    def __init__(self, tableType:str, bufferData:bytes):
        self.tableType = tableType
        self.ftJSON = json.loads(FileHelper.bin2str(bufferData))
        self.isRefBinaryBody = False
        if tableType.lower() == 'b3dm':
            self.buildB3dmJSON()
        elif tableType.lower() == 'i3dm':
            self.buildI3dmJSON()
        elif tableType.lower() == 'pnts':
            self.buildPntsJSON()
        else:
            pass
    
    def buildB3dmJSON(self):
        '''
        解构b3dm.body.ftJSON
        '''
        self.batchLength = FileHelper.hasVal(self.ftJSON, 'BATCH_LENGTH')
        if self.batchLength == None:
            raise Exception("b3dm.FeatureTable: does not have [BATCH_LENGTH]")
        self.rtcCenter = FileHelper.hasVal(self.ftJSON, 'RTC_CENTER')
        self.extensions = FileHelper.hasVal(self.ftJSON, 'extensions')
        self.extras = FileHelper.hasVal(self.ftJSON, 'extras')
        # self.required = ['batchLength']

    def buildI3dmJSON(self):
        '''
        解构i3dm.body.ftJSON
        '''
        self.instancesLength = FileHelper.hasVal(self.ftJSON, 'INSTANCES_LENGTH')
        if self.instancesLength == None:
            raise Exception("i3dm.FeatureTable: does not have [INSTANCES_LENGTH]")
        
        self.position = FileHelper.hasVal(self.ftJSON, 'POSITION')
        self.positionQuantized = FileHelper.hasVal(self.ftJSON, 'POSITION_QUANTIZED')
        if self.position == None & self.positionQuantized == None:
            raise Exception("i3dm.FeatureTable: must have one of [POSITION],[POSITION_QUANTIZED]. Now all miss.")
        
        self.normalUp = FileHelper.hasVal(self.ftJSON, 'NORMAL_UP')
        self.normalRight = FileHelper.hasVal(self.ftJSON, 'NORMAL_RIGHT')
        if self.normalUp == None & self.normalRight == None:
            raise Exception("i3dm.FeatureTable: [NORMAL_UP] & [NORMAL_RIGHT] must all exist.")

        self.normalUpOct32p = FileHelper.hasVal(self.ftJSON, 'NORMAL_UP_OCT32P')
        self.normalRightOct32p = FileHelper.hasVal(self.ftJSON, 'NORMAL_RIGHT_OCT32P')
        if self.normalUpOct32p == None & self.normalRightOct32p == None:
            raise Exception("i3dm.FeatureTable: [NORMAL_UP_OCT32P] & [NORMAL_RIGHT_OCT32P] must all exist.")

        self.scale = FileHelper.hasVal(self.ftJSON, 'SCALE')
        self.scaleNonUniform = FileHelper.hasVal(self.ftJSON, 'SCALE_NON_UNIFORM')
        self.batchId = FileHelper.hasVal(self.ftJSON, 'BATCH_ID')
        self.rtcCenter = FileHelper.hasVal(self.ftJSON, 'RTC_CENTER')
        
        self.quantizedVolumeOffset = FileHelper.hasVal(self.ftJSON, 'QUANTIZED_VOLUME_OFFSET')
        self.quantizedVolumeScale = FileHelper.hasVal(self.ftJSON, 'QUANTIZED_VOLUME_SCALE')
        if self.positionQuantized != None:
            if self.quantizedVolumeOffset == None or self.quantizedVolumeScale == None:
                raise Exception("i3dm.FeatureTable: while [POSITION_QUANTIZED] existed, [QUANTIZED_VOLUME_OFFSET] and [QUANTIZED_VOLUME_SCALE] must all exist, now one of them missed or all missed.")

        self.eastNorthUp = FileHelper.hasVal(self.ftJSON, 'EAST_NORTH_UP')
        self.extensions = FileHelper.hasVal(self.ftJSON, 'extensions')
        self.extras = FileHelper.hasVal(self.ftJSON, 'extras')

    def buildPntsJSON(self):
        '''
        解构pnts.body.ftJSON
        '''
        self.pointsLength = FileHelper.hasVal(self.ftJSON, 'POINTS_LENGTH')
        if self.pointsLength == None:
            raise Exception("pnts.FeatureTable: must have [POINTS_LENGTH], now miss.")
        
        self.position = FileHelper.hasVal(self.ftJSON, 'POSITION')
        self.positionQuantized = FileHelper.hasVal(self.ftJSON, 'POSITION_QUANTIZED')
        self.quantizedVolumeOffset = FileHelper.hasVal(self.ftJSON, 'QUANTIZED_VOLUME_OFFSET')
        self.quantizedVolumeScale = FileHelper.hasVal(self.ftJSON, 'QUANTIZED_VOLUME_SCALE')
        if self.positionQuantized != None:
            if self.quantizedVolumeOffset == None or self.quantizedVolumeScale == None:
                raise Exception("pnts.FeatureTable: while [POSITION_QUANTIZED] exist, [QUANTIZED_VOLUME_OFFSET] and [QUANTIZED_VOLUME_SCALE] must exist.")

        self.RGBA = FileHelper.hasVal(self.ftJSON, 'RGBA')
        self.RGB = FileHelper.hasVal(self.ftJSON, 'RGB')
        self.RGB565 = FileHelper.hasVal(self.ftJSON, 'RGB565')
        self.normal = FileHelper.hasVal(self.ftJSON, 'NORMAL')
        self.normalOct16p = FileHelper.hasVal(self.ftJSON, 'NORMAL_OCT16P')
        self.batchId = FileHelper.hasVal(self.ftJSON, 'BATCH_ID')
        self.rtcCenter = FileHelper.hasVal(self.ftJSON, 'RTC_CENTER')
        self.constantRGBA = FileHelper.hasVal(self.ftJSON, 'CONSTANT_RGBA')
        self.batchLength = FileHelper.hasVal(self.ftJSON, 'BATCH_LENGTH')
        if self.batchId != None:
            if self.batchLength == None:
                raise Exception("pnts.FeatureTable: while [BATCH_ID] exist, [BATCH_LENGTH] can not be None.")
        self.extensions = FileHelper.hasVal(self.ftJSON, 'extensions')
        self.extras = FileHelper.hasVal(self.ftJSON, 'extras')

    def toDict(self):
        return self.ftJSON

    def toString(self):
        return json.dumps(self.ftJSON)

class _FtBinary:
    def __init__(self, tableType:str, bufferData:bytes, ftJSON:dict):
      self.tableType = tableType
      self.data = None
      if len(bufferData) == 0:
          self.data = {}
      else:
          # 若二进制缓存不为0，那么就要根据ftJSON构造了
          # TODO
          self.data = {}

    def toDict(self):
        return self.data