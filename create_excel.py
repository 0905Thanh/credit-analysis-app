import os
import pandas as pd

# Tạo thư mục nếu chưa tồn tại
raw_data_dir = os.path.join("data", "raw")
os.makedirs(raw_data_dir, exist_ok=True)

# Dữ liệu mẫu
data = {
    "customer_id": [1, 2, 3, 4],
    "age": [25, 40, 35, 50],
    "income": [50000, 80000, 60000, 90000],
    "credit_score": [700, 650, 720, 600],
    "loan_amount": [10000, 20000, 15000, 25000]
}

df = pd.DataFrame(data)

# Lưu file Excel
file_path = os.path.join(raw_data_dir, "customer_credit_data.xlsx")
df.to_excel(file_path, index=False)
print(f"File mẫu được tạo tại: {file_path}")
