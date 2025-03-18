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

current_report = ""

def predict_risk():
    global current_report
    if model is None:
        messagebox.showerror("Lỗi", "Mô hình không được tải thành công.")
        return
    try:
        # Thu thập dữ liệu từ các trường nhập hiện tại (chỉ sử dụng các trường mô hình yêu cầu)
        input_data = {
            "age": float(age_var.get()),
            # Lấy tổng thu nhập từ tong_thu_nhap_var
            "income": float(tong_thu_nhap_var.get()),
            "credit_score": float(credit_score_var.get()),
            "loan_amount": float(loan_amount_var.get()),
            "debt_to_income": float(debt_to_income_var.get())
        }
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số cho các trường số.")
        return

    df = pd.DataFrame([input_data])
    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể dự đoán: {e}")
        return

    mapping = {0: "Thấp", 1: "Trung bình", 2: "Cao"}
    risk_level = mapping.get(prediction, "Không xác định")
    result_text = f"Mức rủi ro dự đoán: {risk_level}"
    result_var.set(result_text)
    
    # Tạo báo cáo chi tiết, tích hợp thông tin từ các trường nhập mới
    current_report = (
        f"Báo cáo Phân Tích Tín Dụng\n\n"
        f"Dữ liệu nhập:\n"
        f"  Tuổi: {age_var.get()}\n"
        f"  Nghề nghiệp: {job_var.get()}\n"
        f"  Lương chính: {main_salary_var.get()}\n"
        f"  Lương thụ động: {passive_salary_var.get()}\n"
        f"  Tổng thu nhập: {tong_thu_nhap_var.get()}\n"
        f"  Điểm tín dụng: {credit_score_var.get()}\n"
        f"  Số tiền vay: {loan_amount_var.get()}\n"
        f"  Tỷ lệ nợ trên thu nhập: {debt_to_income_var.get()}\n"
        f"  Lãi suất ngân hàng: {bank_rate_var.get()}\n"
        f"  Thời gian chi trả (tháng): {repayment_period_var.get()}\n\n"
        f"Mức rủi ro dự đoán: {risk_level}"
    )
    
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, current_report + "\n\n" + details_info())
    details_text.config(state="disabled")
    
    messagebox.showinfo("Kết quả dự đoán", current_report)

def show_graph():
    standards = {"Thấp": 40, "Trung bình": 30, "Cao": 30}
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
    ax.set_ylabel("Giá trị tiêu chuẩn")
    ax.set_title("So sánh mức rủi ro")
    
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
    tab_control.select(details_tab)

def details_info():
    info = (
        "Chi tiết các biến số ảnh hưởng đến kết quả dự đoán:\n"
        "- Tuổi: Độ tuổi của khách hàng.\n"
        "- Nghề nghiệp: Loại hình công việc của khách hàng.\n"
        "- Lương chính & Lương thụ động: Các nguồn thu nhập cơ bản và phụ, đánh giá khả năng tài chính.\n"
        "- Tổng thu nhập: Tổng của Lương chính và Lương thụ động.\n"
        "- Điểm tín dụng: Lịch sử tín dụng của khách hàng.\n"
        "- Số tiền vay: Khoản vay yêu cầu, có thể gây áp lực nếu quá cao.\n"
        "- Tỷ lệ nợ trên thu nhập: Chỉ số quan trọng về khả năng trả nợ.\n"
        "- Lãi suất ngân hàng: Lãi suất áp dụng cho khoản vay.\n"
        "- Thời gian chi trả: Khoảng thời gian dự kiến để hoàn tất khoản vay."
    )
    return info

def update_total_income(*args):
    try:
        # Chuyển đổi Lương chính và Lương thụ động thành số, nếu không thì trả về 0
        main_salary = float(main_salary_var.get()) if main_salary_var.get() else 0
        passive_salary = float(passive_salary_var.get()) if passive_salary_var.get() else 0
        total = main_salary + passive_salary
    except ValueError:
        total = 0
    tong_thu_nhap_var.set(f"{total:.2f}")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng Dụng Phân Tích Tín Dụng")
root.geometry("600x750")
root.resizable(False, False)

# Khai báo các biến lưu trữ dữ liệu nhập
age_var = tk.StringVar()
job_var = tk.StringVar()
main_salary_var = tk.StringVar()
passive_salary_var = tk.StringVar()
tong_thu_nhap_var = tk.StringVar()  # Biến cho Tổng thu nhập
credit_score_var = tk.StringVar()
loan_amount_var = tk.StringVar()
debt_to_income_var = tk.StringVar()
bank_rate_var = tk.StringVar()
repayment_period_var = tk.StringVar()
result_var = tk.StringVar()

