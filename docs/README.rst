========
PyQRCode
========

.. contents::

对于 `pyqrcode` 模块来说就是一个二维码生成器，简单实用的以纯 Python 代码开发。
本模块可以自动完成建立二维码的过程。大部分二维码可以仅用2行代码就搞定！

不像其它的二维码生成器库那样，所有功能都可以手动控制。
你可以自由地设置二维码的任何一种或所有财产项。

二维码可以保存成 SVG, PNG (要使用 `pypng <https://pypi.python.org/pypi/pypng/>`_ 模块)，
以及保存成纯文本。二维码也可以直接显示在大多数 Linux 终端模拟器里。
本模块不使用 PIL 对图片文件做渲染。

对于 `pyqrcode` 模块来说，目的是遵循二维码标准。
在 `pyqrcode` 中使用的术语和编码都直接来自二维码技术标准。
本模块也遵循了二维码标准中的算法。

**主页**: https://github.com/mnooner256/pyqrcode

**文档**: http://pythonhosted.org/PyQRCode/

前提条件
============

对于 `pyqrcode` 模块来说，你要安装 Python 2.6, Python 2.7, 或 Python 3 版本。
你也许要安装 `pypng <https://pypi.python.org/pypi/pypng/>`_ 来输出成 PNG 图片，
但选择权在你。注意 `pypng` 是一个纯 Python 编写的 PNG 文件书写器，不需要任何其它库。

安装
============

安装是简单的，你可以使用 `pip` 直接执行下面命令来安装::

    $ pip install pyqrcode

或者从源代码来安装::

    $ python setup.py install


用法
=====

对于 `pyqrcode` 模块的目的，就是简单实用为原则。
下面是一个简单的创建含有 URL 的二维码示例。
二维码渲染成一个 SVG 文件::

    >>> import pyqrcode
    >>> url = pyqrcode.create('http://uca.edu')
    >>> url.svg('uca-url.svg', scale=8)
    >>> url.eps('uca-url.eps', scale=2)
    >>> print(url.terminal(quiet_zone=1))

你可以看到 `pyqrcode` 模块除了简单实用外，还威力无比。
你可以设置二维码的每个财产项。如果你安装了
`pypng <https://pypi.python.org/pypi/pypng/>`_ 模块，
你可以渲染成一个 PNG 图片。下面是一个更多层化的例子::

    >>> big_code = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
    >>> big_code.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
    >>> big_code.show()
