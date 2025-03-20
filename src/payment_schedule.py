import matplotlib.pyplot as plt

def generate_payment_schedule(loan_amount, emi, repayment_period):
    """
    Hàm tạo biểu đồ lộ trình thanh toán.
    """
    months = list(range(1, repayment_period + 1))
    payments = [emi] * repayment_period
    remaining_balance = [loan_amount - (emi * i) for i in range(1, repayment_period + 1)]

    # Tạo đồ thị lộ trình thanh toán
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(months, remaining_balance, label="Số tiền còn lại", color='blue', marker='o')
    ax.set_xlabel("Số tháng")
    ax.set_ylabel("Số tiền còn lại")
    ax.set_title("Lộ Trình Thanh Toán Khoản Vay")
    
    # Thêm dòng chữ "Số tiền cần trả mỗi tháng"
    ax.text(0.5, 0.95, f"Số tiền cần trả mỗi tháng: {emi}", transform=ax.transAxes, fontsize=12, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.5'))
    
    ax.legend()

    return fig