# Cập nhật tổng thu nhập mỗi khi Lương chính hoặc Lương thụ động thay đổi
main_salary_var.trace("w", update_total_income)
passive_salary_var.trace("w", update_total_income)

# Tạo Notebook để quản lý các tab
tab_control = ttk.Notebook(root)
tab_control.pack(fill=tk.BOTH, expand=True)

# Tab Dự đoán
predict_tab = ttk.Frame(tab_control)
tab_control.add(predict_tab, text="Dự đoán")

# Tab Đồ thị
graph_tab = ttk.Frame(tab_control)
tab_control.add(graph_tab, text="Đồ thị")

# Tab Chi tiết & Báo cáo
details_tab = ttk.Frame(tab_control)
tab_control.add(details_tab, text="Chi tiết & Báo cáo")

# --- Giao diện tab Dự đoán ---
predict_frame = ttk.Frame(predict_tab, padding="20")
predict_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(predict_frame, text="Ứng Dụng Phân Tích Tín Dụng", font=("Arial", 16))
title_label.pack(pady=10)

def create_input_field(parent, label_text, variable, readonly=False):
    label = ttk.Label(parent, text=label_text)
    label.pack(anchor=tk.W, pady=2)
    entry = ttk.Entry(parent, textvariable=variable)
    if readonly:
        entry.config(state="readonly")
    entry.pack(fill=tk.X, pady=2)

# Sắp xếp các trường nhập liệu theo thứ tự hợp lý
create_input_field(predict_frame, "Tuổi:", age_var)
create_input_field(predict_frame, "Nghề nghiệp:", job_var)
create_input_field(predict_frame, "Lương chính:", main_salary_var)
create_input_field(predict_frame, "Lương thụ động:", passive_salary_var)
# Hiển thị Tổng thu nhập dưới dạng chỉ đọc (tính tự động)
create_input_field(predict_frame, "Tổng thu nhập:", tong_thu_nhap_var, readonly=True)
create_input_field(predict_frame, "Điểm tín dụng:", credit_score_var)
create_input_field(predict_frame, "Số tiền vay:", loan_amount_var)
create_input_field(predict_frame, "Tỷ lệ nợ trên thu nhập:", debt_to_income_var)

# Trường chọn Lãi suất ngân hàng (ComboBox)
label_bank = ttk.Label(predict_frame, text="Lãi suất ngân hàng:")
label_bank.pack(anchor=tk.W, pady=2)
combo_bank_rate = ttk.Combobox(predict_frame, textvariable=bank_rate_var, 
                               values=["Ngân hàng A - 7%", "Ngân hàng B - 8%", "Ngân hàng C - 9%"])
combo_bank_rate.pack(fill=tk.X, pady=2)
combo_bank_rate.current(0)

# Trường nhập Thời gian chi trả (tháng)
create_input_field(predict_frame, "Thời gian chi trả (tháng):", repayment_period_var)

# Nút điều khiển
button_frame = ttk.Frame(predict_frame)
button_frame.pack(pady=10, fill=tk.X)

predict_button = ttk.Button(button_frame, text="Dự đoán", command=predict_risk)
predict_button.pack(side=tk.LEFT, padx=5)

details_button = ttk.Button(button_frame, text="Xem chi tiết", command=view_details)
details_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(button_frame, text="Lưu báo cáo", command=save_report)
save_button.pack(side=tk.LEFT, padx=5)

print_button = ttk.Button(button_frame, text="In báo cáo", command=print_report)
print_button.pack(side=tk.LEFT, padx=5)

result_label = ttk.Label(predict_frame, textvariable=result_var, font=("Arial", 12), foreground="blue")
result_label.pack(pady=10)

# --- Giao diện tab Đồ thị ---
graph_frame = ttk.Frame(graph_tab, padding="20")
graph_frame.pack(fill=tk.BOTH, expand=True)

graph_update_button = ttk.Button(graph_frame, text="Cập nhật đồ thị", command=show_graph)
graph_update_button.pack(pady=10)

# --- Giao diện tab Chi tiết & Báo cáo ---
details_frame = ttk.Frame(details_tab, padding="20")
details_frame.pack(fill=tk.BOTH, expand=True)

details_label = ttk.Label(details_frame, text="Chi tiết báo cáo", font=("Arial", 14))
details_label.pack(pady=10)

details_text = tk.Text(details_frame, wrap="word", font=("Arial", 10), height=15)
details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
details_text.insert(tk.END, "Chưa có báo cáo. Vui lòng thực hiện dự đoán để xem chi tiết.")
details_text.config(state="disabled")

root.mainloop()
