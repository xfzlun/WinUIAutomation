這個檔案是網站上我收集到的一些關於Windows下自動化的一些資料，主要的匯總思路就是把windows下自動化需要用到的代碼匯總，主要應用在以下几个方面：

1. 运行程序
2. 进程监控
3. 截图 & 图形切割
4. 图像识别 & 位置匹配
5. 文字识别 & 位置匹配
6. 鼠标操作
7. 键盘操作
8. 随机函数的使用



自动化。希望通过Python来操作软件。一般通过程序来操作視窗软件的原理需要获得该視窗的句柄，然后通过该句柄给窗口发命令来操作该软件。Python中可以利用許多方式，整理如下：



## 1. 运行程序

### 1. Pywin32: 

该模块提供了访问Windows API的扩展，利用该模块可以进行相关软件的操作。

Pywin32是一个Python库，为python提供访问Windows API的扩展，提供了齐全的windows常量、接口、线程以及COM机制等等。安装后自带一个pythonwin的IDE

**句柄**是一个32位整数，在windows中标记对象用，类似一个dict中的key

**消息**是windows应用的重要部分，用来告诉窗体“发生了什么”，比如给一个按钮发送BN_CLICKED这么个消息，按钮就知道“哦，我被点了”，才能执行相应的下一步操作。本文将大量使用消息机制。详情参看[这篇文章](http://blog.csdn.net/liulianglin/article/details/14449577)。

貌似在win32编程的世界里，包括窗口到文本框的所有控件就是窗体，所有的窗体都有独立的句柄。要操作任意一个窗体，你都需要找到这个窗体的句柄，这里，我们就可以用到FindWindow函数和FindWindowEx函数。在pywin32中，他们都属于win32gui的模块。

#### 包安装方式



#### 打开软件：

##### os 库：以记事本为例

```python
def runApp():
    os.system(u"C:\\Windows\\System32\\notepad.exe")
```

os.system的缺点是它是单线程的，所谓的阻塞，所以必须要等到这个程式结束后才可以继续下一个

##### win32api:

```python
def runApp():
    import win32api
    # 最后一个参数表示是窗口属性，0表示不显示，1表示正常显示，2表示最小化，3表示最大化
    res = win32api.ShellExecute(0, 'open', 'C:\\Windows\\System32\\notepad.exe', '', '', 3)
```

获取窗口句柄：

```python
def findAppHandle():
    appName = u"233.txt - 记事本"
    hwnd = win32gui.FindWindow(None, appName)
    print hwnd

# 关闭软件
win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
# 软件最大化
win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
# 将软件窗口置于最前
win32gui.SetForegroundWindow(hwnd)
```

- FindWindow(lpClassName=None, lpWindowName=None):
    - 描述：自顶层窗口（也就是桌面）开始搜索条件匹配的窗体，并返回这个窗体的句柄。不搜索子窗口、不区分大小写。找不到就返回0
    - 参数：
        - lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
        - lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。
    - 说明：这个函数我们仅能用来找主窗口。
- FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None);
    - 描述：搜索类名和窗体名匹配的窗体，并返回这个窗体的句柄。不区分大小写，找不到就返回0。
    - 参数：
        - hwndParent：若不为0，则搜索句柄为hwndParent窗体的子窗体。
        - hwndChildAfter：若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。
        - lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
        - lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。
    - 说明：找到了主窗口以后就靠它来定位子窗体啦。

有了这两个函数，我们就可以写出可以定义到任意一个窗体句柄的函数啦：

```python
def find_idxSubHandle(pHandle, winClass, index=0):
    """
    已知子窗口的窗体类名
    寻找第index号个同类型的兄弟窗口
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle
 
 
def find_subHandle(pHandle, winClassList):
    """
    递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
    else:
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
        return find_subHandle(pHandle, winClassList[1:])
    
```

这样在后续的调用中，我们就能使用我们定义的finde_subHandle来方便地找到某个特定的Edit窗体控件。比如我们定义一个FaceGenWindow的类：

```python
class FaceGenWindow(object):
    def __init__(self, fgFilePath=None):
        self.Mhandle = win32gui.FindWindow("FaceGenMainWinClass", None)
        print "FaceGen initialization compeleted"
```

实例化以后就可以很方便地在类的方法中调用find_subHandle函数来找到FaceGenWindow的子窗体了，比如某个Edit控件：

```python
handle = find_subHandle(self.Mhandle, [("ComboBoxEx32", 1), ("ComboBox", 0), ("Edit", 0)])
# python中找回来的句柄都是十进制整型，Spy++里显示的都是十六进制整型，这个要注意下，调试的时候用十六进制输出句柄，如下
print "%x" % (handle)
```

