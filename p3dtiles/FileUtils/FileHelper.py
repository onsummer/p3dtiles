import os


class FileHelper:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def filesize(path, fmt='B'):
        """ 获取文件大小，默认单位是Bytes

        Args:

            path: 文件全路径

            fmt: 字符串，默认是B，即Bytes。可传入'KB'或'MB'

        """
        size = os.path.getsize(path)
        if (fmt == 'B'):
            return size 
        elif (fmt == 'KB'):
            return size / 1024.0
        elif (fmt == 'MB'):
            return size / (1024.0 * 1024.0)
        else:
            return size
            

    @staticmethod
    def bin2str(bin):
        """ 二进制字符串数据（b'xx'）转换为UTF-8编码的字符串
        """
        return str(bin, 'utf-8')

