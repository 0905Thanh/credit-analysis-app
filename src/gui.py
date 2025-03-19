import tkinter as tk
from tkinter import messagebox, filedialog
from src.analysis import calculate_emi, calculate_dti, calculate_loan_to_income, predict_credit_risk  # Import các hàm tính toán

def predict_risk(age_var, main_salary_var, passive_salary_var, credit_score_var, loan_amount_var, bank_rate_var, repayment_period_var, result_var, advice_var, report_var):
    # Lấy dữ liệu từ giao diện
    age = float(age_var.get())
    main_salary = float(main_salary_var.get())
    passive_salary = float(passive_salary_var.get())
    credit_score = float(credit_score_var.get())
    loan_amount = float(loan_amount_var.get())
    bank_rate = float(bank_rate_var.get())
    repayment_period = int(repayment_period_var.get())
    
    # Tính toán các chỉ số tài chính
    total_income = main_salary + passive_salary
    emi = calculate_emi(loan_amount, bank_rate, repayment_period)
    dti = calculate_dti(total_income, emi)  # Tính tỷ lệ nợ trên thu nhập
    loan_to_income = calculate_loan_to_income(loan_amount, total_income)

    # Hiển thị các chỉ số đã tính
    result_text = f"Tổng thu nhập: {total_income}\n"
    result_text += f"EMI: {emi}\n"
    result_text += f"DTI: {dti}\n"
    result_text += f"Loan-to-Income: {loan_to_income}\n"
    
    # Chuẩn bị dữ liệu đầu vào cho mô hình
    input_data = {
        "age": age,
        "total_income": total_income,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "debt_to_income": dti,  # Truyền DTI đã tính toán
        "emi": emi,
        "dti": dti,
        "loan_to_income": loan_to_income
    }
    
    # Dự đoán mức độ rủi ro
    risk_level = predict_credit_risk(input_data)

    result_text += f"\nPredicted Risk Level: {risk_level}"

    # Cập nhật giao diện với kết quả dự đoán
    result_var.set(result_text)

    # Đưa ra lời khuyên
    if risk_level == "High":
        advice = "Chúng tôi khuyên bạn nên giảm số tiền vay hoặc kéo dài thời gian chi trả để giảm áp lực tài chính."
    elif risk_level == "Medium":
        advice = "Hãy xem xét việc điều chỉnh thời gian chi trả để phù hợp với khả năng thanh toán."
    else:
        advice = "Chúc mừng! Bạn có mức độ rủi ro tín dụng thấp. Bạn có thể tiến hành vay với các điều kiện thuận lợi."

    # Hiển thị lời khuyên
    advice_var.set(advice)

    # Tạo báo cáo chi tiết
    report_text = f"--- Báo Cáo Chi Tiết ---\n\n"
    report_text += f"Thông tin khách hàng:\n"
    report_text += f"Tuổi: {age}\n"
    report_text += f"Thu nhập chính: {main_salary}\n"
    report_text += f"Thu nhập thụ động: {passive_salary}\n"
    report_text += f"Điểm tín dụng: {credit_score}\n"
    report_text += f"Số tiền vay: {loan_amount}\n"
    report_text += f"Tỷ lệ nợ trên thu nhập: {dti}\n\n"
    report_text += f"Chỉ số tài chính:\n"
    report_text += f"Tổng thu nhập: {total_income}\n"
    report_text += f"EMI: {emi}\n"
    report_text += f"DTI: {dti}\n"
    report_text += f"Loan-to-Income: {loan_to_income}\n\n"
    report_text += f"Mức độ rủi ro dự đoán: {risk_level}\n"
    report_text += f"Lời khuyên: {advice}"

    # Cập nhật báo cáo vào giao diện
    report_var.set(report_text)

    messagebox.showinfo("Kết quả dự đoán", result_text)

def save_report(report_text):
    # Lưu báo cáo vào file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(report_text)
        messagebox.showinfo("Thông báo", f"Báo cáo đã được lưu tại {file_path}")

def run_app():
    root = tk.Tk()
    root.title("Ứng Dụng Phân Tích Rủi Ro Tín Dụng")
    root.geometry("500x600")

    # Các biến lưu trữ dữ liệu nhập
    name_var = tk.StringVar()  # Tên khách hàng
    age_var = tk.StringVar()   # Tuổi
    occupation_var = tk.StringVar()  # Nghề nghiệp
    main_salary_var = tk.StringVar()
    passive_salary_var = tk.StringVar()
    credit_score_var = tk.StringVar()
    loan_amount_var = tk.StringVar()
    bank_rate_var = tk.StringVar()
    repayment_period_var = tk.StringVar()
    result_var = tk.StringVar()
    advice_var = tk.StringVar()
    report_var = tk.StringVar()

    # Các trường nhập liệu
    tk.Label(root, text="Tên khách hàng:").pack()
    tk.Entry(root, textvariable=name_var).pack()

    tk.Label(root, text="Tuổi:").pack()
    tk.Entry(root, textvariable=age_var).pack()

    tk.Label(root, text="Nghề nghiệp:").pack()
    tk.Entry(root, textvariable=occupation_var).pack()

    tk.Label(root, text="Lương chính:").pack()
    tk.Entry(root, textvariable=main_salary_var).pack()

    tk.Label(root, text="Lương thụ động:").pack()
    tk.Entry(root, textvariable=passive_salary_var).pack()

    tk.Label(root, text="Điểm tín dụng:").pack()
    tk.Entry(root, textvariable=credit_score_var).pack()

    tk.Label(root, text="Số tiền vay:").pack()
    tk.Entry(root, textvariable=loan_amount_var).pack()

    tk.Label(root, text="Lãi suất ngân hàng:").pack()
    tk.Entry(root, textvariable=bank_rate_var).pack()

    tk.Label(root, text="Thời gian chi trả (tháng):").pack()
    tk.Entry(root, textvariable=repayment_period_var).pack()

    # Nút Dự đoán
    predict_button = tk.Button(root, text="Dự đoán", command=lambda: predict_risk(age_var, main_salary_var, passive_salary_var, credit_score_var, loan_amount_var, bank_rate_var, repayment_period_var, result_var, advice_var, report_var))
    predict_button.pack()

    # Kết quả dự đoán
    tk.Label(root, text="Kết quả dự đoán:").pack()
    tk.Label(root, textvariable=result_var).pack()

    # Lời khuyên
    tk.Label(root, text="Lời khuyên:").pack()
    tk.Label(root, textvariable=advice_var).pack()

    # Báo cáo chi tiết
    tk.Label(root, text="Báo cáo chi tiết:").pack()
    tk.Label(root, textvariable=report_var).pack()

    # Nút lưu báo cáo
    save_button = tk.Button(root, text="Lưu Báo Cáo", command=lambda: save_report(report_var.get()))
    save_button.pack()

    # Chạy ứng dụng
    root.mainloop()

# Gọi hàm run_app khi chạy chương trình
if __name__ == "__main__":
    run_app()
