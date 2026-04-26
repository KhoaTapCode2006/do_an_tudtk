import sys
import os
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'part1'))
sys.path.append(os.path.join(root_dir, 'part2'))
sys.path.append(os.path.join(root_dir, 'part3'))

import random
import math
import time
import pandas as pd
import matplotlib.pyplot as plt
from part1 import matrix as mt
from solvers import Solvers

class DualLogger:
    def __init__(self, filename="ket_qua_console.txt"):
        self.terminal = sys.stdout
        # Mở file ở chế độ 'w' để ghi đè file mới 
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message) # Đẩy lên màn hình
        self.log.write(message)      # Đẩy vào file txt

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = DualLogger("ket_qua_console.txt")

def generate_vector_b(n):
    """Sinh vector b ngẫu nhiên"""
    return [random.uniform(-10.0, 10.0) for _ in range(n)]

def generate_type1_sdd_matrix(n):
    """LOẠI 1: Ma trận chéo trội nghiêm ngặt (SDD cơ bản)"""
    A = []
    for i in range(n):
        row = [random.uniform(-10.0, 10.0) for _ in range(n)]
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        # Ép đường chéo CHẮC CHẮN LỚN HƠN tổng các phần tử còn lại
        row[i] = (off_diag_sum + random.uniform(2.0, 10.0)) * (1 if random.random() > 0.5 else -1)
        A.append(row)
    return A

def generate_type2_increasing_sdd(n):
    """LOẠI 2: Ma trận chéo trội (Dành cho test kích thước tăng dần)"""
    A = []
    for i in range(n):
        row = [random.uniform(-50.0, 50.0) for _ in range(n)] # Biên độ ngẫu nhiên lớn hơn
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        row[i] = (off_diag_sum + random.uniform(5.0, 15.0)) * (1 if random.random() > 0.5 else -1)
        A.append(row)
    return A

def generate_type3_non_sdd_matrix(n):
    """LOẠI 3: Ma trận cố tình KHÔNG chéo trội (Đảm bảo Gauss-Seidel thất bại)"""
    A = []
    for i in range(n):
        row = [random.uniform(-10.0, 10.0) for _ in range(n)]
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        
        # CÚ LỪA: Ép phần tử đường chéo phải BÉ HƠN RẤT NHIỀU so với tổng phần tử còn lại
        if off_diag_sum > 0:
            row[i] = random.uniform(0.0, off_diag_sum * 0.1) * (1 if random.random() > 0.5 else -1)
        else:
            row[i] = 0.0 
            
        A.append(row)
    return A

def calculate_error(A, x, b, n):
    """Tính sai số tương đối ||Ax - b||_2 / ||b||_2 """
    error_sq_sum = 0.0
    b_sq_sum = 0.0
    
    for i in range(n):
        # Tính phần tử thứ i của vector (Ax)
        ax_i = sum(A[i][j] * x[j] for j in range(n))
        
        # Tử số: Bình phương sai số (Ax - b)^2
        error_sq_sum += (ax_i - b[i])**2
        
        # Mẫu số: Bình phương phần tử b
        b_sq_sum += b[i]**2
        
    norm_error = math.sqrt(error_sq_sum) 
    norm_b = math.sqrt(b_sq_sum)        
    
    if norm_b == 0:
        return norm_error # Tránh lỗi chia cho 0 nếu vector b toàn số 0
        
    return norm_error / norm_b # Trả về sai số tương đối


def draw_charts(df):
    """Phần 4: Vẽ biểu đồ từ dữ liệu DataFrame thu thập được"""
    print("\n--- ĐANG TIẾN HÀNH VẼ BIỂU ĐỒ ---")
    
    # Lọc dữ liệu: Chỉ lấy những test case chạy thành công (không bị NaN)
    df_success = df.dropna(subset=['Time_Gauss', 'Time_Seidel'])
    
    # Lấy trung bình thời gian theo từng kích thước n
    avg_times = df_success.groupby('n')[['Time_Gauss', 'Time_Seidel']].mean().reset_index()

    plt.figure(figsize=(18, 5))

    # Biểu đồ 1: Thời gian chạy
    plt.subplot(1, 3, 1)
    plt.plot(avg_times['n'], avg_times['Time_Gauss'], marker='o', label='Gauss Partial Pivoting')
    plt.plot(avg_times['n'], avg_times['Time_Seidel'], marker='s', label='Gauss-Seidel')
    plt.title("Thời gian chạy trung bình theo kích thước $n$")
    plt.xlabel("Kích thước ma trận (n)")
    plt.ylabel("Thời gian (giây)")
    plt.legend()
    plt.grid(True)

    # Biểu đồ 2: Phân bố số bước lặp và sai số (Cho ma trận loại 1 & 2)
    plt.subplot(1, 3, 2)
    df_gs_success = df[(df['Iter_Seidel'] > 0) & (df['Matrix_Type'] != 'Loại 3')]
    plt.scatter(df_gs_success['Iter_Seidel'], df_gs_success['Error_Seidel'], color='red')
    plt.yscale('log')
    plt.title("Độ hội tụ của Gauss-Seidel (Tổng quan các Test)")
    plt.xlabel("Số bước lặp đạt được")
    plt.ylabel("Sai số cuối cùng $||Ax - b||$")
    plt.grid(True, which="both", ls="--")

    # Biểu đồ 3: Log-log Thời gian vs n và O(n^3)
    plt.subplot(1, 3, 3)
    plt.loglog(avg_times['n'], avg_times['Time_Gauss'], marker='o', label='Thực tế (Gauss)')
    
    # Vẽ đường lý thuyết O(n^3)
    if not avg_times.empty:
        n0 = avg_times['n'].iloc[0]
        t0 = avg_times['Time_Gauss'].iloc[0]
        # Nếu t0 = 0 do quá nhanh, set một giá trị epsilon nhỏ
        if t0 == 0: t0 = 1e-6 
        theoretical_time = [t0 * (n / n0)**3 for n in avg_times['n']]
        plt.loglog(avg_times['n'], theoretical_time, linestyle='--', color='gray', label='Lý thuyết $O(n^3)$')
        
    plt.title("Đồ thị Log-Log: Thời gian vs $n$")
    plt.xlabel("Kích thước ma trận (n)")
    plt.ylabel("Thời gian (giây)")
    plt.legend()
    plt.grid(True, which="both", ls="--")

    plt.tight_layout()
    plt.show()
    print("--- HOÀN TẤT VẼ BIỂU ĐỒ ---")


