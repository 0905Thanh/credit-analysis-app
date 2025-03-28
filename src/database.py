import sqlite3

# Tạo hoặc kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('credit_risk.db')
cursor = conn.cursor()

# Tạo bảng nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS prediction_history (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    occupation TEXT,
                    income REAL,
                    loan_amount REAL,
                    credit_score INTEGER,
                    risk_level TEXT)''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Database and table created successfully!")

def save_prediction(name, age, occupation, income, loan_amount, credit_score, risk_level):
    conn = sqlite3.connect('credit_risk.db')
    cursor = conn.cursor()
    
    # Lưu dữ liệu vào bảng
    cursor.execute('''INSERT INTO prediction_history (name, age, occupation, income, loan_amount, credit_score, risk_level)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (name, age, occupation, income, loan_amount, credit_score, risk_level))
    
    conn.commit()
    conn.close()
    print("Prediction saved successfully!")

def display_history():
    conn = sqlite3.connect('credit_risk.db')
    cursor = conn.cursor()
    
    # Truy vấn dữ liệu từ bảng
    cursor.execute('SELECT * FROM prediction_history')
    predictions = cursor.fetchall()
    
    for prediction in predictions:
        print(f"ID: {prediction[0]}")
        print(f"Tên khách hàng: {prediction[1]}")
        print(f"Tuổi: {prediction[2]}")
        print(f"Nghề nghiệp: {prediction[3]}")
        print(f"Thu nhập: {prediction[4]}")
        print(f"Số tiền vay: {prediction[5]}")
        print(f"Điểm tín dụng: {prediction[6]}")
        print(f"Mức độ rủi ro: {prediction[7]}")
        print("------------------------")
    
    conn.close()

