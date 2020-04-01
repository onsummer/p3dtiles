#!/usr/bin/python python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

"""
练习使用二进制的读写和格式
"""

import os, sys, struct

filepath = r"D:\MyCodes\3dtiles\0.bin"

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

if __name__ == '__main__':
    # writetest()
    readtest()