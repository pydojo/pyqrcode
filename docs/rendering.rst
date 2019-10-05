翻译二维码
******************

在翻译二维码过程中有 5 种格式。第一种是翻译成由 1 和 0 组成的字符串。
然后二维码可以直接显示在终端里。也有三种图片格式渲染器。所有这些图片格式，
第一点就是你要设置使用的颜色。它们也可以得到一种标量因素，这种方式每个模块
不会渲染成 1 个像素。

基于文本的翻译
====================

在 `pyqrcode` 模块中包含了一项基础文本渲染器。
这会返回一个含有二维码的字符串，由 1 和 0 组成
了每一行二维码。
在二维码中一个数据 :term:`data module` 表示成一个1，
相反，0用来表示二维码的背景。

这种渲染器的目的是让用户建立自己的渲染器，因为如果内置
的渲染器不能满足需求的情况下就更加灵活了。

.. code-block:: python

  >>> number = pyqrcode.create(123)
  >>> print(number.text())
  00000000000000000000000000000
  00000000000000000000000000000
  00000000000000000000000000000
  00000000000000000000000000000
  00001111111011110011111110000
  00001000001000101010000010000
  00001011101001010010111010000
  00001011101010011010111010000
  00001011101000100010111010000
  00001000001001001010000010000
  00001111111010101011111110000
  00000000000001011000000000000
  00000010111011010100010010000
  00001011110001111101010010000
  00000111111011100101001000000
  00001001100011010011110010000
  00001111111001101011001110000
  00000000000010000000001100000
  00001111111000111100100100000
  00001000001011010110001100000
  00001011101010110000101010000
  00001011101001111111010100000
  00001011101011101001011010000
  00001000001001011001110000000
  00001111111000011011011010000
  00000000000000000000000000000
  00000000000000000000000000000
  00000000000000000000000000000
  00000000000000000000000000000


终端翻译
==================

二维码可以直接渲染到一个终端里，并且可以直接由二维码扫描器读取。
使用 ASCII 转义字符来完成翻译。因此绝大多数 Linux 终端都能用。
二维码的颜色也可以进行设置。

.. code-block:: python

  >>> text = pyqrcode.create('Example')
  >>> print(text.terminal())
  >>> print(text.terminal(module_color='red', background='yellow'))
  >>> print(text.terminal(module_color=5, background=123, quiet_zone=1))

在终端里翻译颜色时，是一项技巧性工作。不能超出8色彩机制范围，
否则会有问题。记住这一点只要知道8色彩机制的颜色名即可，它们是：
 black, red, green, yellow, blue, magenta, 和 cyan 。
尽管只有8个颜色，但也能支持另外一些浅色，名字是：
 light gray, dark gray, light red, light green, light blue,
 light yellow, light magenta, light cyan, 和 white 。

另外有两个颜色名，第一个是 "default" ，它对应着终端的默认背景色。
第二个是 "reverse" ，它是当前背景色的反差色。这2个颜色名都是通过
终端方法使用的默认色。

终端方法也支持 256 色彩机制。这种色彩机制是最新的颜色机制。
要使用 256 色直接提供一个0到256的数字即可。这个数字会作为
终端调色板的索引值。一个颜色实际色是根据操作系统来决定。
换句话说，大部分终端模拟器都支持 256 色，所以由于操作系统
原因不能断言一定显示的是什么颜色。

图片翻译
===============

有3种方法来得到二维码图片。所有渲染器都有很少的共性。

每个渲染器要得到一个文件路径或可写的流数据后，绘制二维码。
这些方法都应该实现自动侦测。

每个渲染器也要得到一个标量参数。标量参数设置了单个数据
:term:`data module` 的像素大小。设置标量参数值为1时，
让每个 :term:`data module` 数据都得到1像素。换句话说，
二维码太小的话很难实现扫描成功。使用什么标量值根据你要如何
使用你的二维码来决定。通用中，3、4或5会是最小的尺寸了，而且
能够扫描成功。

二维码也支持有一项 :term:`quiet zone` 无噪点区域环绕着二维码。
这个区域的每一边是4块宽。无噪点区域是用来确保打印出来的二维码能够
扫描成功。对于电子用法来说，无噪点区域也许是不需要根据二维码是如何
显示的。每个渲染器都允许你设置无噪点区域的大小。

许多渲染器也允许你设置 :term:`module` 单位块和背景色。尽管如此，
颜色如何表现都是渲染器来描述的。

XBM 翻译
-------------

