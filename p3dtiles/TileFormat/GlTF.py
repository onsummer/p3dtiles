#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = "chenxh"

import struct, json
from ..FileUtils.FileHelper import FileHelper

class GlTF:
    """
    专门处理glb的
    """
    def __init__(self, file):
        self.data = None
        if isinstance(file, bin):
            self.data = self.passFromGlb(file)
        if isinstance(file, str):
            self.data = json.load(open(file, 'rb'))

    def passFromGlb(self, glbBuffer):
        return FileHelper.bin2str(glbBuffer)

    def move(self, delta):
        '''
        gltf位置移动
        '''
        pass