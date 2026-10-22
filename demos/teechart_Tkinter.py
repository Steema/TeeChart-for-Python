import ctypes
import tkinter as tk

dll = ctypes.WinDLL("teechart.dll")

root = tk.Tk()
root.title("TeeChart for Tkinter")
frame = tk.Frame(root, width=600, height=400)
frame.pack(fill=tk.BOTH, expand=True)
root.update()

hwnd = frame.winfo_id()

dll.Embed(hwnd, 600, 400)

root.mainloop()
