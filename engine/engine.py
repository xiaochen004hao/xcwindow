import ctypes
import ctypes.wintypes as wintypes
from typing import Tuple, List, Optional, Any

# 加载Vulkan库并设置函数原型
vulkan = ctypes.WinDLL('vulkan-1', use_last_error=True)

# 类型别名定义
VkInstance = ctypes.c_void_p
VkSurface = ctypes.c_void_p
VkDevice = ctypes.c_void_p
VkSwapchain = ctypes.c_void_p
VkQueue = ctypes.c_void_p
VkPhysicalDevice = ctypes.c_void_p

# 定义Vulkan常量
VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1
VK_STRUCTURE_TYPE_WIN32_SURFACE_CREATE_INFO_KHR = 1000009000
VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO = 2
VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR = 1000001000
VK_QUEUE_GRAPHICS_BIT = 0x00000001
VK_KHR_SURFACE_EXTENSION_NAME = b"VK_KHR_surface"
VK_KHR_WIN32_SURFACE_EXTENSION_NAME = b"VK_KHR_win32_surface"
VK_KHR_SWAPCHAIN_EXTENSION_NAME = b"VK_KHR_swapchain"
VK_EXT_DEBUG_UTILS_EXTENSION_NAME = b"VK_EXT_debug_utils"
VK_FORMAT_B8G8R8A8_SRGB = 50
VK_PRESENT_MODE_FIFO_KHR = 2
VK_STRUCTURE_TYPE_PRESENT_INFO_KHR = 1000001001
VK_SUCCESS = 0


# 定义VkInstanceCreateInfo结构体
class VkInstanceCreateInfo(ctypes.Structure):
    _fields_ = [
        ("sType", ctypes.c_int),
        ("pNext", ctypes.c_void_p),
        ("flags", ctypes.c_uint32),
        ("pApplicationInfo", ctypes.c_void_p),
        ("enabledLayerCount", ctypes.c_uint32),
        ("ppEnabledLayerNames", ctypes.POINTER(ctypes.c_char_p)),
        ("enabledExtensionCount", ctypes.c_uint32),
        ("ppEnabledExtensionNames", ctypes.POINTER(ctypes.c_char_p)),
    ]


class VkWin32SurfaceCreateInfoKHR(ctypes.Structure):
    _fields_ = [
        ("sType", ctypes.c_int),
        ("pNext", ctypes.c_void_p),
        ("flags", ctypes.c_uint32),
        ("hinstance", wintypes.HINSTANCE),
        ("hwnd", wintypes.HWND),
    ]


class VkQueueFamilyProperties(ctypes.Structure):
    _fields_ = [
        ("queueFlags", ctypes.c_uint32),
        ("queueCount", ctypes.c_uint32),
        ("timestampValidBits", ctypes.c_uint32),
        ("minImageTransferGranularity", ctypes.c_uint32 * 3),
    ]


# 定义交换链相关结构体
class VkDeviceCreateInfo(ctypes.Structure):
    _fields_ = [
        ("sType", ctypes.c_int),
        ("pNext", ctypes.c_void_p),
        ("flags", ctypes.c_uint32),
        ("queueCreateInfoCount", ctypes.c_uint32),
        ("pQueueCreateInfos", ctypes.c_void_p),
        ("enabledLayerCount", ctypes.c_uint32),
        ("ppEnabledLayerNames", ctypes.POINTER(ctypes.c_char_p)),
        ("enabledExtensionCount", ctypes.c_uint32),
        ("ppEnabledExtensionNames", ctypes.POINTER(ctypes.c_char_p)),
        ("pEnabledFeatures", ctypes.c_void_p),
    ]


class VkSwapchainCreateInfoKHR(ctypes.Structure):
    _fields_ = [
        ("sType", ctypes.c_int),
        ("pNext", ctypes.c_void_p),
        ("flags", ctypes.c_uint32),
        ("surface", ctypes.c_void_p),
        ("minImageCount", ctypes.c_uint32),
        ("imageFormat", ctypes.c_int),
        ("imageColorSpace", ctypes.c_int),
        ("imageExtent", ctypes.c_uint32 * 2),
        ("imageArrayLayers", ctypes.c_uint32),
        ("imageUsage", ctypes.c_uint32),
        ("imageSharingMode", ctypes.c_int),
        ("queueFamilyIndexCount", ctypes.c_uint32),
        ("pQueueFamilyIndices", ctypes.POINTER(ctypes.c_uint32)),
        ("preTransform", ctypes.c_int),
        ("compositeAlpha", ctypes.c_int),
        ("presentMode", ctypes.c_int),
        ("clipped", ctypes.c_uint32),
        ("oldSwapchain", ctypes.c_void_p),
    ]


