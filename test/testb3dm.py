#!/usr/bin/python python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

import os, sys, struct
from 3dTileset.B3dm import B3dmHeader

b3dmfilepath = r"D:\MyCodes\3dtiles\assets\b0.b3dm"

"""
4s: 4个b'char，4Bytes，32bit
6I: I: 1个uint32，4Bytes，32bit
"""
fmt_headerFirstPart_20B = '4s6I'
fmt_headerLastPart_8B = ''



if __name__ == '__main__':
    # print(FileHelper.filesize(b3dmfilepath, 'KB'))
    with open(b3dmfilepath, 'rb') as binfile:
        b3dmHeader = B3dmHeader(binfile)
        print(b3dmHeader.magic)