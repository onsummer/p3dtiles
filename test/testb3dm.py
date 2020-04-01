#!/usr/bin/python python3
#-*-coding:utf-8-*-

__author__ = "chenxh"

import os, sys, struct
from p3dtiles.B3dm import B3dmHeader 
from p3dtiles.FileHelper import FileHelper

b3dmfilepath = r"C:\Users\C\Desktop\p3dtiles\assets\b0.b3dm"


if __name__ == '__main__':
    print(FileHelper.filesize(b3dmfilepath, 'KB'))
    with open(b3dmfilepath, 'rb') as binfile:
        b3dmHeader = B3dmHeader(binfile)
        print(b3dmHeader)