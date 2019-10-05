欢迎使用 PyQRCode 文档！
************************************

对于 `pyqrcode` 模块来说，就是一个 QR 二维码生成器，
直接在纯 Python 代码中来编写二维码。本模块兼容 Python
 2.6, 2.7, 和 3.x 版本。几乎为你自动建立完成建立过程。
通用中，二维码可以使用2行代码完成创建工作！

与许多其它二维码生成器不同，所有自动化都可以进行手动控制。
你可以自由设置二维码的任何一项财产值，或设置所有财产值。

二维码可以保存成 SVG, EPS, PNG 格式（要使用
`pypng <https://pypi.python.org/pypi/pypng/>`_ 模块），
甚至可以保存成纯文本格式。本模块没有使用 PIL 来渲染成图片格式文件。
你也可以直接把一个二维码显示成终端里的图像格式。

对于 `pyqrcode` 模块的目的来说，本模块遵循了二维码标准，
尽可能紧随国际标准。术语和编码的使用，在 `pyqrcode` 中
直接与标准一致。本模块也遵循了二维码标准中的算法。

Contents:

.. toctree::
   :maxdepth: 1

   create
   encoding
   rendering
   moddoc

   PyPI Readme <README>

   glossary

前提条件
============

在 `pyqrcode` 模块的使用中，只需要安装 Python 2.6, 2.7, 3.x 版本即可。
你也许想要安装 `pypng <https://pypi.python.org/pypi/pypng/>`_ 来支持
渲染成 PNG 格式的图片文件，这是一个良好的选择。注意， `pypng` 模块是一个纯
 Python 的 PNG 写入器，所以不再需要任何其它 Python 库。


安装
============

安装是简单的，直接用 `pip` 安装 PyQRCode 模块即可::

    $ pip install pyqrcode

或者采用如下方式安装::

    $ python setup.py install


用法
=====

由于 `pyqrcode` 模块的目标是尽可能保持简单实用为原则。
下面的一个简单例子就是为一个网址建立一个二维码。二维码
渲染成了黑白标量向量图像文件::

    >>> import pyqrcode
    >>> url = pyqrcode.create('http://uca.edu')
    >>> url.svg('uca-url.svg', scale=8)
    >>> print(url.terminal(quiet_zone=1))

除了 `pyqrcode` 模块简单实用外，它也是具有威力的模块。
你可以设置二维码的所有财产项。如果你安装了 `pypng` 库，
你可以渲染成一个 PNG 图片文件。显示一个更多层化的示例::

    >>> big_code = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
    >>> big_code.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])


开发者文档
=======================

.. toctree::
   :maxdepth: 1

   moddoc
   tables
   builder


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
