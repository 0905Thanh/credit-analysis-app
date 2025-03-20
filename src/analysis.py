import pandas as pd
import joblib

# Tải mô hình
model_path = 'models/credit_risk_model.joblib'
model = joblib.load(model_path)

def calculate_emi(loan_amount, interest_rate, repayment_period):
    """
    Tính số tiền trả góp hàng tháng (EMI) và làm tròn về số nguyên.
    """
    r = interest_rate / 12 / 100  # Lãi suất hàng tháng
    n = repayment_period  # Số tháng
    emi = loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return round(emi)  # Làm tròn EMI về số nguyên

def calculate_dti(total_income, emi):
    """
    Tính tỷ lệ nợ trên thu nhập (DTI) và trả kết quả dưới dạng phần trăm.
    """
    dti = (emi / total_income) * 100  # Tỷ lệ nợ trên thu nhập dưới dạng phần trăm
    return round(dti, 2)  # Làm tròn DTI đến 2 chữ số thập phân

def calculate_loan_to_income(loan_amount, total_income):
    """
    Tính tỷ lệ vay trên thu nhập (Loan-to-Income).
    """
    loan_to_income = loan_amount / total_income
    return loan_to_income

def check_payment_feasibility(emi, total_income):
    """
    Kiểm tra xem số tiền trả hàng tháng có hợp lý không (DTI không vượt quá 40%).
    """
    dti = calculate_dti(total_income, emi)
    if dti > 40:
        return False  # Nếu DTI lớn hơn 40%, khách hàng sẽ gặp khó khăn trong việc trả nợ.
    return True

def predict_credit_risk(input_data):
    dti = input_data.get("dti", 0)
    
    if dti < 36:
        return "Low"
    elif 36 <= dti <= 50:
        return "Medium"
    else:
        return "High"
