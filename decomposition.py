import math
import numpy as np # Dùng để kiểm thử kết quả

class SVDDecomposition:
    @staticmethod
    def transpose(A):
        """Tính ma trận chuyển vị"""
        return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

    @staticmethod
    def matmul(A, B):
        """Nhân hai ma trận"""
        m, n = len(A), len(A[0])
        p = len(B[0])
        C = [[0.0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    @staticmethod
    def vector_norm(v):
        """Tính chuẩn Euclidean (norm-2) của vector"""
        return math.sqrt(sum(x * x for x in v))

    @staticmethod
    def jacobi_eigen(S, tol=1e-9, max_iter=1000):
        """
        Thuật toán Jacobi tìm trị riêng và vector riêng cho ma trận đối xứng S.
        Trả về danh sách trị riêng (eigenvalues) và ma trận vector riêng (V).
        """
        n = len(S)
        # Khởi tạo V là ma trận đơn vị
        V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        S_copy = [row[:] for row in S]

        for _ in range(max_iter):
            # Tìm phần tử ngoài đường chéo có trị tuyệt đối lớn nhất
            max_val =  0.0
            p, q = 0, 1
            for i in range(n):
                for j in range(i + 1, n):
                    if abs(S_copy[i][j]) > max_val:
                        max_val = abs(S_copy[i][j])
                        p, q = i, j

            # Nếu phần tử lớn nhất đã đủ nhỏ
            if max_val < tol:
                break

            # Tính góc xoay theta
            tau = (S_copy[q][q] - S_copy[p][p]) / (2.0 * S_copy[p][q])
            t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
            c = 1.0 / math.sqrt(1.0 + t * t)
            s = t * c

            # Cập nhật V và S_copy
            for i in range(n):
                # V
                vip = V[i][p]
                viq = V[i][q]
                V[i][p] = c * vip - s * viq
                V[i][q] = s * vip + c * viq

                # Cập nhật các dòng trong S
                if i != p and i != q:
                    sip = S_copy[i][p]
                    siq = S_copy[i][q]
                    S_copy[i][p] = c * sip - s * siq
                    S_copy[p][i] = S_copy[i][p]
                    S_copy[i][q] = s * sip + c * siq
                    S_copy[q][i] = S_copy[i][q]

            # Cập nhật riêng các phần tử p, q
            spp = S_copy[p][p]
            sqq = S_copy[q][q]
            spq = S_copy[p][q]

            S_copy[p][p] = c * c * spp - 2 * s * c * spq + s * s * sqq
            S_copy[q][q] = s * s * spp + 2 * s * c * spq + c * c * sqq
            S_copy[p][q] = 0.0
            S_copy[q][p] = 0.0

        eigenvalues = [S_copy[i][i] for i in range(n)]
        return eigenvalues, V

    @staticmethod
    def svd(A):
        """
        Phân rã SVD: A = U * Sigma * V^T
        Trả về U, Sigma, V_T
        """
        if not A or not A[0]:
            raise ValueError("Ma trận A không được rỗng.")

        m = len(A)
        n = len(A[0])

        tol = 1e-9
        # Tính A_T * A 
        A_T = SVDDecomposition.transpose(A)
        ATA = SVDDecomposition.matmul(A_T, A)

        # Tìm trị riêng và vector riêng của ATA
        # eigenvalues: n phần tử, V: n x n
        eigenvalues, V = SVDDecomposition.jacobi_eigen(ATA)

        # Sắp xếp trị riêng và vector riêng theo thứ tự giảm dần của trị riêng
        eigen_pairs = []
        for i in range(len(eigenvalues)):
            # Lấy trị tuyệt đối để tránh lỗi số âm cực nhỏ 
            val = max(0, eigenvalues[i])
            # V là ma trận mà các cột là vector riêng
            col = [V[row][i] for row in range(len(V))]
            eigen_pairs.append((val, col))
        
        eigen_pairs.sort(key=lambda x: x[0], reverse=True)
        
        sorted_eigenvalues = [p[0] for p in eigen_pairs]
        sorted_V_cols = [p[1] for p in eigen_pairs]

        # Khởi tạo Sigma và gán giá trị suy biến
        Sigma = [[0.0] * n for _ in range(m)]
        singular_values = []
        for i in range(min(m, n)):
            val = math.sqrt(max(0.0, sorted_eigenvalues[i]))
            Sigma[i][i] = val
            singular_values.append(val)

        # Tính ma trận U (m x m)
        # Công thức: u_i = (1 / sigma_i) * A * v_i
        U_cols = []
        
        for i in range(min(m, n)):
            if singular_values[i] > tol:
                # v_i là cột thứ i của V 
                v_i = sorted_V_cols[i]
                # A * v_i 
                u_i = [sum(A[r][c] * v_i[c] for c in range(n)) for r in range(m)]
                # Chuẩn hóa u_i
                norm = SVDDecomposition.vector_norm(u_i)
                U_cols.append([x / norm for x in u_i])

        # Nếu U chưa đủ m cột, bổ sung bằng Gram-Schmidt
        basis_idx = 0
        while len(U_cols) < m:
            # Tạo vector cơ sở tiêu chuẩn e_i
            e = [0.0] * m
            e[basis_idx] = 1.0

            # Trực giao hóa với các cột đã có trong U
            temp_e = e[:]
            for u in U_cols:
                dot = sum(temp_e[k] * u[k] for k in range(m))
                for k in range(m):
                    temp_e[k] -= dot * u[k]

            norm = SVDDecomposition.vector_norm(temp_e)

            if norm > tol:
                # Chuẩn hóa 
                U_cols.append([x / norm for x in temp_e])
            basis_idx += 1

        # Ma trận U hoàn chỉnh
        U = SVDDecomposition.transpose(U_cols)
        V_T = sorted_V_cols
        return U, Sigma, V_T

# Kiểm thử hàm svd(A)
if __name__ == "__main__":

    test_decomposition = [
        {
            "name": "Ma trận 3x2",
            "A": [
                [1.0, 2.0],
                [3.0, 4.0],
                [5.0, 6.0]
            ],
        },
        

        {
            "name": "Ma trận 2x3",
            "A": [
                [3.0, 2.0, 2.0], 
                [2.0, 3.0, -2.0]
            ]
        },

        {
            "name": "Ma trận 2x2 suy biến",
            "A": [
                [1.0, 1.0],
                [2.0, 2.0]
            ]
        },

        {
            "name": "Ma trận 1x1",
            "A": [
                [5.0]
            ]
        },

        {
            "name": "Ma trận 4x3",
            "A": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 1.0]
            ]
        }
    ]
    i = 1
    for test in test_decomposition:
        
        print(f"\n=== Test {i}: {test['name']} ===")
        A = test["A"]
        A_np = np.array(A)
        print("--- Ma trận A ban đầu ---")
        for row in A: 
            print([round(x, 4) for x in row])
        try:
            U, Sigma, V_T = SVDDecomposition.svd(A)


            U_Sigma = SVDDecomposition.matmul(U, Sigma)
            A_rec = SVDDecomposition.matmul(U_Sigma, V_T)
            A_rec_np = np.array(A_rec)

            print("--- Ma trận U ---")
            for row in U: print([round(x, 4) for x in row])

            print("\n--- Ma trận Sigma ---")
            for row in Sigma: print([round(x, 4) for x in row])

            print("\n--- Ma trận V^T ---")
            for row in V_T: print([round(x, 4) for x in row]) 

            if np.allclose(A_np, A_rec_np, atol=1e-7):
                print(f"  => KẾT QUẢ: ĐÚNG (A ≈ U*Σ*V^T)")
            else:
                print(f"  => KẾT QUẢ: SAI")

        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")  
        i += 1
