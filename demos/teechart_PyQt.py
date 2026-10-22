import ctypes
import io
import sys
from PIL import Image
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

# Load the DLL
dll = ctypes.WinDLL("teechart_plugin.dll")

# Define function signatures
dll.GetChartBitmapBytes.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int)]
dll.GetChartBitmapBytes.restype = ctypes.c_bool

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TeeChart via Bitmap with PyQt")
        self.resize(600, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label to display the image
        self.image_label = QLabel("Loading chart...")
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)

        self.load_chart_from_dll()

    def load_chart_from_dll(self):
        buffer_ptr = ctypes.c_void_p()
        size = ctypes.c_int()

        if dll.GetChartBitmapBytes(ctypes.byref(buffer_ptr), ctypes.byref(size)):
            # 1. Read bytes directly from the DLL's memory
            raw_data = ctypes.string_at(buffer_ptr.value, size.value)
            
            # 2. Convert with Pillow to PNG format for PyQt
            img = Image.open(io.BytesIO(raw_data))
            
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='PNG')
            png_bytes = byte_arr.getvalue()

            # 3. Load into QPixmap and display on QLabel
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(png_bytes))
            
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Error generating chart from DLL.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
