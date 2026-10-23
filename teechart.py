"""Python ctypes wrapper for the TeeChartRender function in teechart.dll.

The argument order and pointer types mirror the R .C() call supplied by the
user. Strings are encoded as UTF-8; change _encode_text if the DLL expects a
different Windows code page. The function's native return value is ignored,
as in R's .C() interface; any output buffers must be added explicitly.
"""

from __future__ import annotations

import ctypes
import os
from pathlib import Path
from typing import Sequence, Union

PathLike = Union[str, os.PathLike[str]]


class TeeChartError(RuntimeError):
    """Raised when the native library cannot be loaded or invoked."""


def _encode_text(value: str) -> bytes:
    if not isinstance(value, str):
        raise TypeError(f"S'esperava text (str), rebut: {type(value).__name__}")
    if "\0" in value:
        raise ValueError("Les cadenes passades a la DLL no poden contenir NUL.")
    return value.encode("utf-8")


class TeeChart:
    def __init__(self, dll_path: PathLike = "teechart.dll"):

        self.dll_path = Path(dll_path).resolve()

        if not self.dll_path.is_file():
            raise FileNotFoundError(f"DLL not found at: {self.dll_path}")

        if os.name != "nt":
            raise OSError("This is a Windows wrapper only.")

        if ctypes.sizeof(ctypes.c_void_p) != 8:
            raise OSError("64 bits Python is necessary.")

        try:
            self._dll_directory = os.add_dll_directory(str(self.dll_path.parent))
            self._dll = ctypes.CDLL(str(self.dll_path))  # R .C() uses C calling convention
            self._render = self._dll.TeeChartRender
        except (OSError, AttributeError) as exc:
            raise TeeChartError(
                f"No s'ha pogut carregar {self.dll_path} o trobar TeeChartRender. "
                "Comprova les dependències i el nom exportat."
            ) from exc

        double_ptr = ctypes.POINTER(ctypes.c_double)
        char_ptr = ctypes.POINTER(ctypes.c_char_p)

        self._render.argtypes = [
            ctypes.POINTER(ctypes.c_int), double_ptr,
            ctypes.POINTER(ctypes.c_int), double_ptr,
            ctypes.POINTER(ctypes.c_int), double_ptr,
            ctypes.POINTER(ctypes.c_int), char_ptr,
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p),
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
        ]
        self._render.restype = None

    @staticmethod
    def _double_array(values: Sequence[float], name: str):
        data = [float(v) for v in values]
        array_type = ctypes.c_double * len(data)
        return array_type(*data)

    @staticmethod
    def _text_array(values: Sequence[str], name: str):
        encoded = [_encode_text(value) for value in values]
        array_type = ctypes.c_char_p * len(encoded)
        return array_type(*encoded)

    def render(
        self,
        x: Sequence[float],
        y: Sequence[float],
        z: Sequence[float],
        texts: Sequence[str],
        output_type: str,
        width: int,
        height: int,
        style: str = "",
        title: str = "",
        footer: str = "",
        horiz: bool = False,
        commander: bool = False,
        opengl: bool = False,
    ) -> None:
        """Call TeeChartRender; arrays and scalar values follow the R .C() ABI."""
        xa = self._double_array(x, "x")
        ya = self._double_array(y, "y")
        za = self._double_array(z, "z")
        ta = self._text_array(texts, "texts")

        # Keep encoded scalar strings alive for the duration of the native call.
        strings = [_encode_text(s) for s in (output_type, style, title, footer)]
        output_c, style_c, title_c, footer_c = (ctypes.c_char_p(s) for s in strings)
        nx, ny, nz, nt = (ctypes.c_int(len(v)) for v in (x, y, z, texts))
        w, h = ctypes.c_int(int(width)), ctypes.c_int(int(height))
        flags = [ctypes.c_int(int(bool(flag))) for flag in (horiz, commander, opengl)]

        try:
            self._render(
                ctypes.byref(nx), xa,
                ctypes.byref(ny), ya,
                ctypes.byref(nz), za,
                ctypes.byref(nt), ta,
                ctypes.byref(output_c),
                ctypes.byref(w), ctypes.byref(h),
                ctypes.byref(style_c), ctypes.byref(title_c), ctypes.byref(footer_c),
                *(ctypes.byref(flag) for flag in flags),
            )
        except (OSError, ValueError, ctypes.ArgumentError) as exc:
            raise TeeChartError("TeeChartRender call failed.") from exc


def load(dll_path: PathLike = "teechart.dll") -> TeeChart:
    """Load the DLL and return a TeeChart wrapper."""
    return TeeChart(dll_path)

