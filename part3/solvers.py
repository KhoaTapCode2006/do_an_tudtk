import math
from part1 import matrix as mt
from part1 import gaussian_eliminate as ge
from part1 import back_substitution as bs
from part2 import decomposition as dcp

class Solvers:
    def __init__(self, matrix_obj):
        # Khởi tạo với một đối tượng Matrix.
        self.A = matrix_obj.A
        self.b = matrix_obj.b
        self.n = matrix_obj.n
        self.m = matrix_obj.m
        self.Zero = matrix_obj.Zero

    def solve_gauss(self):
        """Giải Ax = b bằng Gauss với Partial Pivoting"""
        # Đưa về dạng ma trận tam giác trên
        U, c, _ = ge.gaussian_eliminate(self.A, self.b)

        # Giải ma trận tam giác trên
        _, x = bs.back_substitution(U, c)

        return U, x

    def solve_svd(self):
        """Giải Ax = b bằng phân rã SVD"""
        U, Sigma, V_T = dcp.svd(self.A)
    
        # Biến b thành ma trận cột
        b_col = [[x] for x in self.b]

        # U, V là ma trận trực giao nên U_inv = U^T, V_inv = V^T
        # Sigma là ma trận đường chéo nên Sigma_inv là nghịch đảo các giá trị trên đường chéo 
        # Do đó Ax = U * Sigma * V^T * x = b <=> x = V * Sigma_inv * U^T * b_col

        # Tính Ut_b = U^T * b_col
        U_T = dcp.transpose(U)
        Ut_b_mat = dcp.matmul(U_T, b_col)
    
        # Nhân Ut_b với Sigma_inv
        # Lấy các giá trị trên đường chéo để tính s_inv
        s_inv_Ut_b = []
        for i in range(len(Ut_b_mat)):
            s = Sigma[i][i] if i < len(Sigma) else 0
            # Nếu có phần tử trên đường chéo bằng 0, chuyển về dạng giả nghịch đảo
            val = (1.0/s * Ut_b_mat[i][0]) if s > self.Zero else 0.0
            s_inv_Ut_b.append([val])
        
        # Bước 3: x = V * s_inv_Ut_b
        V = dcp.transpose(V_T)
        x_mat = dcp.matmul(V, s_inv_Ut_b)
    
        # Trả nghiệm về kết quả dạng vector
        x = [row[0] for row in x_mat]

        return U, x

    @staticmethod
    def check_diagonal_dominance(matrix):
        """Kiểm tra điều kiện chéo trội chặt của ma trận"""
        # Nếu ma trận không vuông, không thõa mãn
        if len(matrix) != len(matrix[0]):
            return False
        
        # Lấy số hàng của ma trận
        n = len(matrix)

        for i in range(n):
            # Lấy giá trị tuyệt đối của phần tử trên đường chéo chính
            diag = abs(matrix[i][i])
        
            # Tính tổng giá trị tuyệt đối của các phần tử còn lại trên hàng i
            off_sum = sum(abs(matrix[i][j]) for j in range(n) if i != j)
        
            # So sánh theo định nghĩa chéo trội chặt
            # Nếu phần tử đường chéo nhỏ hơn hoặc bằng tổng các phần tử còn lại, không thõa mãn
            if diag <= off_sum:
                return False
            
        return True
    
    def solve_gauss_seidel(self, tol=1e-6, max_iter=10000):
        """Giải Ax = b bằng phương pháp lặp Gauss–Seidel"""
        # Kiểm tra ma trận có vuông không trước khi thực hiện
        if self.n != self.m:
            raise ValueError(f"Gauss-Seidel chỉ áp dụng cho ma trận vuông.")
        
        # Khởi tạo x là vector 0
        x = [0.0] * self.n
    
        # Kiểm tra điều kiện chéo trội chặt
        if not self.check_diagonal_dominance(self.A):
            print("Ma trận không chéo trội — Gauss–Seidel có thể không hội tụ.")

        # Ma trận U là ma trận tam giác trên (không bao gồm đường chéo) chứa các phần tử của A
        U = []
        for i in range(self.n):
            row = [0.0] * self.n
            for j in range(i + 1, self.n):
                row[j] = self.A[i][j]
            U.append(row)

        for k in range(max_iter):
            # Tạo bản sao của x để so sánh hội tụ
            x_old = x[:] 

            for i in range(self.n):
                # Tính sum_new: các phần tử đã được cập nhật ở bước lặp hiện tại (j < i)
                sum_new = sum(self.A[i][j] * x[j] for j in range(i))
            
                # Tính sum_old: các phần tử từ bước lặp trước (j > i)
                sum_old = sum(self.A[i][j] * x_old[j] for j in range(i + 1, self.n))
            
                # Cập nhật x[i]
                # Nếu trên đường chéo có phần tử bằng 0, không thể thực hiện bằng phương pháp này
                if abs(self.A[i][i]) <= self.Zero:
                    raise ValueError(f"Phần tử đường chéo A[{i}][{i}] bằng 0.")
                x[i] = (self.b[i] - sum_new - sum_old) / self.A[i][i]

            # Kiểm tra điều kiện hội tụ bằng chuẩn Euclidean
            diff_sq_sum = sum((x[i] - x_old[i])**2 for i in range(self.n))
            # Nếu khoảng cách này nhỏ hơn sai số cho phép, có nghĩa là các giá trị của x đã ổn định, xác nhận giải thành công.
            if math.sqrt(diff_sq_sum) < tol:
                return U, x
            
        # Nghiệm chưa chắc đã chính xác, cần kiểm tra bằng phương pháp khác
        return U, x
    
if __name__ == "__main__":
    # Ma trận A chéo trội chặt để đảm bảo các phương pháp đều chạy tốt
    A = [
        [10.0, -1.0, 2.0],
        [-1.0, 11.0, -1.0],
        [2.0, -1.0, 10.0]
    ]
    b = [6.0, 25.0, -11.0]

    matrix_obj = mt.Matrix(A, b)
    
    # Khởi tạo lớp Solvers
    solver = Solvers(matrix_obj)

    # Kiểm tra Gauss với Partial Pivoting
    try:
        U_gauss, x_gauss = solver.solve_gauss()
        print("\nPhương pháp Gauss (Partial Pivoting):")
        print(f"   - Nghiệm x: {[round(val, 4) for val in x_gauss]}")
        print(f"   - Ma trận U (Tam giác trên):\n     {U_gauss[0]}\n     {U_gauss[1]}\n     {U_gauss[2]}")
    except Exception as e:
        print(f"\nLỗi khi chạy Gauss: {e}")

    # Kiểm tra SVD
    try:
        U_svd, x_svd = solver.solve_svd()
        print("\nPhương pháp SVD:")
        print(f"   - Nghiệm x: {[round(val, 4) for val in x_svd]}")
        print(f"   - Ma trận U (Orthogonal):\n     {[round(v, 4) for v in U_svd[0]]}...")
    except Exception as e:
        print(f"\nLỗi khi chạy SVD: {e}")

    # Kiểm tra Gauss-Seidel
    try:
        U_gs, x_gs = solver.solve_gauss_seidel(tol=1e-9)
        print("\nPhương pháp lặp Gauss-Seidel:")
        print(f"   - Nghiệm x: {[round(val, 4) for val in x_gs]}")
        print(f"   - Ma trận U (Phần tam giác trên của A):\n     {U_gs[0]}\n     {U_gs[1]}\n     {U_gs[2]}")
    except Exception as e:
        print(f"\nLỗi khi chạy Gauss-Seidel: {e}")