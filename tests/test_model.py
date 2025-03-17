import os
import unittest
import pandas as pd
from src import data_preprocessing, feature_engineering, model_training

class TestCreditModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tạo dữ liệu mẫu để test
        data = {
            "customer_id": [1, 2, 3, 4],
            "age": [25, 40, 35, 50],
            "income": [50000, 80000, 60000, 90000],
            "credit_score": [700, 650, 720, 600],
            "loan_amount": [10000, 20000, 15000, 25000]
        }
        cls.df_raw = pd.DataFrame(data)
        cls.df_clean = data_preprocessing.clean_data(cls.df_raw)
        cls.df_fe = feature_engineering.add_features(cls.df_clean)

    def test_data_cleaning(self):
        # Kiểm tra xem dữ liệu có bị mất dòng không
        self.assertFalse(self.df_clean.isnull().values.any(), "Dữ liệu chứa giá trị null sau khi làm sạch.")

    def test_feature_engineering(self):
        # Kiểm tra xem các feature mới đã được thêm chưa
        self.assertIn("debt_to_income", self.df_fe.columns)
        self.assertIn("risk_level", self.df_fe.columns)

    def test_model_training(self):
        X, y = model_training.prepare_data(self.df_fe)
        model, acc = model_training.train_model(X, y)
        self.assertGreaterEqual(acc, 0, "Độ chính xác phải là số dương.")
        self.assertIsNotNone(model, "Mô hình không được tạo ra.")

if __name__ == '__main__':
    unittest.main()
