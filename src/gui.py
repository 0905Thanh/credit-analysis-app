import tkinter as tk
from tkinter import messagebox, ttk
from src.data_visualization import show_data_visualization_from_file_or_input  # Import từ data_visualization.py
from src.analysis import calculate_emi, calculate_dti, calculate_loan_to_income, predict_credit_risk
from src.payment_schedule import generate_payment_schedule
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.report_generator import generate_report  # Import hàm tạo báo cáo chi tiết
from tkinter.simpledialog import askstring

def save_report(report_text):
    """
    Hàm lưu báo cáo chi tiết vào tệp văn bản.
    """
    try:
        with open("report.txt", "w", encoding="utf-8") as file:
            file.write(report_text)
        messagebox.showinfo("Thông báo", "Báo cáo đã được lưu thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu báo cáo: {str(e)}")


def predict_risk(age_var, main_salary_var, passive_salary_var, credit_score_var, loan_amount_var, bank_rate_var, repayment_period_var, result_var, advice_var, report_var, name_var, occupation_var, report_display):
    try:
        age = int(age_var.get()) if age_var.get() else 0
        if age < 18:
            messagebox.showerror("Lỗi", "Không đủ tuổi để vay mượn")
            return

        if not age_var.get() or not main_salary_var.get() or not passive_salary_var.get() or not credit_score_var.get() or not loan_amount_var.get() or not bank_rate_var.get() or not repayment_period_var.get():
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tất cả các trường dữ liệu.")
            return

        # Chuyển các giá trị nhập thành float
        main_salary = float(main_salary_var.get()) if main_salary_var.get() else 0
        passive_salary = float(passive_salary_var.get()) if passive_salary_var.get() else 0
        credit_score = float(credit_score_var.get()) if credit_score_var.get() else 0
        loan_amount = float(loan_amount_var.get()) if loan_amount_var.get() else 0
        bank_rate = float(bank_rate_var.get()) if bank_rate_var.get() else 0
        repayment_period = int(repayment_period_var.get()) if repayment_period_var.get() else 0

        if age <= 0 or main_salary <= 0 or passive_salary < 0 or credit_score <= 0 or loan_amount <= 0 or bank_rate <= 0 or repayment_period <= 0:
            messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu hợp lệ cho tất cả các trường.")
            return

        # Tính toán các chỉ số tài chính
        total_income = main_salary + passive_salary
        emi = calculate_emi(loan_amount, bank_rate, repayment_period)
        dti = calculate_dti(total_income, emi)  # Tính tỷ lệ nợ trên thu nhập
        loan_to_income = calculate_loan_to_income(loan_amount, total_income)

        # Dự đoán mức độ rủi ro
        input_data = {
            "name": name_var.get(),  # Thêm biến name_var
            "occupation": occupation_var.get(),  # Thêm biến occupation_var
            "age": age,
            "total_income": total_income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "main_salary": main_salary,  # Đảm bảo có 'main_salary'
            'passive_salary': passive_salary,
            'bank_rate': bank_rate,
            'repayment_period': repayment_period,
            "debt_to_income": dti,  # Truyền DTI đã tính toán
            "emi": emi,
            "dti": dti,
            "loan_to_income": loan_to_income
        }

        # Dự đoán mức độ rủi ro
        risk_level = predict_credit_risk(input_data)

        result_text = f"Tổng thu nhập: {total_income}\nEMI: {emi}\nDTI: {dti}\nLoan-to-Income: {loan_to_income}\nPredicted Risk Level: {risk_level}"
        result_var.set(result_text)

        # Đưa ra lời khuyên
        if risk_level == "High":
            advice = "Chúng tôi khuyên bạn nên giảm số tiền vay hoặc kéo dài thời gian chi trả để giảm áp lực tài chính."
        elif risk_level == "Medium":
            advice = "Hãy xem xét việc điều chỉnh thời gian chi trả để phù hợp với khả năng thanh toán."
        else:
            advice = "Chúc mừng! Bạn có mức độ rủi ro tín dụng thấp. Bạn có thể tiến hành vay với các điều kiện thuận lợi."

        advice_var.set(advice)

        # Tạo báo cáo chi tiết
        report_text = generate_report(input_data, emi, dti, loan_to_income, risk_level, advice)
        report_var.set(report_text)

        # Hiển thị báo cáo chi tiết trong phần Text
        report_display.config(state=tk.NORMAL)  # Cho phép chỉnh sửa báo cáo
        report_display.delete(1.0, tk.END)  # Xóa báo cáo cũ
        report_display.insert(tk.END, report_text)  # Hiển thị báo cáo mới
        report_display.config(state=tk.DISABLED)  # Không cho chỉnh sửa báo cáo

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu hợp lệ cho tất cả các trường.")


# Nút để hiển thị biểu đồ
def show_visualization_button_click(visualization_tab, data=None):
    show_data_visualization_from_file_or_input(visualization_tab, data)

# Thêm nút để hiển thị lộ trình thanh toán
def show_payment_schedule(loan_amount_var, bank_rate_var, repayment_period_var, frame):
    try:
        loan_amount = float(loan_amount_var.get())
        bank_rate = float(bank_rate_var.get())
        repayment_period = int(repayment_period_var.get())

        emi = calculate_emi(loan_amount, bank_rate, repayment_period)

        fig = generate_payment_schedule(loan_amount, emi, repayment_period)

        # Hiển thị biểu đồ thanh toán trên cửa sổ mới
        fig_canvas = FigureCanvasTkAgg(fig, master=frame)
        fig_canvas.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu hợp lệ.")


