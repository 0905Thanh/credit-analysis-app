# tests/test_gui.py
import unittest
import tkinter as tk
from src.gui import run_app

class TestGUI(unittest.TestCase):
    def test_run_app_initialization(self):
        # Kiểm tra xem có thể tạo và hủy một cửa sổ Tkinter mà không lỗi.
        try:
            root = tk.Tk()
            root.destroy()
        except Exception as e:
            self.fail(f"Khởi tạo GUI thất bại: {e}")

if __name__ == "__main__":
    unittest.main()
