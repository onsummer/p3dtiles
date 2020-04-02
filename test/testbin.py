#!/usr/bin/python python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

"""
练习使用二进制的读写和格式
"""

import os, sys, struct
import pickle, json
from p3dtiles.FileHelper import FileHelper

filepath = r"D:\MyCodes\p3dtiles\assets\b0.b3dm"

def writetest():
    with open(filepath, 'wb') as binfile:
        a = "hello"
        b = "world!"
        c = 2
        d = 45.123
        byte = struct.pack('5s6sif', bytes(a.encode('utf-8')), bytes(b.encode('utf-8')), c, d)
        binfile.write(byte)

def readtest():
    with open(filepath, 'rb') as binfile:
        byte = binfile.read()
        a, b, c, d = struct.unpack('5s6sif', byte) # 必须满匹配
        print(str(a, 'utf-8'), str(b, 'utf-8'), c, d)

def readbin():
    with open(filepath, 'rb') as binfile:
        byte = binfile.read(28)
        byte = binfile.read(24) # ftJson
        # (featureJSON_Binary, ) = struct.unpack('24s', byte)
        byte = binfile.read(472) # btJson
        (batchJSON_Binary, ) = struct.unpack('472s', byte) # 解译batchJSON为字符串
        print(FileHelper.bin2str(batchJSON_Binary))

if __name__ == '__main__':
    # writetest()
    readbin()