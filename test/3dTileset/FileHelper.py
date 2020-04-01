import os

class FileHelper:
    def __init__(self, path):
        self.path = path
    """
    获取文件大小，默认是Bytes
    """
    @staticmethod
    def filesize(path, fmt = 'B'):
        size = os.path.getsize(path) 
        if (fmt == 'B'):
            return size 
        elif (fmt == 'KB'):
            return size / 1024.0
        elif (fmt == 'MB'):
            return size / (1024.0 * 1024.0)
            
    """
    二进制数据转换为UTF-8编码的字符串
    """
    @staticmethod
    def bin2str(bin):
        return str(bin, 'utf-8')

