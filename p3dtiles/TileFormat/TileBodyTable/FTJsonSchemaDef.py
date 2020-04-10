#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

'''
要素表头有且仅有的属性类型的定义
属性的值定义，取决于类型定义
'''

# 值定义
FeatureTableSchema = {
    "binaryBodyReference": {

    },
    "globalPropertyScalar": {

    },
    "globalPropertyBoolean": {

    },
    "globalPropertyCartesian3": {

    },
    "globalPropertyCartesian4": {

    },
}

B3dmFTJsonSchema = {
    "BATCH_LENGTH": {
        "type": "globalPropertyScalar",
        "isRequired": True
    },
    "RTC_CENTER": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    }
}

I3dmFTJsonSchema = {
    "POSITION": {
        "type": "binaryBodyReference",
        "isRequired": "!POSITION_QUANTIZED.isRequired"
    },
    "POSITION_QUANTIZED": {
        "type": "binaryBodyReference",
        "isRequired": "!POSITION.isRequired"
    },
    "NORMAL_UP": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "NORMAL_RIGHT": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "NORMAL_UP_OCT32P": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "NORMAL_RIGHT_OCT32P": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "SCALE": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "SCALE_NON_UNIFORM": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "BATCH_ID": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "INSTANCES_LENGTH": {
        "type": "globalPropertyScalar",
        "isRequired": True
    },
    "RTC_CENTER": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "QUANTIZED_VOLUME_OFFSET": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "QUANTIZED_VOLUME_SCALE": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "EAST_NORTH_UP": {
        "type": "globalPropertyBoolean",
        "isRequired": False
    },
}

PntsFTJsonSchema = {
    "POSITION": {
        "type": "binaryBodyReference",
        "isRequired": True
    },
    "POSITION_QUANTIZED": {
        "type": "binaryBodyReference",
        "isRequired": True
    },
    "RGB": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "RGBA": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "RGB565": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "NORMAL": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "NORMAL_OCT16P": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "BATCH_ID": {
        "type": "binaryBodyReference",
        "isRequired": False
    },
    "POINTS_LENGTH": {
        "type": "globalPropertyScalar",
        "isRequired": True
    },
    "RTC_CENTER": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "QUANTIZED_VOLUME_OFFSET": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "QUANTIZED_VOLUME_SCALE": {
        "type": "globalPropertyCartesian3",
        "isRequired": False
    },
    "CONSTANT_RGBA": {
        "type": "globalPropertyCartesian4",
        "isRequired": False
    },
    "BATCH_LENGTH": {
        "type": "globalPropertyCartesian4",
        "isRequired": False
    },
}