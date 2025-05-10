from xcwindow import VulkanWindow

if __name__ == "__main__":
    window = VulkanWindow(1000, 720)
    window.show()
    window.run()

# nuitka --standalone --onefile --windows-disable-console --output-dir=dist --remove-output --jobs=16 --lto=yes --windows-icon-from-ico="xcwindow/assets/pyc.ico" main.py
