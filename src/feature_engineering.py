import pandas as pd

def add_features(df):
    """
    Thêm các đặc trưng mới cho dữ liệu.
    Ví dụ: tỉ lệ nợ so với thu nhập, phân loại rủi ro dựa trên credit_score.
    """
    if df is None or df.empty:
        return df

    # Tạo feature: Debt-to-Income Ratio (loan_amount / income)
    df["debt_to_income"] = df["loan_amount"] / df["income"]

    # Tạo feature: Risk Level (dựa trên credit_score)
    def risk_level(score):
        if score >= 700:
            return "Low"
        elif score >= 650:
            return "Medium"
        else:
            return "High"

    df["risk_level"] = df["credit_score"].apply(risk_level)
    
    return df

if __name__ == "__main__":
    # Ví dụ kiểm tra
    df = pd.read_excel("data/processed/customer_credit_data_clean.xlsx")
    df_fe = add_features(df)
    df_fe.to_excel("data/processed/customer_credit_data_features.xlsx", index=False)
    print("Đặc trưng đã được thêm và lưu file features.")
