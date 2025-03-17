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

if __name__ == "__main__":
    print("Bắt đầu tiền xử lý dữ liệu...")
    raw_file = os.path.join("data", "raw", "customer_credit_data.xlsx")
    print(f"Đường dẫn file gốc: {raw_file}")
    data = load_data(raw_file)
    if data is None:
        print("Không thể tải dữ liệu, dừng xử lý.")
        exit(1)
    
    data_clean = clean_data(data)
    if data_clean is None:
        print("Làm sạch dữ liệu thất bại, dừng xử lý.")
        exit(1)
    
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_file = os.path.join(processed_dir, "customer_credit_data_clean.xlsx")
    data_clean.to_excel(processed_file, index=False)
    print(f"Dữ liệu đã được lưu tại: {processed_file}")
    print("Kết thúc tiền xử lý.")