def run_app():
    root = tk.Tk()
    root.title("Ứng Dụng Phân Tích Rủi Ro Tín Dụng")
    root.geometry("900x700")
    root.configure(bg='#e0f7fa')  # Thêm màu nền nhẹ cho cửa sổ chính

    # Tạo notebook (tab) để chứa các tab
    tab_control = ttk.Notebook(root)
    tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tạo các tab
    predict_tab = ttk.Frame(tab_control)
    tab_control.add(predict_tab, text="Dự đoán rủi ro", padding=10)

    payment_schedule_tab = ttk.Frame(tab_control)
    tab_control.add(payment_schedule_tab, text="Lộ trình thanh toán", padding=10)

    report_tab = ttk.Frame(tab_control)  # Thêm tab báo cáo
    tab_control.add(report_tab, text="Báo cáo chi tiết", padding=10)

    visualization_tab = ttk.Frame(tab_control)  # Thêm tab biểu đồ
    tab_control.add(visualization_tab, text="Biểu đồ phân tích", padding=10)

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

    # Tạo danh sách ngân hàng và lãi suất tương ứng
    bank_rates = {
        "Vietcombank (7%)": 7.0,
        "VietinBank (7.5%)": 7.5,
        "BIDV (8%)": 8.0,
        "Sacombank (7.8%)": 7.8,
        "Techcombank (6.9%)": 6.9
    }

    # Các trường nhập liệu trong tab "Dự đoán rủi ro"
    tk.Label(predict_tab, text="Tên khách hàng:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=name_var, width=30, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Tuổi:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=age_var, width=30, font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Nghề nghiệp:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=occupation_var, width=30, font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Lương chính:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=main_salary_var, width=30, font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Lương thụ động:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=passive_salary_var, width=30, font=("Arial", 12)).grid(row=4, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Điểm tín dụng:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=5, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=credit_score_var, width=30, font=("Arial", 12)).grid(row=5, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Số tiền vay:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=6, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=loan_amount_var, width=30, font=("Arial", 12)).grid(row=6, column=1, padx=10, pady=10)

    tk.Label(predict_tab, text="Lãi suất ngân hàng:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=7, column=0, padx=10, pady=10, sticky="w")
    bank_combobox = ttk.Combobox(predict_tab, values=list(bank_rates.keys()), state="readonly", font=("Arial", 12))
    bank_combobox.set("Chọn ngân hàng")
    bank_combobox.grid(row=7, column=1, padx=10, pady=10)

    # Cập nhật lãi suất khi người dùng chọn ngân hàng
    def update_bank_rate(event):
        selected_bank = bank_combobox.get()
        bank_rate_var.set(bank_rates.get(selected_bank, 0))

    bank_combobox.bind("<<ComboboxSelected>>", update_bank_rate)

    tk.Label(predict_tab, text="Thời gian chi trả (tháng):", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=8, column=0, padx=10, pady=10, sticky="w")
    tk.Entry(predict_tab, textvariable=repayment_period_var, width=30, font=("Arial", 12)).grid(row=8, column=1, padx=10, pady=10)

    # Nút Dự đoán
    predict_button = tk.Button(predict_tab, text="Dự đoán", command=lambda: predict_risk(age_var, main_salary_var, passive_salary_var, credit_score_var, loan_amount_var, bank_rate_var, repayment_period_var, result_var, advice_var, report_var, name_var, occupation_var, report_display), bg="#4CAF50", fg="white", font=("Arial", 12, 'bold'))
    predict_button.grid(row=9, column=0, columnspan=2, pady=20)

    # Nút Báo cáo lộ trình thanh toán
    payment_schedule_button = tk.Button(predict_tab, text="Hiển thị lộ trình thanh toán", command=lambda: show_payment_schedule(loan_amount_var, bank_rate_var, repayment_period_var, payment_schedule_tab), bg="#2196F3", fg="white", font=("Arial", 12, 'bold'))
    payment_schedule_button.grid(row=10, column=0, columnspan=2, pady=20)

    # Thêm nút để hiển thị biểu đồ từ file hoặc dữ liệu người dùng nhập
    show_visualization_button = tk.Button(visualization_tab, text="Hiển thị biểu đồ từ file hoặc nhập liệu", command=lambda: show_visualization_button_click(visualization_tab), bg="#FFC107", fg="white", font=("Arial", 12, 'bold'))
    show_visualization_button.pack(pady=10)

    # Kết quả dự đoán
    tk.Label(predict_tab, text="Kết quả dự đoán:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=11, column=0, padx=10, pady=10, sticky="w")
    tk.Label(predict_tab, textvariable=result_var, bg="#e0f7fa", font=("Arial", 12)).grid(row=11, column=1, padx=10, pady=10)

    # Lời khuyên
    tk.Label(predict_tab, text="Lời khuyên:", bg="#e0f7fa", font=("Arial", 12, 'bold')).grid(row=12, column=0, padx=10, pady=10, sticky="w")
    tk.Label(predict_tab, textvariable=advice_var, bg="#e0f7fa", font=("Arial", 12)).grid(row=12, column=1, padx=10, pady=10)

    # Báo cáo chi tiết
    report_display = tk.Text(report_tab, width=70, height=15, font=("Arial", 12), wrap=tk.WORD, bd=2, relief="solid")
    report_display.grid(row=1, column=0, padx=10, pady=10)
    report_display.config(state=tk.DISABLED)  # Không cho chỉnh sửa báo cáo

    # Chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    run_app()
