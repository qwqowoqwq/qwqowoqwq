import ctypes
desktop = ctypes.cdll.LoadLibrary("./desktop.dll")
desktop.desktop_intersect(600, 0, 1000, 1000)
