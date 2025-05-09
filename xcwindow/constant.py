# -*- coding: utf-8 -*-
"""
 - file: constant.py
 - window-styles from: https://learn.microsoft.com/zh-cn/windows/win32/winmsg/window-styles
"""


class Constant:
    """ Windows 常量 """

    """ 窗口具有细线边框 """
    WS_BORDER = 0x00800000

    """ 窗口具有标题栏（包括 WS_BORDER 样式）。 """
    WS_CAPTION = 0x00C00000

    """ 窗口是子窗口。 具有此样式的窗口不能有菜单栏。 此样式不能与 WS_POPUP 样式一起使用。 """
    WS_CHILD = 0x40000000  #

    """ 与 WS_CHILD 样式相同。 """
    WS_CHILDWINDOW = 0x40000000  #

    """ 在父窗口内进行绘图时，不包括子窗口所占用的区域。 创建父窗口时使用此样式。 """
    WS_CLIPCHILDREN = 0x02000000  #

    """
    相对于彼此剪裁子窗口；也就是说，当特定子窗口收到 WM_PAINT 消息时，WS_CLIPSIBLINGS 样式会将所有其他重叠的子窗口剪裁出要更新的子窗口的区域。
    如果 未指定 WS_CLIPSIBLINGS 并且子窗口重叠，则在子窗口的工作区内绘图时，有可能在相邻子窗口的工作区内绘图。
    """
    WS_CLIPSIBLINGS = 0x04000000  #

    """ 窗口最初处于禁用状态。 禁用的窗口无法接收用户的输入。 若要在创建窗口后更改此值，请使用 EnableWindow 函数。 """
    WS_DISABLED = 0x08000000  #

    """ 窗口的边框样式通常与对话框相同。 具有此样式的窗口不能有标题栏。 """
    WS_DLGFRAME = 0x00400000  #

    """
    窗口是一组控件中的第一个控件。
    该组包含此第一个控件及其之后定义的所有控件，直到下一个具有 WS_GROUP 样式的控件。
    每个组中的第一个控件通常具有 WS_TABSTOP 样式，以便用户可以从组移动到组。
    随后，用户可以使用方向键将键盘焦点从组中的一个控件切换为组中的下一个控件。
    您可以打开和关闭此样式以更改对话框导航。 若要在创建窗口后更改此样式，请使用 SetWindowLong 函数。
    """
    WS_GROUP = 0x00020000  #

    """ 窗口具有水平滚动条。 """
    WS_HSCROLL = 0x00100000  #

    """ 窗口最初是最小化的。 与 WS_MINIMIZE 样式相同。 """
    WS_ICONIC = 0x20000000  #

    """ 窗口最初是最大化的。 """
    WS_MAXIMIZE = 0x01000000  #

    """ 窗口具有最大化按钮。 不能与 WS_EX_CONTEXTHELP 样式组合。 还必须指定 WS_SYSMENU 样式。 """
    WS_MAXIMIZEBOX = 0x00010000  #

    """ 窗口最初是最小化的。 与 WS_ICONIC 样式相同。 """
    WS_MINIMIZE = 0x20000000  #

    """ 窗口具有最小化按钮。 不能与 WS_EX_CONTEXTHELP 样式组合。 还必须指定 WS_SYSMENU 样式。 """
    WS_MINIMIZEBOX = 0x00020000  #

    """ 窗口是重叠的窗口。 重叠的窗口带有标题栏和边框。 与 WS_TILED 样式相同。 """
    WS_OVERLAPPED = 0x00000000  #

    """ 窗口是弹出窗口。 此样式不能与 WS_CHILD 样式一起使用。 """
    WS_POPUP = 0x80000000  #

    """ 窗口具有大小调整边框。 与 WS_THICKFRAME 样式相同。 """
    WS_SIZEBOX = 0x00040000  #

    """ 该窗口的标题栏上有一个窗口菜单。 还必须指定 WS_CAPTION 样式。 """
    WS_SYSMENU = 0x00080000  #

    """
    窗口是一个控件，当用户按下 Tab 键时，该控件可以接收键盘焦点。
    按下 Tab 键可将键盘焦点更改为具有 WS_TABSTOP 样式的下一个控件。
    您可以打开和关闭此样式以更改对话框导航。
    若要在创建窗口后更改此样式，请使用 SetWindowLong 函数。
    要使用户创建的窗口和无模式对话框能够使用制表位，请更改消息循环以调用 IsDialogMessage 函数。
    """
    WS_TABSTOP = 0x00010000  #

    """ 窗口具有大小调整边框。 与 WS_SIZEBOX 样式相同。 """
    WS_THICKFRAME = 0x00040000  #

    """ 窗口是重叠的窗口。 重叠的窗口带有标题栏和边框。 与 WS_OVERLAPPED 样式相同。 """
    WS_TILED = 0x00000000  #

    """ 窗口是重叠的窗口。 与 WS_OVERLAPPEDWINDOW 样式相同。 """
    WS_TILEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX  #

    """ 窗口最初可见。可以使用 ShowWindow 或 SetWindowPos 函数打开和关闭此样式。 """
    WS_VISIBLE = 0x10000000  #

    """ 窗口具有垂直滚动条。 """
    WS_VSCROLL = 0x00200000  #

    """ 窗口是重叠的窗口。 与 WS_TILEDWINDOW 样式相同。 """
    WS_OVERLAPPEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX  #

    """ 窗口是弹出窗口。 必须组合 WS_CAPTION 和 WS_POPUPWINDOW 样式以使窗口菜单可见。 """
    WS_POPUPWINDOW = (WS_POPUP | WS_BORDER | WS_SYSMENU)

    WS_EX_CLIENTEDGE = 0x00000200

    WM_DESTROY = 0x0002

    WM_CLOSE = 0x0010

    WM_SIZE = 0x0005

    WM_PAINT = 0x000F

    WM_CREATE = 0x0001

    CW_USEDEFAULT = 0x80000000

    CS_HREDRAW = 0x0002

    CS_VREDRAW = 0x0001

    COLOR_WINDOW = 5

    IDI_APPLICATION = 32512

    IDC_ARROW = 32512

    WHITE_BRUSH = 0

    LR_LOADFROMFILE = 0x00000010

    IMAGE_ICON = 1

    MB_OKCANCEL = 0x00000001

    IDOK = 1

    GWLP_USERDATA = -21

    def LOWORD(value):
        return value & 0xFFFF

    def HIWORD(value: int) -> int:
        return (value >> 16) & 0xFFFF
