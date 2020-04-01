#!/usr/bin/python
# -*- coding: UTF-8 -*-

import struct
import FileHelper

class B3dmHeader:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.fmt = '4s6I'
        byte = self.file_handle.read(28)
        self.header = struct.unpack(self.fmt, byte)
        self.magic = FileHelper.bin2str(self.header[0])
        self.version = self.header[0]
        self.byteLength = self.header[0]
        self.featureTableJSONByteLength = self.header[0]
        self.featureTableBinaryByteLength = self.header[0]
        self.batchTableJSONByteLength = self.header[0]
        self.batchTableBinaryByteLength = self.header[0]