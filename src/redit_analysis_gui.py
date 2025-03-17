import os
import joblib
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tải mô hình đã huấn luyện từ thư mục models
model_path = os.path.join("models", "credit_risk_model.joblib")
try:
    model = joblib.load(model_path)
except Exception as e:
    messagebox.showerror("Lỗi", f"Mô hình không được tải: {e}")
    model = None

# Danh sách các feature cần thiết
FEATURES = ["age", "income", "credit_score", "loan_amount", "debt_to_income"]

current_report = ""

def predict_risk():
    global current_report
    if model is None:
        messagebox.showerror("Lỗi", "Mô hình không được tải thành công.")
        return
    try:
        input_data = {
            "age": float(age_var.get()),
            "income": float(income_var.get()),
            "credit_score": float(credit_score_var.get()),
            "loan_amount": float(loan_amount_var.get()),
            "debt_to_income": float(debt_to_income_var.get())
        }
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số cho tất cả các trường.")
        return

    df = pd.DataFrame([input_data])
    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể dự đoán: {e}")
        return

    mapping = {0: "Low", 1: "Medium", 2: "High"}
    risk_level = mapping.get(prediction, "Unknown")
    result_text = f"Predicted risk level: {risk_level}"
    result_var.set(result_text)
    
    # Tạo báo cáo chi tiết
    current_report = (f"Credit Analysis Report\n\n"
                      f"Input Data:\n"
                      f"  Age: {input_data['age']}\n"
                      f"  Income: {input_data['income']}\n"
                      f"  Credit Score: {input_data['credit_score']}\n"
                      f"  Loan Amount: {input_data['loan_amount']}\n"
                      f"  Debt-to-Income Ratio: {input_data['debt_to_income']}\n\n"
                      f"Predicted risk level: {risk_level}")
    
    # Cập nhật nội dung trong tab Details
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, current_report + "\n\n" + details_info())
    details_text.config(state="disabled")
    
    messagebox.showinfo("Kết quả dự đoán", current_report)