def run_benchmark():
    n_sizes = [50, 100, 200, 500, 1000]
    
    results_data = []
    for n in n_sizes:
        print("\n\n")
        print(f"KÍCH THƯỚC MA TRẬN: {n} x {n}")
        print("\n")
        
        for test_idx in range(1, 6):
            print(f"\nTest Case {test_idx}")
            
            # 1. TẠO MỘT TỪ ĐIỂN ĐỂ LƯU DỮ LIỆU CỦA TEST CASE NÀY
            row_data = {
                'n': n,
                'Test_Case': test_idx,
                'Matrix_Type': '',
                'Time_Gauss': None, 'Error_Gauss': None,
                'Time_SVD': None, 'Error_SVD': None,
                'Time_Seidel': None, 'Error_Seidel': None, 'Iter_Seidel': 0
            }
            
            if test_idx <= 2:
                print("Phân loại : LOẠI 1 - Ma trận chéo trội nghiêm ngặt (SDD)")
                A = generate_type1_sdd_matrix(n)
                row_data['Matrix_Type'] = 'Loại 1'
            elif test_idx <= 4:
                print("Phân loại : LOẠI 2 - Ma trận chéo trội kích thước tăng dần")
                A = generate_type2_increasing_sdd(n)
                row_data['Matrix_Type'] = 'Loại 2'
            else:
                print("Phân loại : LOẠI 3 - Ma trận KHÔNG chéo trội (Test không hội tụ)")
                A = generate_type3_non_sdd_matrix(n)
                row_data['Matrix_Type'] = 'Loại 3'
                
            b = generate_vector_b(n)
            matrix_obj = mt.Matrix(A, b)
            solver = Solvers(matrix_obj)
            
            # 1. Đo Gauss Partial Pivoting
            try:
                start_time = time.perf_counter()
                _, x_gauss = solver.solve_gauss()
                gauss_time = time.perf_counter() - start_time
                gauss_error = calculate_error(A, x_gauss, b, n)
                
                # Lưu vào row_data
                row_data['Time_Gauss'] = gauss_time
                row_data['Error_Gauss'] = gauss_error
                
                print(f"1. Gauss (Partial Pivot) : Thời gian = {gauss_time:.6f}s | Sai số = {gauss_error:.4e} | Số bước = 1 (Trực tiếp)")
            except Exception as e:
                print(f"1. Gauss (Partial Pivot) : LỖI - {e}")

            # 2. Đo SVD
            try:
                start_time = time.perf_counter()
                _, x_svd = solver.solve_svd()
                svd_time = time.perf_counter() - start_time
                svd_error = calculate_error(A, x_svd, b, n)
                
                # Lưu vào row_data
                row_data['Time_SVD'] = svd_time
                row_data['Error_SVD'] = svd_error
                
                print(f"2. SVD                   : Thời gian = {svd_time:.6f}s | Sai số = {svd_error:.4e} | Số bước = 1 (Trực tiếp)")
            except Exception as e:
                print(f"2. SVD                   : LỖI - {e}")

            # 3. Đo Gauss-Seidel
            try:
                start_time = time.perf_counter()
                _, x_gs, k = solver.solve_gauss_seidel(tol=1e-6, max_iter=1000) 
                gs_time = time.perf_counter() - start_time
                gs_error = calculate_error(A, x_gs, b, n)
                
                # Lưu vào row_data
                row_data['Time_Seidel'] = gs_time
                row_data['Error_Seidel'] = gs_error
                row_data['Iter_Seidel'] = k
                
                print(f"3. Gauss-Seidel          : Thời gian = {gs_time:.6f}s | Sai số = {gs_error:.4e} | Số bước = {k}")
            except Exception as e:
                print(f"3. Gauss-Seidel          : LỖI (Không hội tụ) - {e}")

            results_data.append(row_data)

    # SAU KHI CHẠY XONG TẤT CẢ: Lưu ra file Excel
    df = pd.DataFrame(results_data)
    excel_filename = "ket_qua_kiem_thu.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Đã lưu thành công dữ liệu vào file: {excel_filename}")

    # Gọi hàm vẽ biểu đồ
    draw_charts(df)

if __name__ == "__main__":
    run_benchmark()