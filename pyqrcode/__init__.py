# -*- coding: utf-8 -*-
# Copyright (c) 2013, Michael Nooner
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""This module is used to create QR Codes. It is designed to be as simple and
as possible. It does this by using sane defaults and autodetection to make
creating a QR Code very simple.

It is recommended that you use the :func:`pyqrcode.create` function to build the
QRCode object. This results in cleaner looking code.

Examples:
        >>> import pyqrcode
        >>> import sys
        >>> url = pyqrcode.create('http://uca.edu')
        >>> url.svg(sys.stdout, scale=1)
        >>> url.svg('uca.svg', scale=4)
        >>> number = pyqrcode.create(123456789012345)
        >>> number.png('big-number.png')
"""

#Imports required for 2.7 support
from __future__ import absolute_import, division, print_function, with_statement, unicode_literals

import pyqrcode.tables
import pyqrcode.builder as builder

try:
    str = unicode  # Python 2
except NameError:
    pass

def create(content, error='H', version=None, mode=None, encoding=None):
    """当建立一个二维码时，只有内容是需要进行编码的，
    其他所有二维码的财产项会根据内容来进行选择适合的财产值。
    这个函数会返回一个 :class:`QRCode` 类的实例对象。

    除非你非常熟悉二维码的内部工作原理，否则建议你只通过描述
    *内容*来建立二维码，其它的都别动。不管如何做到的，
    有一些情况是你想要描述一些不同的财产值来手动建立二维码，
    这也是除了内容参数以外的参数有用的地方。
    注意，参数名于参数值都直接来自二维码的技术标准。
    你也许需要自己去熟悉一下二维码标准，然后了解二维码的术语，
    这样对于其它参数的名字和参数值就有了正确的理解。

    其中 *error* 参数是设置二维码错误纠正级别用的。
    二维码标准中定义了4个级别：
    第一级 'L' 是 7% 的错误纠正率。
    第二级 'M' 是 15% 的错误纠正率。
    第三级 'Q' 是 25% 的错误纠正率，也是共同使用的一个级别。
    第四级 'H' 是 30% 的错误纠正率。
    描述这项参数有许多方法，你可以使用大写，也可以使用小写字母，
    更可以使用错误纠正率的对应浮点数，还可以是百分比字符串形式。
    阅读 `tables.modes` 来了解所有可能的值内容。
    默认参数值是 'H' ，虽然是最高的错误纠正率，但数据容量也是最小的。

    其中 *version* 参数是描述二维码尺寸和数据容量用的。
    版本都是任意一个1到40之间的整数。其中版本值是1表示最小的二维码，
    版本值是40是最大的二维码。如果不描述参数值的话，二维码的内容和
    错误纠正级别会尽可能选择满足二维码内容的最低版本值。
    你也许想要描述版本参数值，当生成许多数据量不一样的二维码时都用一样的值。
    这样可以批量产生的二维码尺寸都一样。

    其中 *mode* 参数是描述二维码内容会如何进行编码的。
    默认值是根据二维码内容选择最可能的模式。
    这里有4种可用的模式：
    第一种 'numeric' 是用来编码整数的。
    第二种 'alphanumeric' 是用来编码一些 ASCII 字符的。这种模式使用
    时有一项限制，就是英语字母全大写，当然内容参数值要先使用字符串
    `str.upper()` 方法处理完内容后再进行编码。阅读 `tables.ascii_codes`
    文档了解完整的可用字符清单。
    第三种 'kanji' 是用来编码日语片假名的。
    第四种 'binary' 是直接把字节编码到二维码里（这种编码模式是最没有效率的）。

    其中 *encoding* 参数是描述如何解释二维码内容的。
    本参数只在乎 *content* 参数值是字符串、 unicode、或字节阵列数据类型。
    参数值必须是一种合法的编码字符串，或是 `None` 值。
    这会代入到 *content* 内容参数值的 `encode` 和 `decode` 方法中。
    """
    return QRCode(content, error, version, mode, encoding)

class QRCode:
    """这个类是用来表示一个二维码用的。
    要使用这个类，直接在构造器中给出一个字符串形式的数据来完成编码工作，
    这个类然后会在内存中建立一个二维码。接着你可以保存成不同的格式文件。
    注意，二维码可以写成 PNG 图片文件，但需要安装 `pypng` 模块。
    你可以在 PyPNG 模块主页找到它 http://packages.python.org/pypng/

    Examples:
        >>> from pyqrcode import QRCode
        >>> import sys
        >>> url = QRCode('http://uca.edu')
        >>> url.svg(sys.stdout, scale=1)
        >>> url.svg('uca.svg', scale=4)
        >>> number = QRCode(123456789012345)
        >>> number.png('big-number.png')

    .. note::
        对于类初始化中的参数能做什么，阅读 :func:`pyqrcode.create`
        函数的文档字符串。
    """
    def __init__(self, content, error='H', version=None, mode=None,
                 encoding='iso-8859-1'):
        #Guess the mode of the code, this will also be used for
        #error checking
        guessed_content_type, encoding = self._detect_content_type(content, encoding)
        
        if encoding is None:
            encoding = 'iso-8859-1'

        #Store the encoding for use later
        if guessed_content_type == 'kanji':
            self.encoding = 'shiftjis'
        else:
            self.encoding = encoding
        
        if version is not None:
            if 1 <= version <= 40:
                self.version = version
            else:
                raise ValueError("Illegal version {0}, version must be between "
                                 "1 and 40.".format(version))

        #Decode a 'byte array' contents into a string format
        if isinstance(content, bytes):
            self.data = content.decode(encoding)

        #Give a string an encoding
        elif hasattr(content, 'encode'):
            self.data = content.encode(self.encoding)

        #The contents are not a byte array or string, so
        #try naively converting to a string representation.
        else:
            self.data = str(content)  # str == unicode in Py 2.x, see file head

        #Force a passed in mode to be lowercase
        if hasattr(mode, 'lower'):
            mode = mode.lower()

        #Check that the mode parameter is compatible with the contents
        if mode is None:
            #Use the guessed mode
            self.mode = guessed_content_type
            self.mode_num = tables.modes[self.mode]
        elif mode not in tables.modes.keys():
            #Unknown mode
            raise ValueError('{0} is not a valid mode.'.format(mode))
        elif guessed_content_type == 'binary' and \
             tables.modes[mode] != tables.modes['binary']:
            #Binary is only guessed as a last resort, if the
            #passed in mode is not binary the data won't encode
            raise ValueError('The content provided cannot be encoded with '
                             'the mode {}, it can only be encoded as '
                             'binary.'.format(mode))
        elif tables.modes[mode] == tables.modes['numeric'] and \
             guessed_content_type != 'numeric':
            #If numeric encoding is requested make sure the data can
            #be encoded in that format
            raise ValueError('The content cannot be encoded as numeric.')
        elif tables.modes[mode] == tables.modes['kanji'] and \
             guessed_content_type != 'kanji':
            raise ValueError('The content cannot be encoded as kanji.')
        else:
            #The data should encode with the passed in mode
            self.mode = mode
            self.mode_num = tables.modes[self.mode]

        #Check that the user passed in a valid error level
        if error in tables.error_level.keys():
            self.error = tables.error_level[error]
        else:
            raise ValueError('{0} is not a valid error '
                             'level.'.format(error))

        #Guess the "best" version
        self.version = self._pick_best_fit(self.data)

        #If the user supplied a version, then check that it has
        #sufficient data capacity for the contents passed in
        if version:
            if version >= self.version:
                self.version = version
            else:
                raise ValueError('The data will not fit inside a version {} '
                                 'code with the given encoding and error '
                                 'level (the code must be at least a '
                                 'version {}).'.format(version, self.version))

        #Build the QR code
        self.builder = builder.QRCodeBuilder(data=self.data,
                                             version=self.version,
                                             mode=self.mode,
                                             error=self.error)

        #Save the code for easier reference
        self.code = self.builder.code

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "QRCode(content={0}, error='{1}', version={2}, mode='{3}')" \
                .format(repr(self.data), self.error, self.version, self.mode)

    def _detect_content_type(self, content, encoding):
        """这是一个实例方法，尽力自动检测数据类型。
        第一，先试着搞清楚数据是否是一种合法的整数，这种情况下本方法会返回数字。
        第二，测试数据是否是 'alphanumeric' 字母数字组合类型的二维码，使用
        一张特殊的数据表，其中含有二维码技术标准限制的 ASCII 字符范围。
        二维码数据会经过测试来确定是否在这个范围内。如果测试都失败，数据会
        采用 'binary' 二进制类型。
        
        返回一个元组，其中两个元素是检测到的模式和编码格式。

        注意，二维码标准中的 ECI 编码格式还没有部署。
        """
        def two_bytes(c):
            """Output two byte character code as a single integer."""
            def next_byte(b):
                """Make sure that character code is an int. Python 2 and
                3 compatibility.
                """
                if not isinstance(b, int):
                    return ord(b)
                else:
                    return b

            #Go through the data by looping to every other character
            for i in range(0, len(c), 2):
                yield (next_byte(c[i]) << 8) | next_byte(c[i+1])

        #See if the data is a number
        try:
            if str(content).isdigit():
                return 'numeric', encoding
        except (TypeError, UnicodeError):
            pass

        #See if that data is alphanumeric based on the standards
        #special ASCII table
        valid_characters = ''.join(tables.ascii_codes.keys())
        
        #Force the characters into a byte array
        valid_characters = valid_characters.encode('ASCII')

        try:
            if isinstance(content, bytes):
                c = content.decode('ASCII')
            else:
                c = str(content).encode('ASCII')

            if all(map(lambda x: x in valid_characters, c)):
                return 'alphanumeric', 'ASCII'

        #This occurs if the content does not contain ASCII characters.
        #Since the whole point of the if statement is to look for ASCII
        #characters, the resulting mode should not be alphanumeric.
        #Hence, this is not an error.
        except TypeError:
            pass
        except UnicodeError:
            pass

        try:
            if isinstance(content, bytes):
                if encoding is None:
                    encoding = 'shiftjis'

                c = content.decode(encoding).encode('shiftjis')
            else:
                c = content.encode('shiftjis')
            
            #All kanji characters must be two bytes long, make sure the
            #string length is not odd.
            if len(c) % 2 != 0:
                return 'binary', encoding

            #Make sure the characters are actually in range.
            for asint in two_bytes(c):
                #Shift the two byte value as indicated by the standard
                if not (0x8140 <= asint <= 0x9FFC or
                        0xE040 <= asint <= 0xEBBF):
                    return 'binary', encoding

            return 'kanji', encoding

        except UnicodeError:
            #This occurs if the content does not contain Shift JIS kanji
            #characters. Hence, the resulting mode should not be kanji.
            #This is not an error.
            pass

        #All of the other attempts failed. The content can only be binary.
        return 'binary', encoding

    def _pick_best_fit(self, content):
        """这个实例方法返回尽可能最小的版本号。
        版本号会根据给出的错误纠正级别来满足所描述的数据内容。
        """
        import math
        
        for version in range(1, 41):
            #Get the maximum possible capacity
            capacity = tables.data_capacity[version][self.error][self.mode_num]
            
            #Check the capacity
            #Kanji's count in the table is "characters" which are two bytes
            if (self.mode_num == tables.modes['kanji'] and
                capacity >= math.ceil(len(content) / 2)):
                return version
            if capacity >= len(content):
                return version

        raise ValueError('The data will not fit in any QR code version '
                         'with the given encoding and error level.')

    def show(self, wait=1.2, scale=10, module_color=(0, 0, 0, 255),
            background=(255, 255, 255, 255), quiet_zone=4):
        """这个实例方法是显示二维码用的。

        这个方法的主要目的是为了调试用。

        这个方法把 :py:meth:`png` 方法的输出结果（使用默认标量因数值10）
        保存到一个临时文件中，然后用标准的 PNG 阅读器应用程序打开图片文件，
        或者用标准的网页浏览器来打开图片。临时文件稍后会被删除掉。

        如果这个方法没有显示任何结果的话，尝试增加 `wait` 参数值。
        这个等待参数是用来描述多少秒，就是几秒后删除临时文件。
        注意，这个方法没有返回语句，直到提供的秒数（默认值是1.2）代入后。

        其它的参数都直接传递给 `png` 方法。
        """
        import os
        import time
        import tempfile
        import webbrowser
 
        try:  # Python 2
            from urlparse import urljoin
            from urllib import pathname2url
        except ImportError:  # Python 3
            from urllib.parse import urljoin
            from urllib.request import pathname2url

        f = tempfile.NamedTemporaryFile('wb', suffix='.png', delete=False)
        self.png(f, scale=scale, module_color=module_color,
                 background=background, quiet_zone=quiet_zone)
        f.close()
        webbrowser.open_new_tab(urljoin('file:', pathname2url(f.name)))
        time.sleep(wait)
        os.unlink(f.name)
        
    def get_png_size(self, scale=1, quiet_zone=4):
        """这个实例方法是帮助用户确定使用多少 *scale* 标量用的。
        当建立二维码的 PNG 文件时，标量用在终端里可以帮助用户确定
        二维码的像素尺寸，使用不同的标量值，二维码像素尺寸也不一样。

        这个方法会返回一个整数，表示二维码像素的宽和高。
        如果使用给出 *scale* 标量来绘制二维码，你就知道相应的像素大小是多少。
        由于二维码是正方形，数字表示了空间的宽和高。

        其中 *quiet_zone* 参数是设置二维码周围的无噪点区域有多宽。
        根据二维码标准，无噪点区域应该是4个数据块宽。把这个作为可设置的，
        是因为这种无噪点区域的宽在许多应用程序中是不需要的，因为很少会打印二维码。

        Example:
            >>> code = pyqrcode.QRCode("I don't like spam!")
            >>> print(code.get_png_size(1))
            31
            >>> print(code.get_png_size(5))
            155
        """
        return builder._get_png_size(self.version, scale, quiet_zone)

    def png(self, file, scale=1, module_color=(0, 0, 0, 255),
            background=(255, 255, 255, 255), quiet_zone=4):
        """这个实例方法是把二维码写成一个 PNG 图片文件。
        作为 PNG 结果会有1个深度。
        其中 `file` 位置参数是用来描述图片存储到哪里，参数值即可以是
        一种可写的流数据，也可以是一个文件路径。

        .. note::
            这个方法的使用要依赖 `pypng` 模块，所以要安装模块后才能真正建立 PNG 文件。

        这个方法会把给出的 *file* 参数值写成一个 PNG 文件。
        参数值可以是字符串文件路径，也可以是一个可写的流数据。
        如果使用流数据的话，参数 `file` 不会自动关闭。

        其中 *scale* 参数是设置对一个数据块要绘制多大。
        默认参数值是一个数据块绘制1个像素。这也许会让二维码看起来太小，
        导致无法有效读取二维码。增加 `scale` 参数值会让二维码变大。
        参数值只可以使用整数。这个方法会把参数值都变成整数（例如，
        2.5会变成2，3会变成3）。
        你可以使用 :py:meth:`get_png_size` 方法来计算 PNG 图片的实际像素大小。

        其中 *module_color* 参数是设置用什么颜色来对数据块进行编码。
        （绝大部分二维码数据块都是黑色）。
        其中 *background* 参数是设置背景色（大部分二维码用白色）。
        如果设置这两个参数中的一个，那就都要手动分配参数值，
        否则会抛出 `ValueError` 例外错误。颜色值应该描述成列表或元组，
        长度为3或4，其中每个元素值是0到255的整数。
        三个元素长度的参数值是 RGB 色，四个元素长度的参数值 RGBA 色，
        增加了一个透明度，alpha 成份，0表示透明，255表示不透明。
        注意，许多颜色组合都是无法被二维码扫描器读取的，所以慎用着色特性。

        其中 *quiet_zone* 无噪点区域参数是设置二维码周围的宽度。
        根据二维码标准，这个宽度应该是4个数据块。保留成可设置是因为
        许多应用程序不需要这个无噪点区域宽度，因为很少需要打印二维码。

        Example:
            >>> code = pyqrcode.create('Are you suggesting coconuts migrate?')
            >>> code.png('swallow.png', scale=5)
            >>> code.png('swallow.png', scale=5,
                         module_color=(0x66, 0x33, 0x0),      #Dark brown
                         background=(0xff, 0xff, 0xff, 0x88)) #50% transparent white
        """
        builder._png(self.code, self.version, file, scale,
                     module_color, background, quiet_zone)

    def png_as_base64_str(self, scale=1, module_color=(0, 0, 0, 255),
                          background=(255, 255, 255, 255), quiet_zone=4):
        """这个实例方法使用 png 渲染器后返回编码成 base64 字符串格式的 PNG 图片。
        对于建立动态 PNG 图片来说是有用的，常应用在网络开发中，因为不需要建立文件。
        
        Example:
            >>> code = pyqrcode.create('Are you suggesting coconuts migrate?')
            >>> image_as_str = code.png_as_base64_str(scale=5)
            >>> html_img = '<img src="data:image/png;base64,{}">'.format(image_as_str)

        所有参数都会直接传递给 :py:meth:`png` 方法，对于参数的意义参考
        `png` 方法文档字符串。
        
        .. note::
            注意这个方法要依赖 `pypng` 模块，所以才能真正建立 PNG 图片格式。

        """
        import io
        import base64
        
        with io.BytesIO() as virtual_file:
            self.png(file=virtual_file, scale=scale, module_color=module_color,
                     background=background, quiet_zone=quiet_zone)
            image_as_str = base64.b64encode(virtual_file.getvalue()).decode("ascii")
        return image_as_str
        
    def xbm(self, scale=1, quiet_zone=4):
        """这个实例方法返回一种 XBM 图片格式的二维码字符串。
        对于 XBM 格式来说，这是一种黑白图片格式，看起来像一个 C 头部文件一样。
        
        因为在 Tkinter 中来显示二维码，所以主要用这种渲染器，
        这个方法不会得到一个 `file` 参数。而是把渲染完的二维码数据返回成一种字符串形式。
        
        在 Tkinter 中使用这个渲染器的例子如下：
            >>> import pyqrcode
            >>> import tkinter
            >>> code = pyqrcode.create('Knights who say ni!')
            >>> code_xbm = code.xbm(scale=5)
            >>>
            >>> top = tkinter.Tk()
            >>> code_bmp = tkinter.BitmapImage(data=code_xbm)
            >>> code_bmp.config(foreground="black")
            >>> code_bmp.config(background="white")
            >>> label = tkinter.Label(image=code_bmp)
            >>> label.pack()

        
        其中 *scale* 参数是设置一个数据块要绘制多大。
        默认值是使用1个像素绘制一个数据块。这会让二维码太小无法有效读取。
        增加参数值回让二维码变大。只接受整数作为参数值。
        这个方法回把标量参数值归为一个整数（例如2.5会变成2，3变成3）。
        你可以使用 :py:meth:`get_png_size` 方法来计算显示图片时的实际像素大小。

        其中 *quiet_zone* 参数是设置二维码周围的无噪点区域有多宽。
        根据二维码标准这个参数值应该是4个数据块。保留成可设置是因为
        这样的一种无噪点区域宽度在许多应用程序中是不需要的，因为很少
        打印二维码。
        """
        return builder._xbm(self.code, scale, quiet_zone)

    def svg(self, file, scale=1, module_color='#000', background=None,
            quiet_zone=4, xmldecl=True, svgns=True, title=None,
            svgclass='pyqrcode', lineclass='pyqrline', omithw=False,
            debug=False):
        """这个实例方法是把二维码写成一种 SVG 文档格式。
        二维码只会把数据块绘制成1。数据块都会用一行来绘制，
        例如一行中的连续数据块都会绘制在单行里。

        其中 *file* 参数是用来描述存储文件位置用的。
        即可以是可写的流数据，也可以是一个文件路径。
        
        其中 *scale* 参数是设置单个数据块要绘制多大。
        默认值是用1个像素绘制一个数据块。也许会让二维码太小无法有效读取。
        增加参数值会让二维码变大。与 `png()` 方法不一样，
        这个方法回接受分数标量值（例如，2.5）。

        注意，有三件事实现后能建立适合嵌入到 HTML 文档中的二维码。
        那就是二维码的 "白色" 部分要完全透明。
        二维码本身有一个已知类 *svgclass* 参数。
        组成二维码的路径使用这个类设置，使用的是 *lineclass* 参数。
        这些因素让建立二维码更容易使用 CSS 风格。

        这个方法的默认输出结果是一个含有完整的 SVG 的 XML 文档。
        如果只想要二维码本身的话，把 *xmldecl* 参数值设置成 `False` 即可。
        这样会形成一个含有只绘制二维码部分的 SVG 片段。
        同时，你可以设置 *title* 参数给文档提供页面抬头内容。
        对于 SVG 名字空间属性可以通过设置 *svgns* 参数值为 `False` 来
        实现不显示二维码图形，只显示 XML 文档树内容。

        其中 *omithw* 参数值设置成 `True` 会说明要忽略宽高属性。
        那么会有一项 ``viewBox`` 属性增加到 XML 文档中，效果就是
        页面中有一个类似全屏的二维码图像了。

        你也可以直接设置颜色，使用 *module_color* 和 *background* 参数。
        其中 *module_color* 参数是设置数据块要使用的颜色（大部分都是黑色）。
        其中 *background* 参数是设置背景色（大部分都是白色）。
        这两个参数可以设置成任何一种合法的 SVG 或 HTML 安全色。
        如果背景参数值设置成 `None` 的话，不会绘制背景色，例如背景色是透明的。
        注意，许多颜色组合都不会被二维码扫描器读取，所以用色要谨慎。

        其中 *quiet_zone* 参数是设置无噪点区域宽应该是多大。
        根据二维码标准这个参数值应该是4个数据卡宽。保留成可设置是因为许多应用
        程序中不需要无噪点区域宽，因为很少会打印二维码。
        
        Example:
            >>> code = pyqrcode.create('Hello. Uhh, can we have your liver?')
            >>> code.svg('live-organ-transplants.svg', 3.6)
            >>> code.svg('live-organ-transplants.svg', scale=4,
                         module_color='brown', background='0xFFFFFF')
        """
        builder._svg(self.code, self.version, file, scale=scale, 
                     module_color=module_color, background=background,
                     quiet_zone=quiet_zone, xmldecl=xmldecl, svgns=svgns, 
                     title=title, svgclass=svgclass, lineclass=lineclass,
                     omithw=omithw, debug=debug)

    def eps(self, file, scale=1, module_color=(0, 0, 0),
            background=None, quiet_zone=4):
        """这个实例方法是把二维码写成一种 EPS 文档。
        二维码的绘制只把数据块写成1。数据块绘制成行，这样一行里相邻的数据块
        都会绘制在单行里。

        其中 *file* 参数是用来描述文档的存储位置用的。
        参数值即可以是可写的（文本）流数据，也可以是一个文件路径。

        其中 *scale* 参数是设置一个数据块绘制多大用的。
        参数默认值是1点（1/72 英寸）绘制一个数据块。这可能让二维码太小无法有效读取。
        增加标量参数值会让二维码变大。这个参数值可以是分数标量值（例如，2.5）。

        其中 *module_color* 参数是设置数据块的颜色用的。
        其中 *background* 参数是设置背景色（页面颜色）用的。
        这两个与颜色有关的参数值即可以描述成三个浮点数形式 (0.5, 0.5, 0.5)，
        也可以描述成三个整数形式 (128, 128, 128)。
        其中 *module_color* 参数值默认是黑色， *background* 参数默认值透明色。

        其中 *quiet_zone* 参数是设置二维码边界多宽用的。
        由于二维码标准，默认值是4个数据块。

        Examples:
            >>> qr = pyqrcode.create('Hello world')
            >>> qr.eps('hello-world.eps', scale=2.5, module_color='#36C')
            >>> qr.eps('hello-world2.eps', background='#eee')
            >>> out = io.StringIO()
            >>> qr.eps(out, module_color=(.4, .4, .4))
        """
        builder._eps(self.code, self.version, file, scale, module_color,
                     background, quiet_zone)

    def terminal(self, module_color='default', background='reverse',
                 quiet_zone=4):
        """这个实例方法返回一种含有 ASCII 转义代码字符串形式。
        如果使用 `print()` 函数输出的话，会在终端里显示成二维码图像。
        使用 ASCII 转义代码输出的二维码在背景色上会有变化。

        其中 *module_color* 参数是设置数据块颜色用的（大部分二维码是黑色）。
        其中 *background* 参数是设置背景色用的（大部分是白色）。

        对于颜色来说，在终端里有两种选择。
        第一种，最广泛支持的就是实用 8 或 16 色彩机制。
        这种色彩机制实用了8到16个颜色名字，分别是：
        black, red, green, yellow, blue, magenta, 和 cyan。
        另外一些颜色名字是：
        light gray, dark gray, light red, light green, 
        light blue, light yellow, light magenta, light cyan, 和 white。 

        这里有两个特殊的颜色名字。
        *module_color* 参数值是 "default"，这个颜色是采用
        终端的背景色。
        *background* 参数值是 "reverse"，这个颜色实际上不是真正的颜色，
        而是一种特殊的财产值，这个财产值是当前颜色的反向色。
        这两个特殊的颜色名字分别是参数的默认值。
        以上颜色在绝大多数终端里都有效。

        最后，还有一项特殊的颜色。
        有的终端支持 256 色，而实际显示出来的颜色要依赖系统的终端。
        这是比较少用的一种选择。要使用 256 色机制，就是设置
        *module_color* 参数和/或 *background* 参数的值介于 0 到 256 之间。

        其中 *quiet_zone* 参数是设置无噪点区域多宽用的。
        根据二维码标准这个参数值应该是4个数据块。保留成可设置是因为
        在许多应用程序中不需要使用无噪点区域宽。

        Examples:
            >>> code = pyqrcode.create('Example')
            >>> text = code.terminal()
            >>> print(text)
        """
        return builder._terminal(self.code, module_color, background,
                                 quiet_zone)

    def text(self, quiet_zone=4):
        """本实例方法返回二维码的一种字符串表现形式。
        数据块都用1来表示，背景色块都用0表示。
        这种文本形式的主要目的是扮演了用户自己建立渲染器的起始点。

        其中 *quiet_zone* 参数是设置无噪点区域宽。
        根据二维码标准参数值应该是4个数据块。保留可设置是因为在许多应用程序中
        不需要这样一种无噪点区域宽。

        Examples:
            >>> code = pyqrcode.create('Example')
            >>> text = code.text()
            >>> print(text)
        """
        return builder._text(self.code, quiet_zone)

