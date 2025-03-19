import pandas as pd
import joblib

# Tải mô hình
model_path = 'models/credit_risk_model.joblib'
model = joblib.load(model_path)

def calculate_emi(loan_amount, interest_rate, repayment_period):
    """
    Tính số tiền trả góp hàng tháng (EMI) dựa trên công thức EMI.
    """
    r = interest_rate / 12 / 100  # Lãi suất hàng tháng
    n = repayment_period  # Số tháng
    
    # Công thức tính EMI
    emi = loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return emi

def calculate_dti(total_income, emi):
    """
    Tính tỷ lệ nợ trên thu nhập (DTI).
    """
    dti = (emi / total_income) * 100
    return dti

def calculate_loan_to_income(loan_amount, total_income):
    """
    Tính tỷ lệ vay trên thu nhập (Loan-to-Income).
    """
    loan_to_income = total_income / loan_amount
    return loan_to_income

def predict_credit_risk(input_data):
    """
    Dự đoán mức độ rủi ro tín dụng dựa trên các đặc trưng đã tính toán.
    """
    # Chuyển đổi dữ liệu đầu vào thành DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Dự đoán mức độ rủi ro
    prediction = model.predict(df_input)[0]

    # Mã hóa kết quả
    risk_mapping = {0: "Low", 1: "Medium", 2: "High"}
    risk_level = risk_mapping.get(prediction, "Unknown")

    return risk_level