# 定义呈现相关结构体
class VkPresentInfoKHR(ctypes.Structure):
    _fields_ = [
        ("sType", ctypes.c_int),
        ("pNext", ctypes.c_void_p),
        ("waitSemaphoreCount", ctypes.c_uint32),
        ("pWaitSemaphores", ctypes.POINTER(ctypes.c_void_p)),
        ("swapchainCount", ctypes.c_uint32),
        ("pSwapchains", ctypes.POINTER(ctypes.c_void_p)),
        ("pImageIndices", ctypes.POINTER(ctypes.c_uint32)),
        ("pResults", ctypes.POINTER(ctypes.c_int)),
    ]


# 声明表面创建函数原型
vulkan.vkCreateWin32SurfaceKHR = vulkan.vkCreateWin32SurfaceKHR
vulkan.vkCreateWin32SurfaceKHR.argtypes = [
    ctypes.c_void_p,  # instance
    ctypes.POINTER(VkWin32SurfaceCreateInfoKHR),  # pCreateInfo
    ctypes.c_void_p,  # pAllocator
    ctypes.POINTER(ctypes.c_void_p)  # pSurface
]
vulkan.vkCreateWin32SurfaceKHR.restype = ctypes.c_int

# 显式声明Vulkan函数原型
vulkan.vkGetPhysicalDeviceQueueFamilyProperties.argtypes = [
    ctypes.c_void_p,  # physicalDevice
    ctypes.POINTER(ctypes.c_uint32),  # pQueueFamilyPropertyCount
    ctypes.POINTER(VkQueueFamilyProperties)  # pQueueFamilyProperties
]
vulkan.vkGetPhysicalDeviceQueueFamilyProperties.restype = None

# 确保正确加载Vulkan函数
if not hasattr(vulkan, 'vkGetPhysicalDeviceSurfaceSupportKHR'):
    # 显式获取函数指针
    vkGetPhysicalDeviceSurfaceSupportKHR = vulkan.vkGetPhysicalDeviceSurfaceSupportKHR
    vkGetPhysicalDeviceSurfaceSupportKHR.argtypes = [
        ctypes.c_void_p,  # physicalDevice
        ctypes.c_uint32,  # queueFamilyIndex
        ctypes.c_void_p,  # surface
        ctypes.POINTER(ctypes.c_uint32)  # pSupported
    ]
    vkGetPhysicalDeviceSurfaceSupportKHR.restype = ctypes.c_int
    # 将函数指针赋值给模块
    vulkan.vkGetPhysicalDeviceSurfaceSupportKHR = vkGetPhysicalDeviceSurfaceSupportKHR

# 声明交换链相关函数原型
vulkan.vkCreateDevice.argtypes = [
    ctypes.c_void_p,  # physicalDevice
    ctypes.POINTER(VkDeviceCreateInfo),  # pCreateInfo
    ctypes.c_void_p,  # pAllocator
    ctypes.POINTER(ctypes.c_void_p)  # pDevice
]
vulkan.vkCreateDevice.restype = ctypes.c_int

vulkan.vkCreateSwapchainKHR.argtypes = [
    ctypes.c_void_p,  # device
    ctypes.POINTER(VkSwapchainCreateInfoKHR),  # pCreateInfo
    ctypes.c_void_p,  # pAllocator
    ctypes.POINTER(ctypes.c_void_p)  # pSwapchain
]
vulkan.vkCreateSwapchainKHR.restype = ctypes.c_int

# 声明渲染循环相关函数原型
vulkan.vkAcquireNextImageKHR.argtypes = [
    ctypes.c_void_p,  # device
    ctypes.c_void_p,  # swapchain
    ctypes.c_uint64,  # timeout
    ctypes.c_void_p,  # semaphore
    ctypes.c_void_p,  # fence
    ctypes.POINTER(ctypes.c_uint32)  # pImageIndex
]
vulkan.vkAcquireNextImageKHR.restype = ctypes.c_int

