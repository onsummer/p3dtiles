# p3dtiles
3dtiles 开发工具，拟实现读取3dtiles数据集和修改部分数据，如有可能，考虑做数据融合和转换等工作。使用python3原生实现，当前暂无第三方依赖库。

现在能读取一个b3dm文件，把它从二进制转换为json，使用B3dm类实例的toDict()方法可以返回一个dict，如果你喜欢可以写入json文件。

现在gltf引用的二进制数据暂时写为base64编码，后续考虑提供分离b3dm的模型的功能。

开发中的工作见[TODO](#TODO)。
基本用法见[Usage/用法](#usage)

*English Introduction* 

3dtiles sdk, aims to load the binary tile file(`*.b3dm`, `*.i3dm`, `*.pnts`, `*.cmpt`) , load the tileset, and modify some data in it. 

Implement using python3 without any 3rd-part dependences.

Now it can load a b3dm file to jsonfile by using B3dm.toDict() method, return a \<python dict\> . If you like you can save it to a jsonfile.

Future work see [TODO](#TODO).
Basic usage see [Usage/用法](#Usage/用法)

<h1 id="usage"> Usage / 用法 </h1>

## Load a tile file from given path / 从路径读取瓦片

``` python
from p3dtiles import B3dm

b3dm = B3dm('XXX.b3dm') # path to a *.b3dm file / b3dm文件的路径
print(b3dm.toDict())
```

## Load a tile file from fileHandle/从文件指针读取瓦片

``` python
from p3dtiles import B3dm

b3dm = B3dm(open('XXX.b3dm', 'rb')) # give a file reader/给一个文件指针
print(b3dm.toDict()) 
```
Method 'toDict()' return b3dm's readable information.
方法'toDict()'返回人类可读的数据。
# TODO

- 完善GlTF模块的代码分离

- 继续完善FeatureTable.FtBinary的解构（主要是i3dm瓦片）

- 继续开发I3dm、Cmpt瓦片文件的解构

- 递归解构Tileset.json

- 添加提取瓦片文件元数据的功能（ftJSON、btJSON等用于描述二进制文件的数据）

# 项目结构

```
目录
├─.gitignore // git忽略列表
├─README.md
|
├─p3dtiles // 主包
|    ├─Tileset.py   // 处理tileset.json文档的模块
|    ├─__init__.py
|    ├─TileFormat   // 子包，处理各种瓦片
|    |     ├─B3dm.py    // 处理b3dm瓦片的模块
|    |     ├─Cmpt.py    // 处理cmpt瓦片的模块
|    |     ├─GlTF.py    // 处理glTF模型的模块
|    |     ├─Vctr.py    // 处理Vctr模型的模块
|    |     ├─I3dm.py    // 处理i3dm瓦片的模块
|    |     ├─Pnts.py    // 处理pnts瓦片的模块
|    |     ├─__init__.py
|    |     └─TileBodyTable  // 子包，处理瓦片中的要素表和批量表
|    |             ├─BatchTable.py  // 处理批量表的模块
|    |             ├─DataTypeTranslator.py  // 处理两大表时转译结构数据类型的模块
|    |             ├─FeatureTable.py    // 处理要素表的模块
|    |             └__init__.py
|    └─FileUtils
|          └FileHelper.py   // 文件处理的模块
|
└─.vscode   // vscode配置
     └─ ...
```