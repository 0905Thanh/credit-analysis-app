# src/gui.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from src.analysis import process_input_data, load_model, predict_credit_risk

# Đường dẫn tới mô hình
MODEL_PATH = os.path.join("models", "credit_risk_model.joblib")
model = load_model(MODEL_PATH)

def run_app():
    root = tk.Tk()
    root.title("Ứng Dụng Phân Tích Tín Dụng")
    
    # Khai báo các biến lưu trữ dữ liệu
    age_var = tk.StringVar()
    job_var = tk.StringVar()
    main_salary_var = tk.StringVar()
    passive_salary_var = tk.StringVar()
    credit_score_var = tk.StringVar()
    loan_amount_var = tk.StringVar()
    debt_to_income_var = tk.StringVar()
    bank_rate_var = tk.StringVar()
    repayment_period_var = tk.StringVar()
    result_var = tk.StringVar()
    
    # Biến tự động tính Tổng thu nhập
    total_income_var = tk.StringVar()

    def update_total_income(*args):
        try:
            total = float(main_salary_var.get() or 0) + float(passive_salary_var.get() or 0)
        except ValueError:
            total = 0
        total_income_var.set(f"{total:.2f}")

    main_salary_var.trace("w", update_total_income)
    passive_salary_var.trace("w", update_total_income)
    
    # Thiết lập giao diện sử dụng grid layout
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)
    
    row = 0
    ttk.Label(frame, text="Tuổi:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=age_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Nghề nghiệp:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=job_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Lương chính:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=main_salary_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Lương thụ động:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=passive_salary_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Tổng thu nhập:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=total_income_var, state="readonly").grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Điểm tín dụng:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=credit_score_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Số tiền vay:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=loan_amount_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Tỷ lệ nợ trên thu nhập:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=debt_to_income_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Lãi suất ngân hàng:").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=bank_rate_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Thời gian chi trả (tháng):").grid(row=row, column=0, sticky="w")
    ttk.Entry(frame, textvariable=repayment_period_var).grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, textvariable=result_var, foreground="blue").grid(row=row, column=0, columnspan=2)
    row += 1

    def on_predict():
        # Thu thập dữ liệu từ giao diện
        input_data = {
            "age": age_var.get(),
            "job": job_var.get(),
            "main_salary": main_salary_var.get(),
            "passive_salary": passive_salary_var.get(),
            "total_income": total_income_var.get(),
            "credit_score": credit_score_var.get(),
            "loan_amount": loan_amount_var.get(),
            "debt_to_income": debt_to_income_var.get(),
            "bank_rate": bank_rate_var.get(),
            "repayment_period": repayment_period_var.get(),
        }
        try:
            df = process_input_data(input_data)
            pred = predict_credit_risk(model, df)
            mapping = {0: "Thấp", 1: "Trung bình", 2: "Cao"}
            risk_level = mapping.get(pred, "Không xác định")
            result_var.set(f"Mức rủi ro: {risk_level}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {e}")
    
    ttk.Button(frame, text="Dự đoán", command=on_predict).grid(row=row, column=0, columnspan=2)
    
    frame.columnconfigure(1, weight=1)
    root.mainloop()
