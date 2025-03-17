import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Tải mô hình
model_path = os.path.join("models", "credit_risk_model.joblib")
model = joblib.load(model_path)

# Các feature cần thiết
FEATURES = ["age", "income", "credit_score", "loan_amount", "debt_to_income"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Nếu gửi từ form HTML, lấy dữ liệu từ request.form
        try:
            input_data = {feature: float(request.form[feature]) for feature in FEATURES}
        except KeyError as e:
            return render_template('index.html', error=f"Thiếu feature: {str(e)}")
        except ValueError as e:
            return render_template('index.html', error="Vui lòng nhập đúng định dạng số cho các trường.")
        
        # Chuyển đổi dữ liệu thành DataFrame
        df = pd.DataFrame([input_data])
        
        # Dự đoán
        prediction = model.predict(df)[0]
        
        # Ánh xạ lại kết quả
        mapping = {0: "Low", 1: "Medium", 2: "High"}
        risk_level = mapping.get(prediction, "Unknown")
        
        return render_template('index.html', result=f"Predicted risk level: {risk_level}")
    
    # Nếu GET request, chỉ trả về giao diện nhập liệu
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
