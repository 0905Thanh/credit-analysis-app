import os
import pandas as pd

# Tạo thư mục nếu chưa tồn tại
raw_data_dir = os.path.join("data", "raw")
os.makedirs(raw_data_dir, exist_ok=True)

# Dữ liệu mẫu với nhiều tính năng tài chính
data = {
    "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "age": [25, 40, 35, 50, 29, 45, 39, 55, 28, 60],
    "job": ["Engineer", "Doctor", "Teacher", "Artist", "Driver", "Nurse", "Manager", "Lawyer", "Chef", "Developer"],
    "main_salary": [50000, 80000, 60000, 90000, 55000, 65000, 70000, 95000, 70000, 120000],
    "passive_salary": [5000, 2000, 3000, 1000, 4000, 5000, 4500, 2000, 6000, 7000],
    "credit_score": [700, 650, 720, 600, 750, 680, 710, 640, 650, 720],
    "loan_amount": [10000, 20000, 15000, 25000, 30000, 22000, 18000, 20000, 35000, 50000],
    "debt_to_income": [0.2, 0.25, 0.15, 0.3, 0.18, 0.22, 0.2, 0.26, 0.35, 0.4],
    "repayment_period": [12, 24, 18, 36, 24, 30, 24, 36, 36, 48],
    "bank_rate": [7, 6.5, 7.5, 8, 6.2, 7.0, 6.8, 7.2, 6.5, 7.5]
}

# Chuyển dữ liệu sang DataFrame
df = pd.DataFrame(data)

# Tính toán các chỉ số mới
def calculate_emi(loan_amount, interest_rate, repayment_period):
    r = interest_rate / 12 / 100  # Lãi suất hàng tháng
    n = repayment_period  # Số tháng
    emi = loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return emi

def calculate_dti(total_income, emi):
    # DTI = (EMI / Thu nhập hàng tháng) * 100
    return (emi / total_income) * 100

def calculate_loan_to_income(loan_amount, total_income):
    return loan_amount / total_income

# Tính thêm EMI, DTI, Loan-to-Income cho từng khách hàng
df['total_income'] = df['main_salary'] + df['passive_salary']  # Tổng thu nhập
df['emi'] = df.apply(lambda row: calculate_emi(row['loan_amount'], row['bank_rate'], row['repayment_period']), axis=1)
df['dti'] = df.apply(lambda row: calculate_dti(row['total_income'], row['emi']), axis=1)
df['loan_to_income'] = df.apply(lambda row: calculate_loan_to_income(row['loan_amount'], row['total_income']), axis=1)

# Phân loại mức độ rủi ro dựa trên điểm tín dụng và các đặc trưng khác
def risk_level(row):
    if row['credit_score'] >= 700 and row['loan_to_income'] < 0.5 and row['dti'] < 30:
        return "Low"
    elif row['credit_score'] >= 650 and row['loan_to_income'] < 1.0 and row['dti'] < 50:
        return "Medium"
    else:
        return "High"

df['risk_level'] = df.apply(risk_level, axis=1)

# Lưu dữ liệu vào file Excel
file_path = os.path.join(raw_data_dir, "customer_credit_data.xlsx")
df.to_excel(file_path, index=False)

print(f"File mẫu được tạo tại: {file_path}")
