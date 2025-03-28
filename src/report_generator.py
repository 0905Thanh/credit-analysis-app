# report_generator.py
import pandas as pd
def generate_report(input_data, emi, dti, loan_to_income, risk_level, advice):
    """
    Hàm tạo báo cáo chi tiết dựa trên dữ liệu đầu vào và kết quả tính toán.
    """
    report_text = f"--- Báo Cáo Chi Tiết ---\n\n"
    report_text += f"Thông tin khách hàng:\n"
    report_text += f"Tên: {input_data['name']}\n"
    report_text += f"Tuổi: {input_data['age']}\n"
    report_text += f"Nghề nghiệp: {input_data['occupation']}\n"
    report_text += f"Lương chính: {input_data['main_salary']}\n"
    report_text += f"Lương thụ động: {input_data['passive_salary']}\n"
    report_text += f"Điểm tín dụng: {input_data['credit_score']}\n"
    report_text += f"Số tiền vay: {input_data['loan_amount']}\n"
    report_text += f"Lãi suất ngân hàng: {input_data['bank_rate']}\n"
    report_text += f"Thời gian chi trả: {input_data['repayment_period']}\n"
    report_text += f"Tỷ lệ nợ trên thu nhập (DTI): {dti}\n\n"
    
    # Các chỉ số tài chính tính toán được
    report_text += f"Chỉ số tài chính:\n"
    report_text += f"Tổng thu nhập: {input_data['total_income']}\n"
    report_text += f"EMI: {emi}\n"
    report_text += f"DTI: {dti}\n"
    report_text += f"Loan-to-Income: {loan_to_income}\n"
    
    # Mức độ rủi ro dự đoán
    report_text += f"Mức độ rủi ro dự đoán: {risk_level}\n"
    report_text += f"Lời khuyên: {advice}"
    
    return report_text
