import ctypes
import ctypes.wintypes as wintypes
import os
from uuid import uuid4
from enum import Enum, auto
from typing import Optional, Tuple, Union
from .error import XCRegisterClassError, XCCreateWindowError, XCLoadIconWarning
from .constant import Constant

# 类型别名定义
HICON = wintypes.HANDLE
HWND = wintypes.HWND
HINSTANCE = wintypes.HINSTANCE
ATOM = wintypes.ATOM

dwmapi = ctypes.windll.dwmapi
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 确保DefWindowProcW函数原型正确
user32.DefWindowProcW.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
]
user32.DefWindowProcW.restype = ctypes.c_long

WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_long,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM
)


class WNDCLASSEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HANDLE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HANDLE),
    ]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", wintypes.HDC),
        ("fErase", wintypes.BOOL),
        ("rcPaint", wintypes.RECT),
        ("fRestore", wintypes.BOOL),
        ("fIncUpdate", wintypes.BOOL),
        ("rgbReserved", ctypes.c_byte * 32),
    ]


class CREATESTRUCTW(ctypes.Structure):
    _fields_ = [
        ("lpCreateParams", wintypes.LPVOID),
        ("hInstance", wintypes.HINSTANCE),
        ("hMenu", wintypes.HMENU),
        ("hwndParent", wintypes.HWND),
        ("cy", ctypes.c_int),
        ("cx", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x", ctypes.c_int),
        ("style", ctypes.c_long),
        ("lpszName", wintypes.LPCWSTR),
        ("lpszClass", wintypes.LPCWSTR),
        ("dwExStyle", wintypes.DWORD),
    ]



class DWMWINDOWATTRIBUTE(Enum):
    DWMWA_NCRENDERING_ENABLED = auto()
    DWMWA_NCRENDERING_POLICY = auto()
    DWMWA_TRANSITIONS_FORCEDISABLED = auto()
    DWMWA_ALLOW_NCPAINT = auto()
    DWMWA_CAPTION_BUTTON_BOUNDS = auto()
    DWMWA_NONCLIENT_RTL_LAYOUT = auto()
    DWMWA_FORCE_ICONIC_REPRESENTATION = auto()
    DWMWA_FLIP3D_POLICY = auto()
    DWMWA_EXTENDED_FRAME_BOUNDS = auto()
    DWMWA_HAS_ICONIC_BITMAP = auto()
    DWMWA_DISALLOW_PEEK = auto()
    DWMWA_EXCLUDED_FROM_PEEK = auto()
    DWMWA_CLOAK = auto()
    DWMWA_CLOAKED = auto()
    DWMWA_FREEZE_REPRESENTATION = auto()
    DWMWA_PASSIVE_UPDATE_MODE = auto()
    DWMWA_USE_HOSTBACKDROPBRUSH = auto()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = auto()
    DWMWA_CAPTION_COLOR = auto()
    DWMWA_TEXT_COLOR = auto()
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = auto()
    DWMWA_SYSTEMBACKDROP_TYPE = auto()
    DWMWA_LAST = auto()


LONG_PTR  = ctypes.c_long


class StateInfo(ctypes.Structure):
    _fields_ = []


def _get_python_icon_path() -> str:
    return os.path.abspath(r".\xcwindow\assets\pyc.ico")


class XCWindowBase:
    def __init__(self,
                width: int,
                height: int,
                title: str = "XCWindow",
                icon_path: str = _get_python_icon_path(),
                class_name: str = f"XCWindow-{uuid4()}") -> None:
        """
        初始化窗口基类

        参数:
            width: 窗口宽度
            height: 窗口高度
            title: 窗口标题
            icon_path: 图标路径
            class_name: 窗口类名
        """
        self._DWMWINDOWATTRIBUTE = DWMWINDOWATTRIBUTE
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.icon_path: str = icon_path
        self.class_name: str = class_name

        self.g_wnd_proc: Optional[WNDPROC] = None
        self.g_icon_handles: Tuple[Optional[HICON], Optional[HICON]] = (None, None)
        self.hwnd: Optional[HWND] = None
        self.wc: Optional[WNDCLASSEX] = None

        # 设置错误模式
        kernel32.SetErrorMode(0x0001 | 0x0002)

        # 初始化消息结构
        self.msg: wintypes.MSG = wintypes.MSG()
        self.pMsg = ctypes.byref(self.msg)

        # 注册窗口类并创建窗口
        self._register_class(self.class_name, self.icon_path)
        self._init_window(self.class_name, self.title, self.width, self.height)

    def show(self) -> None:
        """
        显示窗口

        注意:
            调用此方法将使窗口可见并更新窗口
        """
        if not self.hwnd:
            raise RuntimeError("窗口尚未创建")

        user32.ShowWindow(self.hwnd, 1)  # SW_SHOWNORMAL = 1
        user32.UpdateWindow(self.hwnd)

    def run(self) -> None:
        """
        运行窗口消息循环

        注意:
            此方法会阻塞直到窗口关闭
        """
        if not self.hwnd:
            raise RuntimeError("窗口尚未创建")

        while user32.GetMessageW(self.pMsg, None, 0, 0) > 0:
            user32.TranslateMessage(self.pMsg)
            user32.DispatchMessageW(self.pMsg)

    def _set_window_attribute(self, attr: int, value: int) -> int:
        """
        设置窗口属性

        参数:
            attr: 属性名(DWMWINDOWATTRIBUTE枚举值)
            value: 属性值

        返回:
            错误代码(0表示成功)

        注意:
            常用属性:
            - DWMWA_CAPTION_COLOR: 标题栏颜色
            - DWMWA_BORDER_COLOR: 边框颜色
            - DWMWA_TEXT_COLOR: 标题颜色
        """
        if not self.hwnd:
            raise RuntimeError("窗口尚未创建")

        try:
            result = dwmapi.DwmSetWindowAttribute(
                self.hwnd,
                wintypes.DWORD(attr),
                ctypes.byref(ctypes.c_int(value)),
                ctypes.sizeof(ctypes.c_int(value))
            )
            return result if result != 0 else kernel32.GetLastError()
        except Exception as e:
            print(f"设置窗口属性时出错: {e}")
            return kernel32.GetLastError()

    def setCaptionColor(self, r, g ,b):
        self._set_window_attribute(DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR.value, wintypes.RGB(r, g, b))

    def setBorderColor(self, r, g, b):
        self._set_window_attribute(DWMWINDOWATTRIBUTE.DWMWA_BORDER_COLOR.value, wintypes.RGB(r, g, b))

    def setTitleColor(self, r, g, b):
        self._set_window_attribute(DWMWINDOWATTRIBUTE.DWMWA_TEXT_COLOR.value, wintypes.RGB(r, g, b))

    def _window_proc(self, hwnd: HWND, uMsg: wintypes.UINT,
                     wParam: wintypes.WPARAM, lParam: wintypes.LPARAM) -> ctypes.c_long:
        """
        窗口消息处理函数

        参数:
            hwnd: 窗口句柄
            uMsg: 消息类型
            wParam: 消息参数
            lParam: 消息参数

        返回:
            消息处理结果
        """
        try:
            if uMsg == Constant.WM_CREATE:
                self._handle_create_message(hwnd, lParam)
                return 0

            elif uMsg == Constant.WM_DESTROY:
                user32.PostQuitMessage(0)
                return 0

            elif uMsg == Constant.WM_CLOSE:
                self._handle_close_message(hwnd)
                return 0

            elif uMsg == Constant.WM_SIZE:
                return self._handle_size_message(hwnd, wParam)

            elif uMsg == Constant.WM_PAINT:
                return self._handle_paint_message(hwnd)

            # 确保参数类型正确
            return user32.DefWindowProcW(
                wintypes.HWND(hwnd),
                wintypes.UINT(uMsg),
                wintypes.WPARAM(wParam),
                wintypes.LPARAM(lParam)
            )

        except Exception as e:
            print(f"处理窗口消息时出错: {e}")
            # 确保参数类型正确
            return user32.DefWindowProcW(
                wintypes.HWND(hwnd),
                wintypes.UINT(uMsg),
                wintypes.WPARAM(wParam),
                wintypes.LPARAM(lParam)
            )

    def _handle_create_message(self, hwnd: HWND, lParam: wintypes.LPARAM) -> None:
        """处理窗口创建消息"""
        pCreate = ctypes.cast(lParam, ctypes.POINTER(CREATESTRUCTW))
        pState = ctypes.cast(pCreate.contents.lpCreateParams, ctypes.POINTER(StateInfo))
        user32.SetWindowLongPtrW(
            hwnd,
            Constant.GWLP_USERDATA,
            LONG_PTR(ctypes.cast(pState, ctypes.c_void_p).value)
        )

    def _handle_close_message(self, hwnd: HWND) -> None:
        """处理窗口关闭消息"""
        # 可以在此处添加关闭确认逻辑
        # if user32.MessageBoxW(hwnd, "确定要退出吗？", self.title, Constant.MB_OKCANCEL) == Constant.IDOK:
        user32.DestroyWindow(hwnd)

    def _handle_size_message(self, hwnd: HWND, wParam: wintypes.WPARAM) -> int:
        """处理窗口大小改变消息"""
        width = Constant.LOWORD(wParam)
        height = Constant.HIWORD(wParam)
        self.width = width
        self.height = height
        self.onSize(hwnd, wintypes.UINT(wParam), width, height)
        return 0

    def _handle_paint_message(self, hwnd: HWND) -> int:
        """处理窗口绘制消息"""
        ps = PAINTSTRUCT()
        hdc = wintypes.HDC(user32.BeginPaint(hwnd, ctypes.byref(ps)))

        # 填充背景
        user32.FillRect(hdc, ctypes.byref(ps.rcPaint), wintypes.HBRUSH(Constant.COLOR_WINDOW + 1))

        user32.EndPaint(hwnd, ctypes.byref(ps))
        return 0

    def onSize(self, hwnd: wintypes.HWND, uMsg: wintypes.UINT, windth: int, height: int):
        pass

    def _load_icon(self, icon_path: str, size: int = 32) -> Union[HICON, wintypes.HICON]:
        """
        加载图标

        参数:
            icon_path: 图标文件路径
            size: 图标大小

        返回:
            加载的图标句柄

        注意:
            如果加载失败会使用默认图标并发出警告
        """
        icon = self._try_load_custom_icon(icon_path, size) if icon_path and os.path.exists(icon_path) \
              else self._load_default_icon(icon_path)

        self._update_icon_handles(icon, size)
        return icon

    def _try_load_custom_icon(self, icon_path: str, size: int) -> HICON:
        """尝试加载自定义图标"""
        icon = user32.LoadImageW(
            None,
            icon_path,
            Constant.IMAGE_ICON,
            size, size,
            Constant.LR_LOADFROMFILE,
        )
        if not icon:
            XCLoadIconWarning(f"警告: 无法加载目标图标文件 {icon_path}, 将使用默认图标")
            return self._load_default_icon(icon_path)
        return icon

    def _load_default_icon(self, icon_path: str) -> wintypes.HICON:
        """加载默认图标"""
        if icon_path:
            XCLoadIconWarning(f"警告: 图标文件路径无效 {icon_path}, 将使用默认图标")
        return user32.LoadIconW(None, ctypes.c_int(Constant.IDI_APPLICATION))

    def _update_icon_handles(self, icon: Union[HICON, wintypes.HICON], size: int) -> None:
        """更新图标句柄缓存"""
        if size >= 32:
            self.g_icon_handles = (icon, self.g_icon_handles[1])
        else:
            self.g_icon_handles = (self.g_icon_handles[0], icon)

    def _get_app_state(self, hwnd: wintypes.HWND):
        ptr = LONG_PTR(user32.GetWindowLongPtrW(hwnd, Constant.GWLP_USERDATA))
        pState = ctypes.cast(ptr, ctypes.POINTER(StateInfo))
        return pState

    def _register_class(self, class_name: str, icon_path: str) -> ATOM:
        """
        注册窗口类

        参数:
            class_name: 窗口类名
            icon_path: 图标路径

        返回:
            注册的窗口类原子

        异常:
            XCRegisterClassError: 如果注册失败
        """
        self.g_wnd_proc = WNDPROC(self._window_proc)

        # 加载图标
        h_icon = self._load_icon(icon_path, 32)
        h_icon_sm = self._load_icon(icon_path, 16)

        # 准备窗口类结构
        self._prepare_window_class(class_name, h_icon, h_icon_sm)

        # 注册窗口类
        return self._register_window_class()

    def _prepare_window_class(self,
                            class_name: str,
                            h_icon: Union[HICON, wintypes.HICON],
                            h_icon_sm: Union[HICON, wintypes.HICON]) -> None:
        """准备窗口类结构体"""
        self.wc = WNDCLASSEX()
        self.wc.cbSize = ctypes.sizeof(WNDCLASSEX)
        self.wc.style = 0
        self.wc.lpfnWndProc = self.g_wnd_proc
        self.wc.cbClsExtra = 0
        self.wc.cbWndExtra = 0
        self.wc.hInstance = kernel32.GetModuleHandleW(None)
        self.wc.hIcon = h_icon
        self.wc.hCursor = user32.LoadCursorW(None, ctypes.c_int(Constant.IDC_ARROW))
        self.wc.hbrBackground = ctypes.windll.gdi32.GetStockObject(ctypes.c_int(Constant.WHITE_BRUSH))
        self.wc.lpszMenuName = None
        self.wc.lpszClassName = class_name
        self.wc.hIconSm = h_icon_sm

    def _register_window_class(self) -> ATOM:
        """执行窗口类注册"""
        atom = user32.RegisterClassExW(ctypes.byref(self.wc))
        if atom == 0:
            raise XCRegisterClassError(f"注册窗口类失败，错误代码: {kernel32.GetLastError()}")
        return atom

    def _init_window(self, class_name: str, title: str, width: int, height: int) -> HWND:
        """
        初始化窗口

        参数:
            class_name: 窗口类名
            title: 窗口标题
            width: 窗口宽度
            height: 窗口高度

        返回:
            创建的窗口句柄

        异常:
            XCCreateWindowError: 如果窗口创建失败
        """
        pState = ctypes.byref(StateInfo())

        # 计算窗口位置(居中)
        x = (user32.GetSystemMetrics(0) - width) // 2
        y = (user32.GetSystemMetrics(1) - height) // 2

        # 创建窗口
        self.hwnd = self._create_window(class_name, title, x, y, width, height, pState)

        if self.hwnd == 0:
            raise XCCreateWindowError(f"创建窗口失败，错误代码: {kernel32.GetLastError()}")
        return self.hwnd

    def _create_window(self,
                      class_name: str,
                      title: str,
                      x: int,
                      y: int,
                      width: int,
                      height: int,
                      pState: ctypes.POINTER(StateInfo)) -> HWND:
        """执行窗口创建"""
        return user32.CreateWindowExW(
            ctypes.c_int(Constant.WS_EX_CLIENTEDGE),
            ctypes.c_wchar_p(class_name),
            ctypes.c_wchar_p(title),
            ctypes.c_int(Constant.WS_OVERLAPPEDWINDOW),
            ctypes.c_int(x),
            ctypes.c_int(y),
            ctypes.c_int(width),
            ctypes.c_int(height),
            None,
            None,
            kernel32.GetModuleHandleW(None),
            pState
        )


__all__ = [
    "XCWindowBase",
]

if __name__ == "__main__":
    pass
