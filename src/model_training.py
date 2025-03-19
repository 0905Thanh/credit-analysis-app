import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def load_feature_data(file_path):
    """
    Tải dữ liệu có chứa đặc trưng.
    """
    return pd.read_excel(file_path)

def prepare_data(df):
    """
    Chuẩn bị dữ liệu cho việc huấn luyện mô hình.
    Giả sử rằng ta dự báo biến 'risk_level' (encode thành số).
    """
    # Encode risk_level
    mapping = {"Low": 0, "Medium": 1, "High": 2}
    df["risk_level_encoded"] = df["risk_level"].map(mapping)

    # Chọn các feature, ví dụ: age, total_income, credit_score, loan_amount, debt_to_income, emi, dti, loan_to_income
    features = [
        "age", "total_income", "credit_score", "loan_amount", 
        "debt_to_income", "emi", "dti", "loan_to_income"
    ]
    
    X = df[features]
    y = df["risk_level_encoded"]

    return X, y

def train_model(X, y):
    """
    Huấn luyện mô hình RandomForest.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Dự đoán trên tập test
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Độ chính xác trên tập test: {acc:.2f}")

    return clf, acc

def save_model(model, model_path):
    """
    Lưu mô hình đã huấn luyện.
    """
    joblib.dump(model, model_path)
    print(f"Mô hình đã được lưu tại: {model_path}")

if __name__ == "__main__":
    # Tải dữ liệu có đặc trưng từ file Excel đã được tính toán các đặc trưng mới
    feature_file = os.path.join("data", "processed", "customer_credit_data_features.xlsx")
    df = load_feature_data(feature_file)
    
    # Chuẩn bị dữ liệu cho mô hình
    X, y = prepare_data(df)
    
    # Huấn luyện mô hình và tính độ chính xác
    model, accuracy = train_model(X, y)
    
    # Lưu mô hình
    model_dir = os.path.join("models")
    os.makedirs(model_dir, exist_ok=True)
    save_model(model, os.path.join(model_dir, "credit_risk_model.joblib"))
