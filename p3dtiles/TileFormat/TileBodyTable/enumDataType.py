#!/usr/bin/python3
# -*- coding: UTF-8 -*-

def getCTypeFmtStr(t):
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

def getCmptCount(cmptType):
    cmptType = cmptType.upper()
    if cmptType == "SCALAR":
        return 1
    if cmptType == "VEC2":
        return 2
    if cmptType == "VEC3":
        return 3
    if cmptType == "VEC4":
        return 4