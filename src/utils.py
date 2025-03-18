# src/utils.py
def validate_numeric(value):
    """
    Kiểm tra giá trị có thể chuyển thành float không.
    Trả về giá trị float nếu hợp lệ, hoặc raise ValueError nếu không.
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Giá trị '{value}' không phải là số hợp lệ.")
