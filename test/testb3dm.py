#!/usr/bin/python python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

import os, sys, struct
from p3dtiles.B3dm import B3dm 
from p3dtiles.FileHelper import FileHelper

b3dmfilepath = r"D:\MyCodes\p3dtiles\assets\b0.b3dm"

if __name__ == '__main__':
    print(FileHelper.filesize(b3dmfilepath, 'KB'))
    with open(b3dmfilepath, 'rb') as binfile:
        b3dm = B3dm(binfile)
        print(b3dm.b3dmHeader)