#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
from p3dtiles.FileHelper import FileHelper

class B3dmHeader:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.fmt = '4s6I'
        byte = self.file_handle.read(28)
        self.header = struct.unpack(self.fmt, byte)
        self.magic = FileHelper.bin2str(self.header[0])
        self.version = self.header[1]
        self.byteLength = self.header[2]
        self.featureTableJSONByteLength = self.header[3]
        self.featureTableBinaryByteLength = self.header[4]
        self.batchTableJSONByteLength = self.header[5]
        self.batchTableBinaryByteLength = self.header[6]