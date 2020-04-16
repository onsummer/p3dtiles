# p3dtiles
3dtiles sdk. Implement using python3 without any dependences.
Now can read a b3dm file to jsonfile by using B3dm.toDict() method, return a dict and if you like you can save it to a jsonfile.

3dtiles 开发工具。使用python3原生实现，当前暂无依赖库。
现在能读取一个b3dm文件，把它从二进制转换为json，使用B3dm类实例的toDict()方法可以返回一个dict，如果你喜欢可以写入json文件。
现在gltf引用的二进制数据暂时写为base64编码，后续考虑分离。

## test目录
作者测试用目录，可以删除/ my test folder, you can delete it

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

# TODO

- 完善GlTF模块的代码分离

- 继续完善FeatureTable.FtBinary的解构（主要是i3dm数据）

- 继续开发I3dm、Pnts、Cmpt瓦片文件的解构

- 递归解构Tileset.json