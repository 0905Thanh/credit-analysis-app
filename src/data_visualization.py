import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Hàm tạo biểu đồ Histogram
def plot_histogram(data, frame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data, bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Histogram')
    ax.set_xlabel('Giá trị')
    ax.set_ylabel('Tần suất')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

# Hàm tạo biểu đồ Boxplot
def plot_boxplot(data, frame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(data)
    ax.set_title('Boxplot')
    ax.set_ylabel('Giá trị')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

# Hàm tạo biểu đồ Scatter plot
def plot_scatter(x_data, y_data, frame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x_data, y_data, color='blue')
    ax.set_title('Scatter plot')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

# Hàm tạo biểu đồ Heatmap
def plot_heatmap(data, frame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(data, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Heatmap')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

# Hàm để hiển thị biểu đồ phân bố dữ liệu và biểu đồ quan hệ từ file hoặc dữ liệu người dùng nhập
# Trong data_visualization.py

def show_data_visualization_from_file_or_input(frame, data=None):
    # Nếu không có dữ liệu đầu vào, mở hộp thoại để chọn file
    if data is None:
        file_path = filedialog.askopenfilename(title="Chọn file dữ liệu", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)  # Đọc dữ liệu từ file CSV
        elif file_path.endswith(".xlsx"):
            data = pd.read_excel(file_path)  # Đọc dữ liệu từ file Excel
        else:
            print("File không hợp lệ!")
            return

    # Kiểm tra dữ liệu và vẽ biểu đồ tương ứng
    if data is not None:
        # Lập biểu đồ Histogram cho cột đầu tiên
        if data.select_dtypes(include=[np.number]).shape[1] > 0:
            plot_histogram(data.iloc[:, 0], frame)

        # Lập biểu đồ Boxplot cho cột đầu tiên
        plot_boxplot(data.iloc[:, 0], frame)

        # Lập biểu đồ Scatter nếu có ít nhất hai cột số
        if data.shape[1] > 1:
            plot_scatter(data.iloc[:, 0], data.iloc[:, 1], frame)

        # Nếu có dữ liệu ma trận, vẽ Heatmap
        if data.shape[0] > 1 and data.shape[1] > 1:
            corr_matrix = data.corr()  # Tính toán ma trận tương quan
            plot_heatmap(corr_matrix, frame)

