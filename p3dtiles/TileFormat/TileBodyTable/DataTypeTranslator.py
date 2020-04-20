#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

'''
枚举一些常见数据类型，并提供转换
'''

def getCTypeFmtStr(t:str):
    '''
    传入字符串t，判断它对应的C语言结构体数据类型，并返回python解析字符和比特长度
    '''
    t = t.upper()
    if t == "CHAR":
        return ("s",1)
    if t == "SHORT":
        return ("h",2)
    if t == "UNSIGNED_SHORT":
        return ("H",2)
    if t == "FLOAT":
        return ("f",4)
    if t == "INT":
        return ("i",4)
    if t == "UNSIGNED_INT":
        return ("I",4)
    if t == "DOUBLE":
        return ("d",8)

def getCmptCount(cmptType:str):
    '''
    传入3dtiles batchtable中batch组件的构成类型字符串cmptType，获取对应的元素个数
    cmptType从BatchTableJSON的每一个batchID的type属性获取，只有"SCALAR"、"VEC2"、"VEC3"、"VEC4"四种类型。
    '''
    cmptType = cmptType.upper()
    element_count = None
    if cmptType == "SCALAR":
        element_count = 1
    if cmptType == "VEC2":
        element_count = 2
    if cmptType == "VEC3":
        element_count = 3
    if cmptType == "VEC4":
        element_count = 4

    return element_count