pyqrcode
================================

`pyqrcode` 模块是一个二维码生成器，直接使用且是用纯 Python 编写。
模块可以自动完成创建二维码的大部分过程。大部分二维码可以仅用2行代码搞定！

不像其它的二维码生成器，所有功能都可以手动控制。
你可以自由地设置二维码的任何一项或所有财产项。

二维码可以保存成 SVG, XBM, EPS, PNG (要使用
[pypng](https://pypi.python.org/pypi/pypng/) 模块), 或保存成纯文本形式。
二维码也可以直接显示在大部分 Linux 终端模拟器里，以及直接显示在 Tkinter 程序中。
渲染成图片文件时不使用 PIL 模块。

`pyqrcode` 模块的目的是遵循二维码技术标准。模块中的术语和编码都直接来自二维码标准。
本模块也遵循了二维码标准中的算法。

前提条件
-------------------------

`pyqrcode` 模块只需要你安装 Python 2.6, Python 2.7, 或 Python 3 版本。
要想存储成 PNG 文件，你要安装 `pypng` 模块。选择权在你！

安装
------------

安装简单，直接使用 `pip` 命令：

```bash
$ pip install pyqrcode
```

或从源代码安装：

```bash
$ python setup.py install
```

用法
-----

这是对你唯一重要的事情。本模块的核心就是 `QRCode` 类。
你可以正常地调用这个类，或使用 *`create`* 打包函数。

```python
>>> import pyqrcode
>>> qr = pyqrcode.create('Unladden swallow')
>>> qr.png('famous-joke.png', scale=5)
```

PyPi
----

* _PyPi 页面_: https://pypi.python.org/pypi?name=PyQRCode&:action=display

* _文档地址_: http://pythonhosted.org/PyQRCode/

### 编码数据 ###

本模块支持所有对数据的4种编码：
numeric（数字模式）, alphanumeric（字母数字组合模式）, kanji（片假名模式）和 binary（二进制模式）。

数字类型是对编码数字最有效率的方法。顾名思义，就是为编码整数而设计的。
有些数字也许太大，你可以用数字字符串来代替直接数字形式。

```python
>>> number = pyqrcode.create(123456789012345)
````

字母数字类型是非常受限于只包含一些 ASCII 字符编码。
可编码的内容有：全大写字母，数字 0-9，水平空间，和八个标点符号。
就这些字符也完全满足对一个 URL 地址编码成二维码。

```python
>>> url = pyqrcode.create('http://uca.edu')
```

当其它编码模式失败时，数据会被编码成纯二进制。
下面的多行字符串种含有超出受限范围对字符和标点，
因为有小写字母、单引号、新行转义字符，所以必须采用二进制编码模式。

```python
>>> life = pyqrcode.create('''MR. CREOSOTE: Better get a bucket. I'm going to throw up.
    MAITRE D: Uh, Gaston! A bucket for monsieur. There you are, monsieur.''')
```
唯一没有部署的编码就是 ECI 模式，这个模式允许为多种编码用在二维码里（以后会部署）。

### 手动设置二维码的财产项 ###

有许多种情况你也许希望有更好的控制如何生成二维码。
你可以描述二维码的所有财产项，在 *`create`* 函数中，
有二维码的3个主要财产项。

其中 _`error`_ 参数是设置二维码的错误纠正级别。
每个级别都对应着一个字母： L, M, Q, 或 H；
每个级别响应的错误纠正率是百分之： 7, 15, 25, 或 30。
有许多种方法来描述级别，阅读 `pyqrcode.tables.modes` 内容。
这个参数的默认值是 `'H'` ，意思是采用最高错误纠正级别，
但却拥有最小的数据容量。

其中 _`version`_ 参数是描述二维码的大小和数据容量。
版本参数值都是1到40的整数，其中版本1是最小的二维码，
版本40是最大的。参数的默认值是根据数据的编码和错误纠正级别
计算出来的最小版本号。你也许想要在批量生产二维码时描述
这个参数值，因为含有不同的数据量，却能产生同样大小的二维码。

最后 _`mode`_ 参数是设置如何对二维码内容进行编码。
如同上面提到的一样，五种编码已经写完3种了。
本参数的默认值针对内容使用最有效率的编码模式。
你可以手动改变，阅读 `qrcode.tables.modes` 了解内容。

下面的代码是建立了一个 25% 错误纠正的二维码，大小是27，
并且指明使用二进制编码模式（这要比数字模式好一点）。

```python
>>> big_code = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
```

### 渲染 ###

在渲染二维码时有许多可以用的格式。
第一个是渲染成有1和0组成的字符串。这方法用来帮助用户建立自己的渲染器。
这也可以直接输出到大多数 Linux 终端里。
有一些图片形式的渲染器。

终端渲染器输出一种 ASCII 转义字符串二维码形式，
在终端里显示出一个合法的二维码。背景和数据块颜色都可设置
（尽管可以随时着色显示，但也有一些颜色警告）。

```python
>>> print(url.terminal())
>>> print(url.terminal('red', 'white'))
```

对于 SVG 渲染器输出的二维码，是作为一种可标量向量图形。
这种渲染器不需要任何一个外部模块。相反它把二维码绘制成一套路径集合。

```python
>>> url.svg(sys.stdout, scale=1)
>>> url.svg('uca.svg', scale=4, module_color="#7D007D")
```

另外，如果你安装了 `pypng` 模块的话，你可以把二维码渲染成一个 PNG 文件。
颜色应该描述成 RGB （无透明效果）或 RGBA （有透明效果）形式。

```python
>>> number.png('big-number.png')
>>> life.png('sketch.png', scale=6, module_color=(0, 0, 0, 128), background=(0xff, 0xff, 0xcc))
```

最后，一种基于文本的渲染器。这种输出二维码是由1和0组成的字符串形式，
二维码的每行数据都分别显示在一行上。

```python
>>> print(number.text())
```
