import ctypes
import ctypes.wintypes as wintypes
import os
from uuid import uuid4
from enum import Enum, auto
from .error import XCRegisterClassError, XCCreateWindowError, XCLoadIconWarning
from .constant import Constant

vulkan = ctypes.WinDLL('vulkan-1', use_last_error=True)
dwmapi = ctypes.windll.dwmapi
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

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
    def __init__(self, width: int, height: int, title: str="XCWindow",
                 icon_path: str=_get_python_icon_path(), class_name: str=f"XCWindow-{uuid4()}"):
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.icon_path: str = icon_path
        self.class_name: str = class_name

        self.g_wnd_proc: WNDPROC = None
        self.g_icon_handles: tuple = (None, None)

        kernel32.SetErrorMode(0x0001 | 0x0002)

        self.msg: wintypes.MSG = wintypes.MSG()
        self.pMsg = ctypes.byref(self.msg)

        self._register_class(self.class_name, self.icon_path)
        self._init_window(self.class_name, self.title, self.width, self.height)

    def show(self):
        user32.ShowWindow(self.hwnd, 1)
        user32.UpdateWindow(self.hwnd)

    def run(self):
        while user32.GetMessageW(self.pMsg, None, 0, 0) > 0:
            user32.TranslateMessage(self.pMsg)
            user32.DispatchMessageW(self.pMsg)

    def _window_proc(self, hwnd: wintypes.HWND, uMsg: wintypes.UINT,
                     wParam: wintypes.WPARAM, lParam: wintypes.LPARAM) -> ctypes.c_long:
        if uMsg == Constant.WM_CREATE:
            pCreate = ctypes.cast(lParam, ctypes.POINTER(CREATESTRUCTW))
            pState = ctypes.cast(pCreate.contents.lpCreateParams, ctypes.POINTER(StateInfo))
            user32.SetWindowLongPtrW(hwnd, Constant.GWLP_USERDATA,
                                                   LONG_PTR(ctypes.cast(pState, ctypes.c_void_p).value))

        if uMsg == Constant.WM_DESTROY:
            user32.PostQuitMessage(0)
            return 0
        elif uMsg == Constant.WM_CLOSE:
            # 弹出消息框询问用户是否真的要退出
            # result = user32.MessageBoxW(hwnd, "确定要退出吗？", self.title, Constant.MB_OKCANCEL)
            # if result == Constant.IDOK:
            #     user32.DestroyWindow(hwnd)
            user32.DestroyWindow(hwnd)
            return 0
        elif uMsg == Constant.WM_SIZE:
            width = Constant.LOWORD(wParam)
            height = Constant.HIWORD(wParam)
            self.width = width
            self.height = height
            self.onSize(hwnd, wintypes.UINT(wParam), width, height)
            return 0
        elif uMsg == Constant.WM_PAINT:
            ps = PAINTSTRUCT()
            hdc = wintypes.HDC(user32.BeginPaint(hwnd, ctypes.byref(ps)))

            user32.FillRect(hdc, ctypes.byref(ps.rcPaint), wintypes.HBRUSH(Constant.COLOR_WINDOW + 1))

            user32.EndPaint(hwnd, ctypes.byref(ps))
            return 0

        return user32.DefWindowProcW(
            wintypes.HWND(hwnd),
            wintypes.UINT(uMsg),
            wintypes.WPARAM(wParam),
            wintypes.LPARAM(lParam)
        )

    def onSize(self, hwnd: wintypes.HWND, uMsg: wintypes.UINT, windth: int, height: int):
        pass

    def _load_icon(self, icon_path: str, size: int=32) -> wintypes.HANDLE | wintypes.HICON:
        if icon_path and os.path.exists(icon_path):
            icon: wintypes.HANDLE = user32.LoadImageW(
                None,
                icon_path,
                Constant.IMAGE_ICON,
                size, size,
                Constant.LR_LOADFROMFILE,
            )
            if not icon:
                XCLoadIconWarning(f"警告: 无法加载目标图标文件 {icon_path}, 将使用默认图标")
                icon: wintypes.HICON = user32.LoadIconW(None, ctypes.c_int(Constant.IDI_APPLICATION))
        else:
            XCLoadIconWarning(f"警告: 图标文件路径无效 {icon_path}, 将使用默认图标")
            icon: wintypes.HICON = user32.LoadIconW(None, ctypes.c_int(Constant.IDI_APPLICATION))

        if size >= 32:
            self.g_icon_handles = (icon, self.g_icon_handles[1])
        else:
            self.g_icon_handles = (self.g_icon_handles[0], icon)

        return icon

    def _get_app_state(self, hwnd: wintypes.HWND):
        ptr = LONG_PTR(user32.GetWindowLongPtrW(hwnd, Constant.GWLP_USERDATA))
        pState = ctypes.cast(ptr, ctypes.POINTER(StateInfo))
        return pState

    def _register_class(self, class_name: str, icon_path: str) -> wintypes.ATOM:
        wnd_proc = WNDPROC(self._window_proc)
        self.g_wnd_proc = wnd_proc

        h_icon: wintypes.HANDLE | wintypes.HICON = self._load_icon(icon_path, 32)
        h_icon_sm: wintypes.HANDLE | wintypes.HICON = self._load_icon(icon_path, 16)

        self.wc: WNDCLASSEX = WNDCLASSEX()
        self.wc.cbSize = ctypes.sizeof(WNDCLASSEX)
        self.wc.style = 0
        self.wc.lpfnWndProc = wnd_proc
        self.wc.cbClsExtra = 0
        self.wc.cbWndExtra = 0
        self.wc.hInstance = kernel32.GetModuleHandleW(None)
        self.wc.hIcon = h_icon
        self.wc.hCursor = user32.LoadCursorW(None, ctypes.c_int(Constant.IDC_ARROW))
        self.wc.hbrBackground = ctypes.windll.gdi32.GetStockObject(ctypes.c_int(Constant.WHITE_BRUSH))
        self.wc.lpszMenuName = None
        self.wc.lpszClassName = class_name
        self.wc.hIconSm = h_icon_sm

        atom: wintypes.ATOM = user32.RegisterClassExW(ctypes.byref(self.wc))
        if atom == 0:
            XCRegisterClassError(f"注册窗口类失败，错误代码: {kernel32.GetLastError()}")
        return atom

    def _init_window(self, class_name: str, title: str, width: int, height: int) -> wintypes.HWND:
        pState = ctypes.byref(StateInfo())

        self.hwnd: wintypes.HWND = user32.CreateWindowExW(
            ctypes.c_int(Constant.WS_EX_CLIENTEDGE),
            ctypes.c_wchar_p(class_name),
            ctypes.c_wchar_p(title),
            ctypes.c_int(Constant.WS_OVERLAPPEDWINDOW),
            ctypes.c_int((user32.GetSystemMetrics(0) - width) // 2),
            ctypes.c_int((user32.GetSystemMetrics(1) - height) // 2),
            ctypes.c_int(width),
            ctypes.c_int(height),
            None,
            None,
            kernel32.GetModuleHandleW(None),
            pState
        )
        # DWMWA_CAPTION_COLOR  标题栏颜色属性名
        # DWMWA_BORDER_COLOR  边框颜色属性名
        # DWMWA_TEXT_COLOR  标题颜色属性名

        caption_color = wintypes.RGB(10, 100, 100)
        try:
            result = dwmapi.DwmSetWindowAttribute(
                self.hwnd, 
                wintypes.DWORD(DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR.value),
                ctypes.byref(ctypes.c_int(caption_color)),
                ctypes.sizeof(ctypes.c_int(caption_color))
            )
            if result != 0:  # S_OK = 0
                kernel32.GetLastError()
        except Exception:
            pass
        if self.hwnd == 0:
            XCCreateWindowError(f"创建窗口失败，错误代码: {kernel32.GetLastError()}")
        return self.hwnd


__all__ = [
    "XCWindowBase",
]

if __name__ == "__main__":
    pass
