# src/analysis.py
import pandas as pd
import joblib

def load_model(model_path):
    """
    Tải mô hình tín dụng từ file joblib.
    """
    return joblib.load(model_path)

def process_input_data(input_data):
    """
    Chuyển đổi dữ liệu nhập từ giao diện thành DataFrame và xử lý các kiểu dữ liệu.
    Các trường số sẽ được chuyển thành số float.
    """
    numeric_fields = ["age", "main_salary", "passive_salary", "total_income", 
                      "credit_score", "loan_amount", "debt_to_income", "repayment_period"]
    processed_data = {}
    for key, value in input_data.items():
        if key in numeric_fields:
            try:
                processed_data[key] = float(value)
            except ValueError:
                processed_data[key] = 0.0
        else:
            processed_data[key] = value
    return pd.DataFrame([processed_data])

def predict_credit_risk(model, df):
    """
    Dự đoán mức rủi ro tín dụng bằng cách sử dụng mô hình đã tải.
    """
    # Giả sử mô hình đã được huấn luyện với các đặc trưng phù hợp.
    prediction = model.predict(df)[0]
    return prediction
