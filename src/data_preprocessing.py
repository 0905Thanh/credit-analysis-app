import os
import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Dữ liệu đã được tải thành công.")
        return df
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu: {e}")
        return None

def clean_data(df):
    if df is None:
        print("Dữ liệu rỗng, không thể làm sạch.")
        return None
    df_clean = df.dropna()
    try:
        df_clean['customer_id'] = df_clean['customer_id'].astype(int)
    except Exception as e:
        print(f"Lỗi chuyển đổi kiểu dữ liệu: {e}")
    return df_clean

def calculate_emi(loan_amount, interest_rate, repayment_period):
    """
    Tính số tiền trả góp hàng tháng (EMI).
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
    # DTI = (EMI / Thu nhập hàng tháng) * 100
    dti = (emi / total_income) * 100
    return dti

def calculate_loan_to_income(loan_amount, total_income):
    """
    Tính tỷ lệ vay trên thu nhập (Loan-to-Income).
    """
    loan_to_income = loan_amount / total_income
    return loan_to_income

def feature_engineering(df):
    """
    Tính toán các tính năng mới từ dữ liệu hiện có (EMI, DTI, Loan-to-Income).
    """
    # Tính thêm các chỉ số cần thiết (EMI, DTI, Loan-to-Income)
    df['total_income'] = df['main_salary'] + df['passive_salary']  # Tính tổng thu nhập

    # Tính EMI, DTI và Loan-to-Income cho từng khách hàng
    df['emi'] = df.apply(lambda row: calculate_emi(row['loan_amount'], row['bank_rate'], row['repayment_period']), axis=1)
    df['dti'] = df.apply(lambda row: calculate_dti(row['total_income'], row['emi']), axis=1)
    df['loan_to_income'] = df.apply(lambda row: calculate_loan_to_income(row['loan_amount'], row['total_income']), axis=1)

    return df

if __name__ == "__main__":
    print("Bắt đầu tiền xử lý dữ liệu...")

    # Đường dẫn đến file gốc
    raw_file = os.path.join("data", "raw", "customer_credit_data.xlsx")
    print(f"Đường dẫn file gốc: {raw_file}")
    
    # Tải dữ liệu
    data = load_data(raw_file)
    if data is None:
        print("Không thể tải dữ liệu, dừng xử lý.")
        exit(1)
    
    # Làm sạch dữ liệu
    data_clean = clean_data(data)
    if data_clean is None:
        print("Làm sạch dữ liệu thất bại, dừng xử lý.")
        exit(1)
    
    # Tính toán các tính năng mới
    data_clean = feature_engineering(data_clean)

    # Lưu dữ liệu đã xử lý vào thư mục processed
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_file = os.path.join(processed_dir, "customer_credit_data_clean.xlsx")
    
    # Lưu file Excel đã được tính toán các tính năng mới
    data_clean.to_excel(processed_file, index=False)
    
    print(f"Dữ liệu đã được lưu tại: {processed_file}")
    print("Kết thúc tiền xử lý.")