vulkan.vkQueuePresentKHR.argtypes = [
    ctypes.c_void_p,  # queue
    ctypes.POINTER(VkPresentInfoKHR)  # pPresentInfo
]
vulkan.vkQueuePresentKHR.restype = ctypes.c_int

vulkan.vkGetDeviceQueue.argtypes = [
    ctypes.c_void_p,  # device
    ctypes.c_uint32,  # queueFamilyIndex
    ctypes.c_uint32,  # queueIndex
    ctypes.POINTER(ctypes.c_void_p)  # pQueue
]
vulkan.vkGetDeviceQueue.restype = None


class EngineBase:
    def __init__(self, hwnd, hinstance):
        """初始化Vulkan引擎基类"""
        self.hwnd = hwnd
        self.hinstance = hinstance
        self.instance = None
        self._create_instance()
        self._create_surface()
        self._select_physical_device()

    def _create_instance(self):
        """创建Vulkan实例"""
        # 定义扩展列表
        extensions = [
            VK_KHR_SURFACE_EXTENSION_NAME,
            VK_KHR_WIN32_SURFACE_EXTENSION_NAME,
            VK_EXT_DEBUG_UTILS_EXTENSION_NAME
        ]

        # 准备扩展名称数组
        ext_names = (ctypes.c_char_p * len(extensions))()
        ext_names[:] = extensions

        # 填充实例创建信息
        instance_info = VkInstanceCreateInfo()
        instance_info.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        instance_info.enabledExtensionCount = len(extensions)
        instance_info.ppEnabledExtensionNames = ext_names

        # 创建实例
        instance = ctypes.c_void_p()
        result = vulkan.vkCreateInstance(
            ctypes.byref(instance_info),
            None,
            ctypes.byref(instance)
        )

        if result != 0:
            raise RuntimeError(f"创建Vulkan实例失败: {result}")

        self.instance = instance

        return instance

    def _create_surface(self) -> VkSurface:
        """
        创建Win32 Vulkan表面

        返回:
            创建的Vulkan表面

        异常:
            RuntimeError: 如果表面创建失败
        """
        surface_create_info = self._prepare_surface_info()

        surface = VkSurface()
        result = vulkan.vkCreateWin32SurfaceKHR(
            self.instance,
            ctypes.byref(surface_create_info),
            None,
            ctypes.byref(surface)
        )
        self._check_vk_result(result, "创建Vulkan表面失败")

        self.surface = surface
        return surface

    def _prepare_surface_info(self) -> VkWin32SurfaceCreateInfoKHR:
        """准备表面创建信息"""
        surface_create_info = VkWin32SurfaceCreateInfoKHR()
        surface_create_info.sType = VK_STRUCTURE_TYPE_WIN32_SURFACE_CREATE_INFO_KHR
        surface_create_info.hwnd = self.hwnd
        surface_create_info.hinstance = self.hinstance
        return surface_create_info

    def _select_physical_device(self) -> None:
        """
        选择物理设备和图形队列族

        异常:
            RuntimeError: 如果没有找到合适的设备或队列族
        """
        devices = self._enumerate_physical_devices()

        for device in devices:
            queue_families = self._get_queue_families(device)

            for j, queue_family in enumerate(queue_families):
                if self._is_suitable_queue_family(device, j, queue_family):
                    self.physical_device = device
                    self.graphics_queue_family = j
                    self._create_device()
                    self._create_swapchain()
                    return

        raise RuntimeError("未找到支持图形和呈现的队列族")

    def _enumerate_physical_devices(self) -> List[VkPhysicalDevice]:
        """枚举所有可用的物理设备"""
        device_count = ctypes.c_uint32(0)
        vulkan.vkEnumeratePhysicalDevices(self.instance, ctypes.byref(device_count), None)

        if device_count.value == 0:
            raise RuntimeError("未找到支持Vulkan的物理设备")

        devices = (VkPhysicalDevice * device_count.value)()
        vulkan.vkEnumeratePhysicalDevices(self.instance, ctypes.byref(device_count), devices)
        return list(devices)

    def _get_queue_families(self, device: VkPhysicalDevice) -> List[VkQueueFamilyProperties]:
        """获取设备的队列族属性"""
        count = ctypes.c_uint32(0)
        vulkan.vkGetPhysicalDeviceQueueFamilyProperties(device, ctypes.byref(count), None)

        families = (VkQueueFamilyProperties * count.value)()
        vulkan.vkGetPhysicalDeviceQueueFamilyProperties(device, ctypes.byref(count), families)
        return list(families)

    def _is_suitable_queue_family(self, device: VkPhysicalDevice,
                                index: int,
                                queue_family: VkQueueFamilyProperties) -> bool:
        """检查队列族是否适合图形和呈现"""
        present_support = ctypes.c_uint32(False)
        # 确保正确传递surface参数
        result = vulkan.vkGetPhysicalDeviceSurfaceSupportKHR(
            device,
            ctypes.c_uint32(index),
            self.surface,
            (ctypes.byref(present_support))
        )

        return (result == VK_SUCCESS and
                (queue_family.queueFlags & VK_QUEUE_GRAPHICS_BIT) and
                present_support.value)

    def _create_device(self) -> VkDevice:
        """
        创建逻辑设备

        返回:
            创建的Vulkan逻辑设备

        异常:
            RuntimeError: 如果设备创建失败
        """
        extensions = self._get_device_extensions()
        device_info = self._prepare_device_info(extensions)

        device = VkDevice()
        result = vulkan.vkCreateDevice(
            self.physical_device,
            ctypes.byref(device_info),
            None,
            ctypes.byref(device)
        )
        self._check_vk_result(result, "创建逻辑设备失败")

        self.device = device
        self._get_graphics_queue()
        return device

    def _get_device_extensions(self) -> List[bytes]:
        """获取设备所需的扩展列表"""
        return [VK_KHR_SWAPCHAIN_EXTENSION_NAME]

    def _prepare_device_info(self, extensions: List[bytes]) -> VkDeviceCreateInfo:
        """准备设备创建信息"""
        ext_names = (ctypes.c_char_p * len(extensions))()
        ext_names[:] = extensions

        queue_create_info = (ctypes.c_uint32 * 1)(self.graphics_queue_family)

        device_info = VkDeviceCreateInfo()
        device_info.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO
        device_info.queueCreateInfoCount = 1
        device_info.pQueueCreateInfos = ctypes.cast(queue_create_info, ctypes.c_void_p)
        device_info.enabledExtensionCount = len(extensions)
        device_info.ppEnabledExtensionNames = ext_names

        return device_info

    def _get_graphics_queue(self):
        """获取图形队列"""
        queue = ctypes.c_void_p()
        vulkan.vkGetDeviceQueue(
            self.device,
            self.graphics_queue_family,
            0,  # 第一个队列
            ctypes.byref(queue)
        )
        self.graphics_queue = queue
        return queue

    def _create_swapchain(self) -> VkSwapchain:
        """
        创建交换链

        返回:
            创建的Vulkan交换链

        异常:
            RuntimeError: 如果交换链创建失败
        """
        swapchain_info = self._prepare_swapchain_info()

        swapchain = VkSwapchain()
        result = vulkan.vkCreateSwapchainKHR(
            self.device,
            ctypes.byref(swapchain_info),
            None,
            ctypes.byref(swapchain)
        )
        self._check_vk_result(result, "创建交换链失败")

        self.swapchain = swapchain
        return swapchain

    def _prepare_swapchain_info(self) -> VkSwapchainCreateInfoKHR:
        """准备交换链创建信息"""
        swapchain_info = VkSwapchainCreateInfoKHR()
        swapchain_info.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR
        swapchain_info.surface = self.surface
        swapchain_info.minImageCount = 3  # 根据Surface能力调整
        swapchain_info.imageFormat = VK_FORMAT_B8G8R8A8_SRGB
        swapchain_info.imageExtent = (ctypes.c_uint32 * 2)(800, 600)  # 与窗口尺寸一致
        swapchain_info.imageArrayLayers = 1
        swapchain_info.imageUsage = 0x00000010  # VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT
        swapchain_info.imageSharingMode = 0  # VK_SHARING_MODE_EXCLUSIVE
        swapchain_info.preTransform = 0  # VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR
        swapchain_info.compositeAlpha = 1  # VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR
        swapchain_info.presentMode = VK_PRESENT_MODE_FIFO_KHR
        swapchain_info.clipped = 1

        return swapchain_info

    def _acquire_next_image(self) -> int:
        """
        获取交换链中的下一帧图像

        返回:
            int: 获取到的图像索引

        异常:
            RuntimeError: 如果获取图像失败
        """
        image_index = ctypes.c_uint32(0)
        result = vulkan.vkAcquireNextImageKHR(
            self.device,
            self.swapchain,
            0xFFFFFFFFFFFFFFFF,  # UINT64_MAX
            None,  # 不使用信号量
            None,  # 不使用栅栏
            ctypes.byref(image_index)
        )
        self._check_vk_result(result, "获取下一帧图像失败")

        return image_index.value

    def _present_image(self, image_index: int) -> None:
        """
        呈现当前帧到屏幕

        参数:
            image_index: 要呈现的图像索引

        异常:
            RuntimeError: 如果呈现失败
        """
        swapchain = ctypes.c_void_p(self.swapchain)
        image_index = ctypes.c_uint32(image_index)

        present_info = self._prepare_present_info(swapchain, image_index)

        result = vulkan.vkQueuePresentKHR(
            self.graphics_queue,
            ctypes.byref(present_info)
        )
        self._check_vk_result(result, "呈现图像失败")

    def _prepare_present_info(self,
                            swapchain: VkSwapchain,
                            image_index: ctypes.c_uint32) -> VkPresentInfoKHR:
        """准备呈现信息结构体"""
        present_info = VkPresentInfoKHR()
        present_info.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR
        present_info.swapchainCount = 1
        present_info.pSwapchains = ctypes.byref(swapchain)
        present_info.pImageIndices = ctypes.byref(image_index)
        return present_info

    def render_frame(self) -> bool:
        """
        渲染一帧

        返回:
            bool: 渲染是否成功

        注意:
            子类应该重写_custom_render方法实现实际渲染逻辑
        """
        try:
            # 尝试获取下一帧图像
            try:
                image_index = self._acquire_next_image()
            except RuntimeError as e:
                if "1000001003" in str(e):  # VK_ERROR_OUT_OF_DATE_KHR
                    self._recreate_swapchain()
                    return False
                raise e

            self._custom_render(image_index)

            # 呈现图像
            try:
                result = self._present_image(image_index)
                if result == 1000001003:  # VK_ERROR_OUT_OF_DATE_KHR
                    self._recreate_swapchain()
                    return False
            except RuntimeError as e:
                if "1000001003" in str(e):
                    self._recreate_swapchain()
                    return False
                raise e

            return True
        except Exception as e:
            print(f"渲染帧时出错: {e}")
            return False

    def _acquire_next_image(self) -> int:
        """
        获取交换链中的下一帧图像

        返回:
            int: 获取到的图像索引

        异常:
            RuntimeError: 如果获取图像失败
        """
        image_index = ctypes.c_uint32(0)
        result = vulkan.vkAcquireNextImageKHR(
            self.device,
            self.swapchain,
            0xFFFFFFFFFFFFFFFF,  # UINT64_MAX
            None,  # 不使用信号量
            None,  # 不使用栅栏
            ctypes.byref(image_index)
        )
        if result != VK_SUCCESS:
            raise RuntimeError(f"获取下一帧图像失败: {result}")
        return image_index.value

    def _recreate_swapchain(self) -> None:
        """重建交换链"""
        # 等待设备空闲
        self._wait_device_idle()

        # 销毁旧交换链
        if hasattr(self, 'swapchain'):
            vulkan.vkDestroySwapchainKHR(self.device, self.swapchain, None)

        # 重建交换链
        self._create_swapchain()

    def _wait_device_idle(self) -> None:
        """等待设备空闲"""
        vulkan.vkDeviceWaitIdle(self.device)

    def _check_vk_result(self, result: int, message: str) -> None:
        """
        检查Vulkan API调用结果

        参数:
            result: Vulkan API调用返回码
            message: 错误消息前缀

        异常:
            RuntimeError: 如果result不为VK_SUCCESS
        """
        if result != VK_SUCCESS:
            raise RuntimeError(f"{message}: {result}")

    def _custom_render(self, image_index: int) -> None:
        """
        自定义渲染逻辑(供子类实现)

        参数:
            image_index: 当前帧图像索引
        """
        # 基础实现为空，子类应该重写此方法
        pass
