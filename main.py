from xcwindow import XCWindowBase
from engine import EngineBase

window = XCWindowBase(1000, 720, title="Vulkan Test")
window.setCaptionColor(233, 235, 254)

EngineBase(window.hwnd, window.wc.hInstance)

window.show()
window.run()

# nuitka --standalone --onefile --windows-disable-console --output-dir=dist --remove-output --jobs=16 --lto=yes --windows-icon-from-ico="xcwindow/assets/pyc.ico" main.py
