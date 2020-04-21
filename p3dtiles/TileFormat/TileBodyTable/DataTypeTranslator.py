#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

'''
枚举一些常见数据类型，并提供转换
'''

def getCTypeFmtStr(pyType:str):
    '''
    传入字符串t，判断它对应的C语言结构体数据类型，并返回python解析字符和比特长度
    '''
    PYTYPE_CTYPE = {
        "CHAR": ("s", 1),
        "UNSIGNED_BYTE": ("B", 1),
        "BYTE": ("b", 1),
        "SHORT": ("h", 2),
        "UNSIGNED_SHORT": ("H", 2),
        "FLOAT": ("f", 4),
        "INT": ("i", 4),
        "UNSIGNED_INT": ("I", 4),
        "DOUBLE": ("d", 8),
    }
    return PYTYPE_CTYPE[pyType.upper()]

def getCmptCount(cmptType:str):
    '''
    传入3dtiles batchtable中batch组件的构成类型字符串cmptType，获取对应的元素个数
    cmptType从BatchTableJSON的每一个batchID的type属性获取，只有"SCALAR"、"VEC2"、"VEC3"、"VEC4"四种类型。
    '''
    CMPT_SCHEMA = {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4
    }
    return CMPT_SCHEMA[cmptType.upper()]


def getPntsPointPropertyDataType(name:str, batchIdCmptType:str):
    POINT_SCHEMA = {
        "POSITION": ("FLOAT", 3),
        "POSITION_QUANTIZED": ("UNSIGNED_SHORT", 3),
        "RGBA": ("UNSIGNED_BYTE", 4),
        "RGB": ("UNSIGNED_BYTE", 3),
        "RGB565": ("UNSIGNED_SHORT", 1),
        "NORMAL": ("FLOAT", 3),
        "NORMAL_OCT16P": ("UNSIGNED_BYTE", 2),
        "BATCH_ID_DEFAULT": ("UNSIGNED_SHORT", 1), # 有问题
        "BATCH_ID_UINT8": ("UNSIGNED_BYTE", 1), # 有问题
        "BATCH_ID_UINT32": ("UNSIGNED_INT", 1) # 有问题
    }
    if name == "BATCH_ID":
        if batchIdCmptType.upper() == "UINT16" or batchIdCmptType == None:
            return POINT_SCHEMA["BATCH_ID_DEFAULT"]
        elif batchIdCmptType.upper() == "UINT8":
            return POINT_SCHEMA["BATCH_ID_UINT8"]
        elif batchIdCmptType.upper() == "UINT32":
            return POINT_SCHEMA["BATCH_ID_UINT32"]
    else:
        return POINT_SCHEMA[name]

def getPntsGlobalPropertyDataType(name:str):
    GLOBAL_SCHEMA = {
        "POINTS_LENGTH": ("UNSIGNED_INT", 1),
        "RTC_CENTER": ("FLOAT", 3),
        "QUANTIZED_VOLUME_OFFSET": ("FLOAT", 3),
        "QUANTIZED_VOLUME_SCALE": ("FLOAT", 3),
        "CONSTANT_RGBA": ("UNSIGNED_BYTE", 4),
        "BATCH_LENGTH": ("UNSIGNED_INT", 1),
    }

    return GLOBAL_SCHEMA[name]