def show_graph():
    # Xây dựng đồ thị trên tab Graph
    standards = {"Low": 40, "Medium": 30, "High": 30}
    categories = list(standards.keys())
    values = list(standards.values())
    
    predicted = None
    if result_var.get():
        parts = result_var.get().split(":")
        if len(parts) == 2:
            predicted = parts[1].strip()
    
    fig, ax = plt.subplots(figsize=(5,4))
    bars = ax.bar(categories, values, color=["blue"]*len(categories))
    if predicted in categories:
        idx = categories.index(predicted)
        bars[idx].set_color("green")
    ax.set_ylabel("Standard Value")
    ax.set_title("Risk Level Comparison")
    
    # Tích hợp đồ thị vào canvas trong tab Graph
    for widget in graph_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def save_report():
    if not current_report:
        messagebox.showerror("Lỗi", "Chưa có báo cáo nào để lưu. Vui lòng dự đoán trước.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(current_report)
            messagebox.showinfo("Thông báo", f"Báo cáo đã được lưu tại: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu báo cáo: {e}")

def print_report():
    if not current_report:
        messagebox.showerror("Lỗi", "Chưa có báo cáo nào để in. Vui lòng dự đoán trước.")
        return
    messagebox.showinfo("Báo cáo", current_report)

def view_details():
    # Chức năng này đã được tích hợp vào tab "Details & Report"
    tab_control.select(details_tab)

def details_info():
    # Giả lập chi tiết các biến số
    info = ("Chi tiết các biến số ảnh hưởng đến kết quả dự đoán:\n"
            "- Age: Độ tuổi của khách hàng, ảnh hưởng đến khả năng vay mượn.\n"
            "- Income: Thu nhập của khách hàng, cho biết khả năng chi trả.\n"
            "- Credit Score: Điểm tín dụng, phản ánh lịch sử tín dụng của khách hàng.\n"
            "- Loan Amount: Số tiền vay, nếu quá cao có thể gây áp lực tài chính.\n"
            "- Debt-to-Income Ratio: Tỷ lệ nợ trên thu nhập, chỉ số quan trọng về khả năng trả nợ.")
    return info

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Credit Analysis App")
root.geometry("600x600")
root.resizable(False, False)

# Các biến lưu trữ dữ liệu nhập
age_var = tk.StringVar()
income_var = tk.StringVar()
credit_score_var = tk.StringVar()
loan_amount_var = tk.StringVar()
debt_to_income_var = tk.StringVar()
result_var = tk.StringVar()

# Tạo Notebook để quản lý các tab
tab_control = ttk.Notebook(root)
tab_control.pack(fill=tk.BOTH, expand=True)

# Tab 1: Predict
predict_tab = ttk.Frame(tab_control)
tab_control.add(predict_tab, text="Predict")

# Tab 2: Graph
graph_tab = ttk.Frame(tab_control)
tab_control.add(graph_tab, text="Graph")

# Tab 3: Details & Report
details_tab = ttk.Frame(tab_control)
tab_control.add(details_tab, text="Details & Report")

# --- Giao diện tab Predict ---
predict_frame = ttk.Frame(predict_tab, padding="20")
predict_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(predict_frame, text="Credit Analysis App", font=("Arial", 16))
title_label.pack(pady=10)

def create_input_field(parent, label_text, variable):
    label = ttk.Label(parent, text=label_text)
    label.pack(anchor=tk.W, pady=2)
    entry = ttk.Entry(parent, textvariable=variable)
    entry.pack(fill=tk.X, pady=2)

create_input_field(predict_frame, "Age:", age_var)
create_input_field(predict_frame, "Income:", income_var)
create_input_field(predict_frame, "Credit Score:", credit_score_var)
create_input_field(predict_frame, "Loan Amount:", loan_amount_var)
create_input_field(predict_frame, "Debt-to-Income Ratio:", debt_to_income_var)

# Nút dự đoán nằm ngang
button_frame = ttk.Frame(predict_frame)
button_frame.pack(pady=10, fill=tk.X)

predict_button = ttk.Button(button_frame, text="Predict", command=predict_risk)
predict_button.pack(side=tk.LEFT, padx=5)

# Nút View Details (chuyển tab Details)
details_button = ttk.Button(button_frame, text="View Details", command=view_details)
details_button.pack(side=tk.LEFT, padx=5)

# Nút Save Report
save_button = ttk.Button(button_frame, text="Save Report", command=save_report)
save_button.pack(side=tk.LEFT, padx=5)

# Nút Print Report
print_button = ttk.Button(button_frame, text="Print Report", command=print_report)
print_button.pack(side=tk.LEFT, padx=5)

# Label hiển thị kết quả dự đoán
result_label = ttk.Label(predict_frame, textvariable=result_var, font=("Arial", 12), foreground="blue")
result_label.pack(pady=10)

# --- Giao diện tab Graph ---
graph_frame = ttk.Frame(graph_tab, padding="20")
graph_frame.pack(fill=tk.BOTH, expand=True)

# Nút cập nhật đồ thị (nếu muốn làm mới đồ thị)
graph_update_button = ttk.Button(graph_frame, text="Update Graph", command=show_graph)
graph_update_button.pack(pady=10)

# --- Giao diện tab Details & Report ---
details_frame = ttk.Frame(details_tab, padding="20")
details_frame.pack(fill=tk.BOTH, expand=True)

details_label = ttk.Label(details_frame, text="Report Details", font=("Arial", 14))
details_label.pack(pady=10)

# Text widget để hiển thị báo cáo chi tiết
details_text = tk.Text(details_frame, wrap="word", font=("Arial", 10), height=15)
details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
details_text.insert(tk.END, "Chưa có báo cáo. Vui lòng thực hiện dự đoán để xem chi tiết.")
details_text.config(state="disabled")

root.mainloop()
