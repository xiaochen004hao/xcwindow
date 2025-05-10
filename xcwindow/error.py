from typing import Optional

class XCRegisterClassError(WindowsError):
    """
    窗口类注册失败异常

    属性:
        error_code: Windows API错误代码
        message: 错误描述信息
    """
    def __init__(self, message: str, error_code: Optional[int] = None):
        """
        初始化异常

        参数:
            message: 错误描述
            error_code: Windows API错误代码(可选)
        """
        self.error_code = error_code
        super().__init__(f"{message} (错误代码: {error_code})" if error_code else message)


class XCCreateWindowError(WindowsError):
    """
    窗口创建失败异常

    属性:
        error_code: Windows API错误代码
        message: 错误描述信息
    """
    def __init__(self, message: str, error_code: Optional[int] = None):
        """
        初始化异常

        参数:
            message: 错误描述
            error_code: Windows API错误代码(可选)
        """
        self.error_code = error_code
        super().__init__(f"{message} (错误代码: {error_code})" if error_code else message)


class XCLoadIconWarning(RuntimeWarning):
    """
    图标加载警告

    属性:
        message: 警告信息
    """
    def __init__(self, message: str):
        """
        初始化警告

        参数:
            message: 警告信息
        """
        print(f"XCLoadIconWarning: {message}")
        super().__init__(message)
