# p3dtiles
3dtiles sdk. Implement using python3.

3dtiles 开发工具。使用python实现，当前暂无依赖库。

## test目录
作者测试用目录，仅供参考

## test/testData目录
测试用数据

# Usage/用法

## Load a tile file from given path/从路径读取瓦片

``` python
from p3dtiles.TileFormat.B3dm import B3dm

b3dm = B3dm('../data/XXX.b3dm') # path to a *.b3dm file / b3dm文件的路径
print(b3dm.toDict())
```

## Load a tile file from fileHandle/从文件指针读取瓦片

``` python
from p3dtiles.TileFormat.B3dm import B3dm

b3dm = B3dm(open('../data/XXX.b3dm', 'rb')) # give a file reader/给一个文件指针
# Method 'toDict()' return b3dm's readable format/toDict()方法返回人类可读的格式
print(b3dm.toDict()) 
```