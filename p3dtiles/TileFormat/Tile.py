#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct
from .. FileUtils import FileHelper

class Tile:
    def __init__(self, tileFile):
        buffer = None
        import _io
        if isinstance(tileFile, _io.BufferedReader):
            buffer = tileFile.read()
        elif isinstance(tileFile, bytes):
            buffer = tileFile
        else:
            with open(tileFile, 'rb') as fileHandle:
                buffer = fileHandle.read()
