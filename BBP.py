from decimal import Decimal, getcontext
import time
import matplotlib.pyplot as plt
import numpy as np

# 设置 matplotlib 中文字体支持（可选，具体字体因系统不同可能需要调整）
plt.rcParams['font.sans-serif'] = ['Arial']  # 如果中文乱码，更改为支持的字体
plt.rcParams['axes.unicode_minus'] = False

# 定义一个函数，使用 BBP 公式计算 π 的小数点位数
def calculate_pi_decimal_places(digits):
    """
    使用 Bailey–Borwein–Plouffe (BBP) 公式计算 π 的前 'digits' 位小数。
    
    参数:
        digits (int): 要计算的 π 的小数位数。
    
    返回:
        pi (str): 计算出的 π 值（字符串形式）。
        elapsed_time (float): 计算所用时间（秒）。
    """
    # 设置计算精度，增加余量以避免误差
    getcontext().prec = digits + 20

    # 估算所需的项数，经验公式（大约为 1.204 倍的 digits）
    num_terms = int(digits * 1.204) + 10  

    # 开始计时
    start_time = time.time()

    # 计算 π 使用 BBP 公式
    pi = sum(1 / Decimal(16)**k * 
             (Decimal(4) / (8*k + 1) - 
              Decimal(2) / (8*k + 4) - 
              Decimal(1) / (8*k + 5) - 
              Decimal(1) / (8*k + 6)) for k in range(num_terms))

    # 结束计时
    end_time = time.time()

    # 返回 π 值（保留 'digits' 位小数）和耗时
    return str(pi)[:digits + 2], end_time - start_time

# 定义需要计算的小数点位数列表（用于拟合）
decimal_places_fit = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# 定义需要计算的小数点位数用于验证
decimal_places_test = 12000

# 存储拟合数据的计算耗时
times_fit = []

# 逐步计算每个小数点位数的 π（用于拟合曲线）
for digits in decimal_places_fit:
    print(f"Calculating π to {digits} decimal places...")
    pi, elapsed_time = calculate_pi_decimal_places(digits)
    times_fit.append(elapsed_time)
    print(f"Time taken for {digits} decimal places: {elapsed_time:.2f} seconds")
    if digits == 1000:  # 打印 π 的前 1000 位，供参考
        print(f"\nπ to 1000 decimal places:\n{pi}\n")

# 使用拟合曲线预测 12000 位的时间
print(f"\nCalculating π to {decimal_places_test} decimal places for validation...")
pi_12000, time_test_actual = calculate_pi_decimal_places(decimal_places_test)
print(f"Actual time taken for {decimal_places_test} decimal places: {time_test_actual:.2f} seconds")

# 拟合曲线，假设复杂度为 O(n^2)
coefficients = np.polyfit(decimal_places_fit, times_fit, 2)  # 二次多项式拟合
poly_func = np.poly1d(coefficients)

# 使用拟合曲线预测 12000 位的耗时
time_test_predicted = poly_func(decimal_places_test)

# 绘制时间变化趋势图
plt.figure(figsize=(10, 6))
plt.plot(decimal_places_fit, times_fit, marker='o', linestyle='-', color='b', label='Actual Time (Fit Data)')
plt.plot(decimal_places_test, time_test_actual, 'go', label=f'Actual Time (12000): {time_test_actual:.2f}s')
plt.plot(decimal_places_test, time_test_predicted, 'ro', label=f'Predicted Time (12000): {time_test_predicted:.2f}s')

# 绘制拟合曲线
decimal_places_all = decimal_places_fit + [decimal_places_test]
fitted_times = [poly_func(n) for n in decimal_places_all]
plt.plot(decimal_places_all, fitted_times, linestyle='--', color='r', label=f'Fitted Curve: {coefficients[0]:.2e}x² + {coefficients[1]:.2e}x + {coefficients[2]:.2e}')

# 图形细节
plt.title('Time Taken to Compute π vs Decimal Places', fontsize=14)
plt.xlabel('Decimal Places', fontsize=12)
plt.ylabel('Time Taken (seconds)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)

# 显示图形
plt.tight_layout()
plt.show()

# 打印拟合曲线的系数（用于验证复杂度）
print(f"Fitted quadratic curve: {coefficients[0]:.2e}x^2 + {coefficients[1]:.2e}x + {coefficients[2]:.2e}")

# 验证时间复杂度是否接近 O(n^2)
print("\nComplexity Analysis:")
print(f"The leading coefficient of x^2 is approximately {coefficients[0]:.2e}.")
print(f"Predicted time for {decimal_places_test} decimal places: {time_test_predicted:.2f} seconds")
print(f"Actual time for {decimal_places_test} decimal places: {time_test_actual:.2f} seconds")
print(f"Prediction error: {abs(time_test_predicted - time_test_actual):.2f} seconds ({abs(time_test_predicted - time_test_actual) / time_test_actual * 100:.2f}%)")
if abs(time_test_predicted - time_test_actual) / time_test_actual < 0.1:  # 误差小于 10% 认为拟合良好
    print("The prediction matches the actual time well, verifying the O(n^2) complexity.")
else:
    print("The prediction deviates significantly, further investigation is needed.")

# 可选：打印前 1000 位 π（在 12000 位计算完成后）
print(f"\nπ to 1000 decimal places from 12000-digit computation:\n{pi_12000[:1002]}\n")