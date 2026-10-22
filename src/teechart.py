import ctypes
import os

class TeeChart:
    def __init__(self, dll_path="teechart.dll"):
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"No teechart.dll found at: {dll_path}")

        self._dll = ctypes.WinDLL(dll_path)
        self._setup_signatures()

    def _setup_signatures(self):
        self._dll.RenderChart.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.RenderChart.restype = ctypes.c_bool

    def render(self, data: str, size: int) -> bool:
        return self._dll.RenderChart(data.encode('utf-8'), size)

