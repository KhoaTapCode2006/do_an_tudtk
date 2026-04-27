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
from part1 import matrix as mt
from solvers import Solvers

def generate_vector_b(n):
    """Sinh vector b ngẫu nhiên"""
    return [random.uniform(-10.0, 10.0) for _ in range(n)]

def generate_type1_sdd_matrix(n):
    """LOẠI 1: Ma trận chéo trội nghiêm ngặt (SDD cơ bản)"""
    A = []
    for i in range(n):
        row = [random.uniform(-10.0, 10.0) for _ in range(n)]
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        # Làm phần tử đường chéo chắc chắn lớn hơn tổng các phần tử còn lại
        row[i] = (off_diag_sum + random.uniform(2.0, 10.0)) * (1 if random.random() > 0.5 else -1)
        A.append(row)
    return A

def generate_type2_increasing_sdd(n):
    """LOẠI 2: Ma trận chéo trội """
    A = []
    for i in range(n):
        row = [random.uniform(-50.0, 50.0) for _ in range(n)] # Biên độ ngẫu nhiên lớn hơn
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        row[i] = (off_diag_sum + random.uniform(5.0, 15.0)) * (1 if random.random() > 0.5 else -1)
        A.append(row)
    return A

def generate_type3_non_sdd_matrix(n):
    """LOẠI 3: Ma trận không chéo trội """
    A = []
    for i in range(n):
        row = [random.uniform(-10.0, 10.0) for _ in range(n)]
        off_diag_sum = sum(abs(x) for x in row) - abs(row[i])
        
        # Làm phần tử đường chéo chắc chắn bé hơn nhiều so với tổng phần tử còn lại
        if off_diag_sum > 0:
            row[i] = random.uniform(0.0, off_diag_sum * 0.1) * (1 if random.random() > 0.5 else -1)
        else:
            row[i] = 0.0 
            
        A.append(row)
    return A

def calculate_error(A, x, b, n):
    """Tính sai số ||Ax - b||_2"""
    error_sq_sum = 0.0
    for i in range(n):
        ax_i = sum(A[i][j] * x[j] for j in range(n))
        error_sq_sum += (ax_i - b[i])**2
    return math.sqrt(error_sq_sum)

def run_benchmark():
    n_sizes = [50, 100, 200, 500, 1000]
      
    for n in n_sizes:
        print("\n\n")
        print(f"KÍCH THƯỚC MA TRẬN: {n} x {n}")
        print("\n")

        for test_idx in range(1, 6):
            print(f"\nTest Case {test_idx}")
            
            if test_idx <= 2:
                print("Phân loại : LOẠI 1 - Ma trận chéo trội nghiêm ngặt (SDD)")
                A = generate_type1_sdd_matrix(n)
            elif test_idx <= 4:
                print("Phân loại : LOẠI 2 - Ma trận chéo trội kích thước tăng dần")
                A = generate_type2_increasing_sdd(n)
            else:
                print("Phân loại : LOẠI 3 - Ma trận KHÔNG chéo trội (Test không hội tụ)")
                A = generate_type3_non_sdd_matrix(n)
                
            b = generate_vector_b(n)
            matrix_obj = mt.Matrix(A, b)
            solver = Solvers(matrix_obj)
            
            # 1. Đo Gauss Partial Pivoting
            try:
                start_time = time.perf_counter()
                _, x_gauss = solver.solve_gauss()
                gauss_time = time.perf_counter() - start_time
                gauss_error = calculate_error(A, x_gauss, b, n)
                print(f"1. Gauss (Partial Pivot) : Thời gian = {gauss_time:.6f}s | Sai số = {gauss_error:.4e} | Số bước = 1 (Trực tiếp)")
            except Exception as e:
                print(f"1. Gauss (Partial Pivot) : LỖI - {e}")

            # 2. Đo SVD
            try:
                start_time = time.perf_counter()
                _, x_svd = solver.solve_svd()
                svd_time = time.perf_counter() - start_time
                svd_error = calculate_error(A, x_svd, b, n)
                print(f"2. SVD                   : Thời gian = {svd_time:.6f}s | Sai số = {svd_error:.4e} | Số bước = 1 (Trực tiếp)")
            except Exception as e:
                print(f"2. SVD                   : LỖI - {e}")

            # 3. Đo Gauss-Seidel
            try:
                start_time = time.perf_counter()
                _, x_gs, k = solver.solve_gauss_seidel(tol=1e-6, max_iter=1000) 
                gs_time = time.perf_counter() - start_time
                gs_error = calculate_error(A, x_gs, b, n)
                print(f"3. Gauss-Seidel          : Thời gian = {gs_time:.6f}s | Sai số = {gs_error:.4e} | Số bước = {k}")
            except Exception as e:
                print(f"3. Gauss-Seidel          : LỖI (Không hội tụ) - {e}")

if __name__ == "__main__":
    run_benchmark()