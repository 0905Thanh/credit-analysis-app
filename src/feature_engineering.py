# src/feature_engineering.py
import os
import pandas as pd

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
    loan_to_income = loan_amount / total_income
    return loan_to_income

def add_features(df):
    """
    Thêm các đặc trưng mới cho dữ liệu:
    1. Debt-to-Income Ratio (loan_amount / income)
    2. Risk Level (dựa trên credit_score)
    3. EMI (số tiền trả hàng tháng)
    4. Tỷ lệ nợ trên thu nhập (DTI)
    5. Tỷ lệ vay trên thu nhập (Loan-to-Income)
    """
    if df is None or df.empty:
        return df

    # Tính thêm tổng thu nhập từ lương chính và lương thụ động
    df["total_income"] = df["main_salary"] + df["passive_salary"]

    # Tạo feature: Debt-to-Income Ratio (loan_amount / income)
    df["debt_to_income"] = df["loan_amount"] / df["total_income"]

    # Tạo feature: Risk Level (dựa trên credit_score)
    def risk_level(score):
        if score >= 700:
            return "Low"
        elif score >= 650:
            return "Medium"
        else:
            return "High"

    df["risk_level"] = df["credit_score"].apply(risk_level)

    # Tính thêm các tính năng mới: EMI, DTI, Loan-to-Income
    df["emi"] = df.apply(lambda row: calculate_emi(row['loan_amount'], row['bank_rate'], row['repayment_period']), axis=1)
    df["dti"] = df.apply(lambda row: calculate_dti(row['total_income'], row['emi']), axis=1)
    df["loan_to_income"] = df.apply(lambda row: calculate_loan_to_income(row['loan_amount'], row['total_income']), axis=1)

    return df

if __name__ == "__main__":
    # Ví dụ kiểm tra
    df = pd.read_excel("data/processed/customer_credit_data_clean.xlsx")
    
    # Thêm các đặc trưng vào DataFrame
    df_fe = add_features(df)
    
    # Lưu file đã được thêm đặc trưng vào thư mục processed
    output_file = os.path.join("data", "processed", "customer_credit_data_features.xlsx")
    df_fe.to_excel(output_file, index=False)
    print(f"Đặc trưng đã được thêm và lưu vào file: {output_file}")
