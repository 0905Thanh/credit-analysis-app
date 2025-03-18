# tests/test_analysis.py
import unittest
import pandas as pd
from src.analysis import process_input_data, predict_credit_risk

class TestAnalysis(unittest.TestCase):
    def test_process_input_data(self):
        input_data = {
            "age": "30",
            "job": "Engineer",
            "main_salary": "5000",
            "passive_salary": "1000",
            "total_income": "6000",
            "credit_score": "750",
            "loan_amount": "2000",
            "debt_to_income": "0.3",
            "repayment_period": "12",
            "bank_rate": "7"
        }
        df = process_input_data(input_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.loc[0, "age"], 30.0)
    
    def test_predict_credit_risk(self):
        # Tạo mô hình giả lập: luôn trả về 0
        class DummyModel:
            def predict(self, df):
                return [0]
        dummy_model = DummyModel()
        input_data = {
            "age": "30",
            "job": "Engineer",
            "main_salary": "5000",
            "passive_salary": "1000",
            "total_income": "6000",
            "credit_score": "750",
            "loan_amount": "2000",
            "debt_to_income": "0.3",
            "repayment_period": "12",
            "bank_rate": "7"
        }
        df = process_input_data(input_data)
        prediction = predict_credit_risk(dummy_model, df)
        self.assertEqual(prediction, 0)

if __name__ == "__main__":
    unittest.main()