对于 XBM 文件格式来说是一种直接黑白图片格式。图片数据采用了
一种合法 C 头部文件形式。 XBM 渲染过程是通过
:py:meth:`pyqrcode.QRCode.xbm` 方法来处理的。

XMB 文件天生被 Tkinter 支持。所以在 Tkinter 应用中显示二维码是非常容易。

.. code-block:: python

    >>> import pyqrcode
    >>> import tkinter
    >>> # Create and render the QR code
    >>> code = pyqrcode.create('Knights who say ni!')
    >>> code_xbm = code.xbm(scale=5)
    >>> # Create a tk window
    >>> top = tkinter.Tk()
    >>> # Make generate the bitmap image from the redered code
    >>> code_bmp = tkinter.BitmapImage(data=code_xbm)
    >>> # Set the code to have a white background,
    >>> # instead of transparent
    >>> code_bmp.config(background="white")
    >>> # Bitmaps are accepted by lots of Widgets
    >>> label = tkinter.Label(image=code_bmp)
    >>> # The QR code is now visible
    >>> label.pack()

可标量向量图形 (SVG)
-----------------------------

对于 SVG 渲染器输出的二维码，会是一种可标量向量图形，
使用 :py:meth:`pyqrcode.QRCode.svg` 方法来实现。

该方法绘制二维码要使用一个路径集合。默认情况不绘制背景，
例如，二维码结果有一种透明背景。默认前景（块单位）颜色是黑色。

.. code-block:: python

  >>> url = pyqrcode.create('http://uca.edu')
  >>> url.svg('uca.svg', scale=4)
  >>> # in-memory stream is also supported
  >>> buffer = io.BytesIO()
  >>> url.svg(buffer)
  >>> # do whatever you want with buffer.getvalue()
  >>> print(list(buffer.getvalue()))
  
你可以改变数据块的颜色，使用 *module_color* 参数实现。
同样，你可以使用 *background* 参数来描述一个背景色。
这些参数都可以接受一种 HTML 风格的颜色，例如网络安全色。

.. code-block:: python

  >>> url.svg('uca.svg', scale=4, background="white", module_color="#7D007D")

你也可以强制 SVG 文档的某部分内容。换句话说，
你可以建立一个 SVG 碎片。

封装的 PostScript 脚本(EPS)
-----------------------------

对于 EPS 渲染器输出二维码来说，是一种封装的 PostScript 脚本文档，
使用 :py:meth:`pyqrcode.QRCode.eps` 方法来实现。 *这种渲染器
不需要任何一个外部模块。*

该方法绘制 EPS 文档使用相邻块行实现。默认情况不绘制背景，
例如，二维码结果有一种透明背景。默认块颜色是黑色。注意，
1标量等价于一个块绘制在1点上（1/72 英寸）。

.. code-block:: python

  >>> qr = pyqrcode.create('Hello world')
  >>> qr.eps('hello-world.eps', scale=2.5, module_color='#36C')
  >>> qr.eps('hello-world2.eps', background='#eee')
  >>> out = io.StringIO()
  >>> qr.eps(out, module_color=(.4, .4, .4))

移植网络图像 (PNG)
------------------------------

对于 PNG 渲染器输出二维码是一种可移植网络图像文件，
使用 :py:meth:`pyqrcode.QRCode.png` 方法实现。

.. note::

  PNG 渲染器需要安装 `pypng <https://pypi.python.org/pypi/pypng/>`_ 模块。

.. code-block:: python

  >>> url = pyqrcode.create('http://uca.edu')
  >>> with open('code.png', 'w') as fstream:
  ...     url.png(fstream, scale=5)
  >>> # same as above
  >>> url.png('code.png', scale=5)
  >>> # in-memory stream is also supported
  >>> buffer = io.BytesIO()
  >>> url.png(buffer)
  >>> # do whatever you want with buffer.getvalue()
  >>> print(list(buffer.getvalue()))


颜色应该是一个列表或元素类型，所包含的数字是介于0到255之间。
列表数据应该是3个值形式（RGB）或4个值形式（RGBA）。颜色是
 (0,0,0) 表示的是黑色，白色是 (255,255,255) 来表示。
对于第四个值是0时，表示的是全部透明。同时第四个值是255时，
表示的是不透明。

默认情况，PNG 渲染器建立一个二维码所含的数据块颜色是黑色，
背景块颜色是白色。

.. code-block:: python

  >>> url.png('uca-colors.png', scale=6, 
  ...         module_color=[0, 0, 0, 128], 
  ...         background=[0xff, 0xff, 0xcc])