#### 菜单操作：

打开文件，File→Open，然后再File→Save Image

窗口的菜单就像窗口的标题栏一样，是窗口自身的一部分，不是其他窗体控件，也就没有办法用FindWindow和FindWindowEx返回句柄。所以要对菜单进行操作的话，我们需要新的函数，也就是GetMenu，GetSubMenu和GetMenuItemID，它们也都属于win32gui模块。怎么用呢，结合下图来说：

![](https://raw.githubusercontent.com/xfzlun/xfzlun.github.iogithub/master/%E6%88%AA%E5%B1%8F2020-08-25%20%E4%B8%8A%E5%8D%888.36.45.png)

- GetMenu(hwnd)
    - 描述：获取窗口的菜单句柄。
    - 参数：
        - hwnd：整型，需要获取菜单的窗口的句柄。
    - 说明：获取的是插图中黄色的部分。
- GetSubMenu(hMenu, nPos)
    - 描述：获取菜单的下拉菜单或者子菜单。
    - 参数：
        - hMenu：整型，菜单的句柄，从GetMenu获得。
        - nPos：整型，下拉菜单或子菜单的的索引，从0算起。
    - 说明：这个可以获取插图中蓝色的部分z；如描述所述，这个不仅可以获取本例中的下拉菜单，还可以获取子菜单。
- GetMenuItemID(hMenu, nPos)
    - 描述：获取菜单中特定项目的标识符。
    - 参数：
        - hMenu：整型，包含所需菜单项的菜单句柄，从GetSubMenu获得。
        - nPos：整型，菜单项的索引，从0算起。
    - 说明：这个获取的就是红色区域中的项目啦，**注意**，分隔符是被编入索引的，所以Open的索引是2而非1，而Exit的索引是9而非6。

找到这个菜单项的标识符有什么用呢？找到以后我们就可以告诉应用程序：我们要执行这个菜单项的命令！怎么告诉呢？这就要涉及消息机制了，我们要给应用程序发个消息，让它执行所需菜单项的命令。假设之前获取的Open的标识符是open_ID，那么只需要这样：

```python
win32gui.PostMessage(self.Mhandle, win32con.WM_COMMAND, open_ID, 0)
```

就会有一个打开文件的对话框出现啦。

解释一下：

- PostMessage(hWnd, Msg, wParam, lParam)

    - 描述：在消息队列中加入为指定的窗体加入一条消息，并马上返回，不等待线程对消息的处理。
    - 参数：
        - hWnd：整型，接收消息的窗体句柄
        - Msg：整型，要发送的消息，这些消息都是windows预先定义好的，可以参见[系统定义消息(System-Defined Messages](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).aspx#system_defined)))
        - wParam：整型，消息的wParam参数
        - lParam：整型，消息的lParam参数
    - 说明：简单说，就是给指定程序发一个消息，这些消息都用整型编好号，作为windows的常量可以查询的。在这里，我们用的就是win32con这个库里定义的WM_COMMAND这个消息，具体的wParam和lParam是根据消息的不同而不同的。具体请根据MSDN查阅。

    

    ##### 关于wParam的low word和high word：

    > 查阅MSDN的消息时，会发现有的wParam定义了low word和high word，这是什么呢？wParam的定义是32位整型，high word就是他的31至16位，low word是它的15至0位，如图。当参数超过两个，wParam和lParam不够用时，可以将wParam就给拆成两个int16来使用。这种时候在python里记得用把HIWORD的常数向左移16位，再加LOWORD，即wParam = HIWORD<<16+LOWORD。

    

    ![](https://raw.githubusercontent.com/xfzlun/xfzlun.github.iogithub/master/20131225011108578.png)

    

    

    ```python
    class FaceGenWindow(object):
        def __init__(self, fgFilePath=None):
            self.Mhandle = win32gui.FindWindow("FaceGenMainWinClass", None)
            self.menu = win32gui.GetMenu(self.Mhandle)
            self.menu = win32gui.GetSubMenu(self.menu, 0)
            print "FaceGen initialization compeleted"
     
     
        # 然后定义一个菜单操作的方法：
     
     
        def menu_command(self, command):
            """
            菜单操作
            返回弹出的打开或保存的对话框的句柄 dig_handle
            返回确定按钮的句柄 confBTN_handle
            """
            command_dict = {  # [目录的编号, 打开的窗口名]
                "open": [2, u"打开"],
                "save_to_image": [5, u"另存为"],
            }
            cmd_ID = win32gui.GetMenuItemID(self.menu, command_dict[command][0])
            win32gui.PostMessage(self.Mhandle, win32con.WM_COMMAND, cmd_ID, 0)
            for i in range(10):
                if win32gui.FindWindow(None, command_dict[command][1]): 
                    break  # 如果找到了打开或者另存为的对话框，就跳出循环
                else:
                    win32api.Sleep(200)  # 利用这个函数等待200ms，就不需要再额外导入time模块了
            dig_handle = win32gui.FindWindow(None, command_dict[command][1])
            confBTN_handle = win32gui.FindWindowEx(dig_handle, 0, "Button", None)
            return dig_handle, confBTN_handle  # 返回了弹出来的对话框的句柄和确定按钮的句柄
    ```



#### 控件操作A

通过菜单的目录操作，我们打开了打开文件对话框。为了简单起见，我们可以直接在文件名处填入要打开文件的绝对路径。怎么填呢？

首先还是定位到文本框控件

```python
handle = find_subHandle(Mhandle, [("ComboBoxEx32", 0), ("ComboBox", 0), ("Edit", 0)])
```

find_subHandle()是在Part 1中定义的函数，可以按照列表的信息查找Mhandle的子窗体。列表中的元组提供窗体的类名和排位号（z-index）。列表索引编号较小的为父窗体。

接着我们依然是利用win32的消息机制，给这个文本框控件送去一个消息：

```python
win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, os.path.abspath(fgFilePath).encode('gbk'))
```

在这里，我们用了SendMessage而不是PostMessage，其区别就在于我们可以通过SendMessage取得消息的返回信息。因为对于我们要设置文本框信息的WM_SETTEXT信息来说，设置成功将返回True。

- SendMessage(hWnd, Msg, wParam, lParam)
    - 描述：在消息队列中加入为指定的窗体加入一条消息，直到窗体处理完信息才返回。
    - 参数：
        - hWnd：整型，接收消息的窗体句柄
        - Msg：整型，要发送的消息，这些消息都是windows预先定义好的，可以参见[系统定义消息（System-Defined Messages）](http://msdn.microsoft.com/en-us/library/windows/desktop/ms644927(v=vs.85).aspx#system_defined)
        - wParam：整型，消息的wParam参数
        - lParam：整型，消息的lParam参数
    - 说明：wParam和IParam根据具体的消息不同而有不同的定义，详情参阅Part 2.
- WM_SETTEXT 消息
    - 描述：设置窗体的文本
    - 参数：
        - wParam：未使用
        - lParam：一个指针，指向以null结尾的字符串。窗体文本将被设置为该字符串。
    - 返回值：
        - 如果成功设置，则返回1（MSDN原文是返回True）
    - 说明：
        - 上面的定义是直接从MSDN上翻译过来的，在Python的语境里面没有指针，你只需要把变量名作为lParam传入就好了。
        - 另外，请注意编码，**包含中文请用gbk编码，否则乱码**。

再利用一个WM_COMMAND消息来点击确定按钮：

```python
win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle)
```

- WM_COMMAND 消息
    - 描述：当用户选择了菜单（或按钮等控件的）命令，或控件发送通知到父窗口，或加速键击（accelerator keystroke is translated）时发送。
    - 参数：根据情景不同而不同，在这里属于用户命令，参数配置如下
        - wParam：HIWORD为0（未使用），LOWORD为控件的ID
        - lParam：0（未使用）
    - 返回值：如果窗体处理了消息，应返回0

综上，我们现在就可以利用win32的各种API完成打开fg文件的任务了。

```python
def open_fg(self, fgFilePath):
    """打开fg文件"""
    Mhandle, confirmBTN_handle = self.menu_command('open')
    handle = find_subHandle(Mhandle, [("ComboBoxEx32", 0), ("ComboBox", 0), ("Edit", 0)])
    if win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, os.path.abspath(fgFilePath).encode('gbk')) == 1:
        return win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle)
    raise Exception("File opening path set failed")
```

顺便，如果要获取目标文本框的内容呢，可以使用WM_GETTEXT，如下：

- WM_GETTEXT 消息：
    - 描述：将窗体的文本内容复制到指定的buffer对象中
    - 参数：
        - wParam：要复制字符的最大长度，包括截尾的空字节
        - lParam：用来保存字符串的buffer的指针
    - 返回值：返回复制字符的数量，不包括截尾的空字节

利用win32gui.PyMakeBuffer(len, addr)可以造一个buffer对象，类似python3中的bytearray，lParam的返回值。而利用WM_GETTEXTLENGTH可以获取不含截尾空字节的文本长度的长度，可以用来设置Buffer的长度。完整的示例如下：

```python
buf_size = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1  # 要加上截尾的字节
str_buffer = win32gui.PyMakeBuffer(buf_size)  # 生成buffer对象
win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, str_buffer)  # 获取buffer
str = str(str_buffer[:-1])  # 转为字符串
```



#### 控件操作B

至于另存为图片，情况要稍微复杂一点，因为另存为图片的默认选项是BMP，特别不巧，我使用的FaceGen版本保存为BMP有BUG，不能成功保存，所以我们除了定位保存文件的路径以外，还需要对文件类型的下拉组合框(ComboBox进)行操作：

我们假设我们找到了组合框的句柄为CB_handle，我们可以用CB_SETCURSEL消息来更改当前的选项：

- CB_SETCURSEL 消息
    - 描述：
    - 参数：
        - wParam：以0起始的待选选项的索引；如果该值为-1，将从组合框列表中删除当前选项，并使当前选项为空
        - lParam：未使用。
    - 返回值：
        - 更改选择成功将返回所设置选项的索引号。

只要给组合框发一个CB_SETCURSEL消息，你就会发现下拉列表的选项已经改变了。

这时，只要你点保存，你就会发现，这保存的跟之前的一样啊！根本没有变！

问题在哪里？

我们用鼠标或者键盘操作一下，是没有问题的，一旦更保存类型，保存窗口里的预览也会随之变化。所以，除了CB_SETCURSEL以外，一定还缺了点儿什么。

于是，我们可以调用Spy++的消息机制查看一下手动操作时，我们的下拉组合框发生的事情，好像除了渲染和点击，没有什么特别值得注意的。

那再看看父窗体呢？好像有点儿不太一样的东西：

- CBN_SELENDOK 通知（notification code）
    - 描述：当用户选择了有效的列表项时发送，提示父窗体处理用户的选择。父窗体通过WM_COMMAND消息接收这个通知。
    - 参数：（作为WM_COMMAND的参数）
        - wParam：LOWORD为组合框的ID. HIWORD为CBN_SELENDOK的值。
        - lParam：组合框的句柄。
- CBN_SELCHANGE 通知（notification code）
    - 描述：当用户更改了列表项的选择时发送，不论用户是通过鼠标选择或是通过方向键选择都会发送此通知。父窗体通过WM_COMMAND消息接收这个通知。
    - 参数：（作为WM_COMMAND的参数）
        - wParam：LOWORD为组合框的ID. HIWORD为CBN_SELCHANGE的值。
        - lParam：组合框的句柄。
- 说明：他们是WM_COMMAND消息wParam的high word（wParam的16-31位，详情参见Part 2）的常数之一，在Python中可以用位移操作将其移动到高位上（a<<16），再用加法加上低位的内容。

继续查MSDN的资料，我们发现，对于一个有效的选择，一定会发送这两个通知，发送完CBN*SELENDOK以后马上发送CBN\*SELCHANGE。而且，使用CB\*SETCURSEL消息时，CBN\*SELCHANGE通知是**不会**被送达的！

问题就在这里，加上这两个消息之后，就能正常操作下拉菜单了。完整函数如下

```python
    def save_to_image(self, filePath, format="jpg"):
        format_dict = {
            "bmp": 0,  # Facegen的Bug导致无法保存bmp
            "jpg": 1,
            "tga": 2,
            "tif": 3,
        }
        Mhandle, confirmBTN_handle = self.menu_command('save_to_image')
        mhandle = find_subHandle(Mhandle, [("DUIViewWndClassName", 0), ("DirectUIHWND", 0)])
        EDIT_handle = find_subHandle(mhandle, [("FloatNotifySink", 0), ("ComboBox", 0), ("Edit", 0)])  # 定位保存地址句柄
        PCB_handle = find_subHandle(mhandle, [("FloatNotifySink", 1)])  # 定位下拉菜单父窗体句柄
        CB_handle = find_subHandle(PCB_handle, [("ComboBox", 0)])  # 定位下拉菜单窗体句柄
        wait_and_assert(EDIT_handle, find_subHandle(mhandle, [("FloatNotifySink", 0), ("ComboBox", 0), ("Edit", 0)]))
        # 以下3行皆为ComboBox的list中选择格式必要的Message操作
        if win32api.SendMessage(CB_handle, win32con.CB_SETCURSEL, format_dict[format], 0) == format_dict[format]:
            win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, 0x90000, CB_handle)
            win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, 0x10000, CB_handle)
        else:
            raise Exception("Change saving type failed")
        # 填入保存地址，确认
        if win32api.SendMessage(EDIT_handle, win32con.WM_SETTEXT, 0, os.path.abspath(filePath).encode('gbk')) == 1:
            return win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle)
        raise Exception("Set file opening path failed")
```



#### 范例脚本：

```python
import win32gui
import win32con
import win32api
 
# 从顶层窗口向下搜索主窗口，无法搜索子窗口
# FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
handle = win32gui.FindWindow("Notepad", None) 
 
 
# 获取窗口位置
left, top, right, bottom = win32gui.GetWindowRect(handle)
 
#获取某个句柄的类名和标题
title = win32gui.GetWindowText(handle)     
clsname = win32gui.GetClassName(handle)
 
# 打印句柄
# 十进制
print(handle)
# 十六进制
print("%x" %(handle) )
 
 
# 搜索子窗口
# 枚举子窗口
hwndChildList = []     
win32gui.EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd),  hwndChildList)
 
# FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None) 
# 父窗口句柄 若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。 子窗口类名 子窗口标题
subHandle = win32gui.FindWindowEx(handle, 0, "EDIT", None)
 
# 获得窗口的菜单句柄
menuHandle = win32gui.GetMenu(subHandle)
 
# 获得子菜单或下拉菜单句柄   
# 参数：菜单句柄 子菜单索引号
subMenuHandle = win32gui.GetSubMenu(menuHandle, 0)
 
# 获得菜单项中的的标志符，注意，分隔符是被编入索引的  
# 参数：子菜单句柄 项目索引号 
menuItemHandle = win32gui.GetMenuItemID(subMenuHandle, 0)
 
# 发送消息，加入消息队列，无返回 
# 参数：句柄 消息类型 WParam IParam
win32gui.postMessage(subHandle, win32con.WM_COMMAND, menuItemHandle, 0)
 
# wParam的定义是32位整型，high word就是他的31至16位，low word是它的15至0位。
# 当参数超过两个，wParam和lParam不够用时，可以将wParam就给拆成两个int16来使用。
# 这种时候在python里记得用把HIWORD的常数向左移16位，再加LOWORD，即wParam = HIWORD<<16+LOWORD。
 
 
# 下选框内容更改
# 参数：下选框句柄； 消息内容； 
#参数下选框的哪一个item，以0起始的待选选项的索引；如果该值为-1，将从组合框列表中删除当前选项，并使当前选项为空；
# 参数CB_Handle为下选框句柄，PCB_handle下选框父窗口句柄
if win32api.SendMessage(CB_handle, win32con.CB_SETCURSEL, 1, 0) == 1:
 
# 下选框的父窗口命令
# 参数：父窗口句柄； 命令； 
# 参数：WParam：高位表示类型，低位表示内容；参数IParam，下选框句柄
# CBN_SELENDOK当用户选择了有效的列表项时发送，提示父窗体处理用户的选择。 LOWORD为组合框的ID. HIWORD为CBN_SELENDOK的值。
            win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, 0x90000, CB_handle) 
# CBN_SELCHANGE当用户更改了列表项的选择时发送，不论用户是通过鼠标选择或是通过方向键选择都会发送此通知。LOWORD为组合框的ID. HIWORD为CBN_SELCHANGE的值。
            win32api.SendMessage(PCB_handle, win32con.WM_COMMAND, 0x10000, CB_handle) 
 
 
# 设置文本框内容，等窗口处理完毕后返回true。中文需编码成gbk 
# 参数：句柄；消息类型；
# 参数WParam，无需使用； 
# 参数IParam，要设置的内容，字符串
win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, os.path.abspath(fgFilePath).encode('gbk'))
 
 
# 控件点击确定,处理消息后返回0
# 参数:窗口句柄; 消息类型; 参数WParam HIWORD为0（未使用），LOWORD为控件的ID; 参数IParam  0（未使用）,确定控件的句柄
win32api.SendMessage(Mhandle, win32con.WM_COMMAND, 1, confirmBTN_handle)
 
 
# 获取窗口文本不含截尾空字符的长度
# 参数：窗口句柄； 消息类型； 参数WParam； 参数IParam
bufSize = win32api.SendMessage(subHandle, win32con.WM_GETTEXTLENGTH, 0, 0) +1
 
# 利用api生成Buffer
strBuf = win32gui.PyMakeBuffer(bufSize)
print(strBuf)
 
# 发送消息获取文本内容
# 参数：窗口句柄； 消息类型；文本大小； 存储位置
length = win32gui.SendMessage(subHandle, win32con.WM_GETTEXT, bufSize, strBuf)
 
# 反向内容，转为字符串
# text = str(strBuf[:-1])
 
address, length = win32gui.PyGetBufferAddressAndLen(strBuf) 
text = win32gui.PyGetString(address, length) 
# print('text: ', text)
 
# 鼠标单击事件
#鼠标定位到(30,50)
win32api.SetCursorPos([30,150])
 
#执行左单键击，若需要双击则延时几毫秒再点击一次即可
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
 
#右键单击
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
 
def click1(x,y):                #第一种
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
 
def click2(x,y):               #第二种
    ctypes.windll.user32.SetCursorPos(x,y)
    ctypes.windll.user32.mouse_event(2,0,0,0,0)
    ctypes.windll.user32.mouse_event(4,0,0,0,0)
 
def click_it(pos):          #第三种
    handle= win32gui.WindowFromPoint(pos)
    client_pos =win32gui.ScreenToClient(handle,pos)
    tmp=win32api.MAKELONG(client_pos[0],client_pos[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,tmp)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,tmp)
 
# 发送回车
win32api.keybd_event(13,0,0,0)
win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
 
# 关闭窗口
win32gui.PostMessage(win32lib.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
 
 
# 检查窗口是否最小化，如果是最大化
if(win32gui.IsIconic(hwnd)):
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.ShowWindow(hwnd, 8)
    sleep(0.5)
 
# SW_HIDE：隐藏窗口并激活其他窗口。nCmdShow=0。
# SW_MAXIMIZE：最大化指定的窗口。nCmdShow=3。
# SW_MINIMIZE：最小化指定的窗口并且激活在Z序中的下一个顶层窗口。nCmdShow=6。
# SW_RESTORE：激活并显示窗口。如果窗口最小化或最大化，则系统将窗口恢复到原来的尺寸和位置。在恢复最小化窗口时，应用程序应该指定这个标志。nCmdShow=9。
# SW_SHOW：在窗口原来的位置以原来的尺寸激活和显示窗口。nCmdShow=5。
# SW_SHOWDEFAULT：依据在STARTUPINFO结构中指定的SW_FLAG标志设定显示状态，STARTUPINFO 结构是由启动应用程序的程序传递给CreateProcess函数的。nCmdShow=10。
# SW_SHOWMAXIMIZED：激活窗口并将其最大化。nCmdShow=3。
# SW_SHOWMINIMIZED：激活窗口并将其最小化。nCmdShow=2。
# SW_SHOWMINNOACTIVE：窗口最小化，激活窗口仍然维持激活状态。nCmdShow=7。
# SW_SHOWNA：以窗口原来的状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=8。
# SW_SHOWNOACTIVATE：以窗口最近一次的大小和状态显示窗口。激活窗口仍然维持激活状态。nCmdShow=4。
# SW_SHOWNORMAL：激活并显示一个窗口。如果窗口被最小化或最大化，系统将其恢复到原来的尺寸和大小。应用程序在第一次显示窗口的时候应该指定此标志。nCmdShow=1。
```



```python
from pymouse import PyMouse
from pykeyboard import PyKeyboard
#实例化
m = PyMouse()       
k = PyKeyboard()
 
x_dim, y_dim = m.screen_size()
# 鼠标点击 参数:x,y,button=1(左键)、2(右键)、3(中间),次数
m.click(x_dim, y_dim, button=1,n=1)  
# 键盘输入 参数:str,间隔
k.type_string('Hello, World!',interval=0)
 
# 按住一个键
k.press_key('H')
# 松开一个键
k.release_key('H')
 
# 相当于===>按住并松开，tap一个键
k.tap_key('e')
# tap支持重复的间歇点击键,参数:str,次数,间隔
k.tap_key('l',n=2,interval=5) 
 
#创建组合键===>press_key和release_key结合使用
k.press_key(k.alt_key)
k.tap_key(k.tab_key)
k.release_key(k.alt_key)
 
# 特殊功能键
k.tap_key(k.function_keys[5]) # Tap F5
k.tap_key(k.numpad_keys['Home']) # Tap 'Home' on the numpad
k.tap_key(k.numpad_keys[5], n=3) # Tap 5 on the numpad, thrice
 
# Mac系统按键
k.press_keys(['Command','shift','3'])
# Windows系统按键
k.press_keys([k.windows_l_key,'d'])
 
其中pymouse的PyMouseEvent和pykeyboard的PyKeyboardEvent还可用于监听鼠标和键盘事件的输入
class Clickonacci(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.fibo = fibo()
 
    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if button == 1:
            if press:
                print('Press times:%d'.format(press))
        else: # Exit if any other mouse button used
            self.stop()
 
C = Clickonacci()
C.run()
 
class TapRecord(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
 
    def tap(self, keycode, character, press):
        print(time.time(), keycode, character, press)
 
t = TapRecord()
t.run()
#这些对象是一个架构用于监听鼠标和键盘的输入；他们除了监听之外不会做任何事，需要继承重构他们#PyKeyboardEvent为编写完成，所以这里是一个继承PyMouseEvent的例子：
```



使用这三个模块 win32api, win32con, win32gui 以及from ctypes import windll

```python
import win32api
import win32con
import win32gui
from ctypes import windll
from time import sleep
12345
```

下面就贴上一些我常用的功能
注：贴上的都是简单封装的函数作为示例，可以直接拿去用，也可以自己重新优化，主要是整理在一次供参考，给出一些思路。

##### 1. 获取当前坐标

```python
   def get_point():
       point = win32api.GetCursorPos()
       return point
123
```

##### 2. 移动鼠标至指定坐标位

```python
	def mouse_move(x, y):
	    windll.user32.SetCursorPos(x, y)
12
```

##### 3. 鼠标左键单击

这里需要注意的是，下面最后两行是鼠标的按下和弹起，需要点击某个坐标的话可以配合用2中的移动鼠标来实现点击

```python
    def mouse_click(self, x=None, y=None):
        if not x is None and not y is None:
            self.mouse_move(x, y)
            sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
123456
```

##### 4. 获取所有的窗口句柄

```python
    def get_window_handlers():
        handlers = []
        win32gui.EnumWindows(lambda handler, param: param.append(handler), handlers)
        return handlers
1234
```

##### 5. 获取指定窗口的大小

入参是指定窗口句柄

```python
    def get_window_size(handler):
        location_size = win32gui.GetWindowRect(handler)
        return location_size
123
```

##### 6. 设置指定窗口的大小

第一个参数是指定窗口句柄， 后四个是坐标位置
分别是起点x，起点y，终点x，终点y
例如0,0,800,600就是在屏幕左上角开始设置宽800，高600的窗口

```python
    def set_window(handler, start_x, start_y, size_x, size_y):
        win32gui.SetWindowPos(handler, win32con.HWND_TOPMOST, start_x, start_y, size_x, size_y, win32con.SWP_SHOWWINDOW)
12
```

##### 7. 根据应用窗口名找到窗口控件编号（单个）

注：用win32gui的FindWindow方法查找有一个缺点，就是当有重名的窗口时只会找到一个

```python
    def find_window_by_title(title):
        window_found = win32gui.FindWindow(None, title)
        return window_found
123
```

##### 8. 根据应用窗口名找到窗口控件编号（多个）

由于win32gui的FindWindow方法的缺点，自己封装一个查找指定名称窗口们的方法

```python
    def find_windows_by_title(self, title):
        windows = []
        handlers = self.get_window_handlers()
        for handler in handlers:
            if win32gui.GetWindowText(handler) == title:
                windows.append(handler)
        return windows
1234567
```

##### 9. 获取所有窗口的标题名

这个方法我用于确认是否成功双开阴阳师
入参是所有的handler，可以结合第4点来实现

```python
    def get_window_title_all(handlers):
        titles = []
        for handler in handlers:
            title = win32gui.GetWindowText(handler)
            titles.append(title)
        return title
```



## 2. 进程监控



## 3. 截图 & 图形切割



```python
def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
# 注意，一定要在管理员权限下的cmd中运行，否则点击无效
```



定位窗口

```python

import win32gui
def get_window_info():  # 获取阴阳师窗口信息
    wdname = u'阴阳师-网易游戏'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '小轩提示：请打开PC端阴阳师\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)

#get_window_info()函数返回阴阳师窗口信息(x1, y1, x2, y2)，(x1, y1)是窗口左上角的坐标，(x2, y2)是窗口右下角的坐标，代码中的text可以暂时忽略，这在后续GUI界面中用于输出提示信息。
```



使用PIL获取游戏截图

```python
def get_posx(x, window_size):  # 返回x相对坐标
    return (window_size[2] - window_size[0]) * x / 870


def get_posy(y, window_size):  # 返回y相对坐标
    return (window_size[3] - window_size[1]) * y / 520

topx, topy = window_size[0], window_size[1]
img_ready = ImageGrab.grab((topx + get_posx(500, window_size), topy + get_posy(480, window_size),
                            topx + get_posx(540, window_size), topy + get_posy(500, window_size)))
# 查看图片
im_ready.show()
```



考虑到窗口大小不同，位置会有所偏移，这里使用屏幕上点的相对位置
获取到关键位置的截图之后，计算图片的hash值

```python
def get_hash(img):
    img = img.resize((16, 16), Image.ANTIALIAS).convert('L')  # 抗锯齿 灰度
    avg = sum(list(img.getdata())) / 256  # 计算像素平均值
    s = ''.join(map(lambda i: '0' if i < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
    return ''.join(map(lambda j: '%x' % int(s[j:j+4], 2), range(0, 256, 4)))
```





## 4. 图像识别 & 位置匹配

关键位置截图的hash值保存下来，下次脚本运行时，将截图hash值与原始hash值进行比对，判断是否相似。
这里使用汉明距离进行计算，比较hash值中相同位置上不同元素的个数

```python
def hamming(hash1, hash2, n=20):
    b = False
    assert len(hash1) == len(hash2)
    if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) < n:
        b = True
    return b
```







## 5. 文字识别 & 位置匹配



## 6. 鼠标操作



### win32api

范例代码：

```python
import win32api
import time
def move_click(x, y, t=0):  # 移动鼠标并点击左键
    win32api.SetCursorPos((x, y))  # 设置鼠标位置(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
    if t == 0:
        time.sleep(random.random()*2+1)  # sleep一下
    else:
        time.sleep(t)
    return 0

# 测试
move_click(30, 30)

# 写个while循环，不停地点击屏幕上不同的几个点了
```





## 7. 键盘操作



## 8. 随机函数的使用





## 實際案例

Python实现自动挂机脚本（基础篇）

```python
def yu_ling(window_size):
    global is_start
    topx, topy = window_size[0], window_size[1]
    state = []

    while is_start:
        # print 'start'
        # text.insert('end', 'start')
        time.sleep(0.5)
        img_ready = ImageGrab.grab((topx + get_posx(750, window_size), topy + get_posy(465, window_size),
                                    topx + get_posx(840, window_size), topy + get_posy(500, window_size)))
        if hamming(get_hash(img_ready), ready_hash, 10):
            state.append(0)
            move_click(topx + get_posx(740, window_size), topy + get_posy(380, window_size))
            text.insert('end', strftime('%H:%M:%S', localtime()) + ' 点击准备\n')
            text.see('end')  # 自动显示底部
            time.sleep(15)
            continue

        img_success = ImageGrab.grab((topx + get_posx(400, window_size), topy + get_posy(320, window_size),
                                      topx + get_posx(470, window_size), topy + get_posy(400, window_size)))
        if hamming(get_hash(img_success), success_hash):
            time.sleep(2)
            state.append(1)
            text.insert('end', strftime('%H:%M:%S', localtime()) + ' 成功%d次\n' % state.count(1))
            text.see('end')  # 自动显示底部
            move_click(topx + get_posx(730, window_size), topy + get_posy(380, window_size))
            continue

        img_fail = ImageGrab.grab((topx + get_posx(560, window_size), topy + get_posy(340, window_size),
                                   topx + get_posx(610, window_size), topy + get_posy(390, window_size)))
        if hamming(get_hash(img_fail), fail_hash):
            time.sleep(2)
            state.append(2)
            text.insert('end', strftime('%H:%M:%S', localtime()) + ' 失败%d次\n' % state.count(2))
            text.see('end')  # 自动显示底部
            move_click(topx + get_posx(720, window_size), topy + get_posy(380, window_size))
            continue

        img_attack = ImageGrab.grab((topx + get_posx(615, window_size), topy + get_posy(350, window_size),
                                     topx + get_posx(675, window_size), topy + get_posy(375, window_size)))
        if hamming(get_hash(img_attack), yu_attack_hash):
            move_click(topx + get_posx(670, window_size), topy + get_posy(365, window_size))
            text.insert('end', strftime('%H:%M:%S', localtime()) + ' 点击进攻\n')
            text.see('end')  # 自动显示底部
            state.append(3)
            if state[-6:] == [3]*6:
                text.insert('end', strftime('%H:%M:%S', localtime()) + ' 痴汉券可能不够了\n')
                text.see('end')  # 自动显示底部
                click()
                break
            continue
```

