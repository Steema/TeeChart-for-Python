import ctypes
import io
import tkinter as tk
from PIL import Image, ImageTk

dll = ctypes.WinDLL("teechart.dll")

dll.GetChartBitmapBytes.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int)]
dll.GetChartBitmapBytes.restype = ctypes.c_bool

root = tk.Tk()
root.title("TeeChart as Bitmap")

buffer_ptr = ctypes.c_void_p()
size = ctypes.c_int()

if dll.GetChartBitmapBytes(ctypes.byref(buffer_ptr), ctypes.byref(size)):
    raw_data = ctypes.string_at(buffer_ptr.value, size.value)

    img = Image.open(io.BytesIO(raw_data))
    photo = ImageTk.PhotoImage(img)

    lbl = tk.Label(root, image=photo)
    lbl.image = photo
    lbl.pack()

root.mainloop()
