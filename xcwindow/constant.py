# -*- coding: utf-8 -*-
"""
Windows API 常量定义

参考:
- Window Styles: https://learn.microsoft.com/en-us/windows/win32/winmsg/window-styles
- Window Class Styles: https://learn.microsoft.com/en-us/windows/win32/winmsg/window-class-styles
- System Colors: https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-colors
"""

from typing import ClassVar


class Constant:
    """
    Windows API 常量定义类

    包含:
    - 窗口样式 (WS_*)
    - 窗口类样式 (CS_*)
    - 系统颜色 (COLOR_*)
    - 资源标识符 (IDI_*, IDC_*)
    - 消息常量 (WM_*)
    - 实用方法 (LOWORD, HIWORD)
    """

    # 窗口样式常量
    WS_BORDER: ClassVar[int] = 0x00800000
    """窗口具有细线边框"""

    WS_CAPTION: ClassVar[int] = 0x00C00000
    """窗口具有标题栏(包括WS_BORDER样式)"""

    WS_CHILD: ClassVar[int] = 0x40000000
    """
    窗口是子窗口
    - 具有此样式的窗口不能有菜单栏
    - 不能与WS_POPUP样式一起使用
    """

    WS_CHILDWINDOW: ClassVar[int] = WS_CHILD
    """与WS_CHILD样式相同"""

    WS_CLIPCHILDREN: ClassVar[int] = 0x02000000
    """在父窗口内绘图时排除子窗口区域"""

    WS_CLIPSIBLINGS: ClassVar[int] = 0x04000000
    """
    剪裁重叠的子窗口
    - 当子窗口收到WM_PAINT消息时，剪裁其他重叠子窗口
    - 未设置此样式时，可能在相邻子窗口工作区内绘图
    """

    WS_DISABLED: ClassVar[int] = 0x08000000
    """窗口初始禁用，无法接收用户输入"""

    WS_DLGFRAME: ClassVar[int] = 0x00400000
    """对话框样式的边框(无标题栏)"""

    WS_GROUP: ClassVar[int] = 0x00020000
    """
    控件组起始标志
    - 标识一组控件的开始
    - 通常与WS_TABSTOP配合使用
    - 可使用方向键在组内导航
    """

    WS_HSCROLL: ClassVar[int] = 0x00100000
    """窗口具有水平滚动条"""

    WS_ICONIC: ClassVar[int] = 0x20000000
    """窗口初始最小化(同WS_MINIMIZE)"""

    WS_MAXIMIZE: ClassVar[int] = 0x01000000
    """窗口初始最大化"""

    WS_MAXIMIZEBOX: ClassVar[int] = 0x00010000
    """
    窗口具有最大化按钮
    - 需要同时指定WS_SYSMENU样式
    - 不能与WS_EX_CONTEXTHELP一起使用
    """

    WS_MINIMIZE: ClassVar[int] = 0x20000000
    """窗口初始最小化(同WS_ICONIC)"""

    WS_MINIMIZEBOX: ClassVar[int] = 0x00020000
    """
    窗口具有最小化按钮
    - 需要同时指定WS_SYSMENU样式
    - 不能与WS_EX_CONTEXTHELP一起使用
    """

    WS_OVERLAPPED: ClassVar[int] = 0x00000000
    """重叠窗口(带标题栏和边框)"""

    WS_POPUP: ClassVar[int] = 0x80000000
    """
    弹出窗口
    - 不能与WS_CHILD样式一起使用
    """

    WS_SIZEBOX: ClassVar[int] = 0x00040000
    """窗口具有大小调整边框(同WS_THICKFRAME)"""

    WS_SYSMENU: ClassVar[int] = 0x00080000
    """
    窗口具有系统菜单
    - 需要同时指定WS_CAPTION样式
    """

    WS_TABSTOP: ClassVar[int] = 0x00010000
    """
    Tab键可停驻控件
    - 允许用户通过Tab键导航
    """

    WS_THICKFRAME: ClassVar[int] = 0x00040000
    """窗口具有大小调整边框(同WS_SIZEBOX)"""

    WS_TILED: ClassVar[int] = 0x00000000
    """平铺窗口(同WS_OVERLAPPED)"""

    WS_TILEDWINDOW: ClassVar[int] = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
    """标准重叠窗口样式组合"""

    WS_VISIBLE: ClassVar[int] = 0x10000000
    """窗口初始可见"""

    WS_VSCROLL: ClassVar[int] = 0x00200000
    """窗口具有垂直滚动条"""

    WS_OVERLAPPEDWINDOW: ClassVar[int] = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
    """标准重叠窗口样式组合(同WS_TILEDWINDOW)"""

    WS_POPUPWINDOW: ClassVar[int] = WS_POPUP | WS_BORDER | WS_SYSMENU
    """标准弹出窗口样式组合"""

    # 窗口扩展样式
    WS_EX_CLIENTEDGE: ClassVar[int] = 0x00000200
    """窗口具有3D边框样式"""

    # 窗口消息常量
    WM_DESTROY: ClassVar[int] = 0x0002
    """窗口销毁消息"""

    WM_CLOSE: ClassVar[int] = 0x0010
    """窗口关闭消息"""

    WM_SIZE: ClassVar[int] = 0x0005
    """窗口大小改变消息"""

    WM_PAINT: ClassVar[int] = 0x000F
    """窗口绘制消息"""

    WM_CREATE: ClassVar[int] = 0x0001
    """窗口创建消息"""

    # 窗口创建常量
    CW_USEDEFAULT: ClassVar[int] = 0x80000000
    """使用默认窗口位置/大小"""

    # 窗口类样式
    CS_HREDRAW: ClassVar[int] = 0x0002
    """水平调整大小时重绘整个窗口"""

    CS_VREDRAW: ClassVar[int] = 0x0001
    """垂直调整大小时重绘整个窗口"""

    # 系统颜色
    COLOR_WINDOW: ClassVar[int] = 5
    """窗口背景颜色"""

    # 系统资源常量
    IDI_APPLICATION: ClassVar[int] = 32512
    """默认应用程序图标"""

    IDC_ARROW: ClassVar[int] = 32512
    """标准箭头光标"""

    WHITE_BRUSH: ClassVar[int] = 0
    """白色画刷"""

    LR_LOADFROMFILE: ClassVar[int] = 0x00000010
    """从文件加载资源标志"""

    IMAGE_ICON: ClassVar[int] = 1
    """图标资源类型"""

    # 对话框常量
    MB_OKCANCEL: ClassVar[int] = 0x00000001
    """确定/取消消息框"""

    IDOK: ClassVar[int] = 1
    """确定按钮ID"""

    # 窗口属性
    GWLP_USERDATA: ClassVar[int] = -21
    """窗口用户数据指针索引"""

    @staticmethod
    def LOWORD(value: int) -> int:
        """
        获取32位值的低16位

        参数:
            value: 32位整数值

        返回:
            低16位值
        """
        return value & 0xFFFF

    @staticmethod
    def HIWORD(value: int) -> int:
        """
        获取32位值的高16位

        参数:
            value: 32位整数值

        返回:
            高16位值
        """
        return (value >> 16) & 0xFFFF
