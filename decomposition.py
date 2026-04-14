import math

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
            max_val = 0.0
            p, q = 0, 0
            for i in range(n):
                for j in range(i + 1, n):
                    if abs(S_copy[i][j]) > max_val:
                        max_val = abs(S_copy[i][j])
                        p, q = i, j

            # Nếu phần tử lớn nhất đã đủ nhỏ -> hội tụ
            if max_val < tol:
                break

            # Tính góc xoay theta
            if abs(S_copy[p][p] - S_copy[q][q]) < 1e-12:
                theta = math.pi / 4.0
            else:
                theta = 0.5 * math.atan2(2.0 * S_copy[p][q], S_copy[p][p] - S_copy[q][q])

            c = math.cos(theta)
            s = math.sin(theta)

            # Cập nhật V và S_copy
            for i in range(n):
                # V
                vip = V[i][p]
                viq = V[i][q]
                V[i][p] = c * vip - s * viq
                V[i][q] = s * vip + c * viq

                # S (chỉ cập nhật các dòng/cột không phải p, q ở bước này)
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

        # 1. Tính A^T * A
        A_T = SVDDecomposition.transpose(A)
        S = SVDDecomposition.matmul(A_T, A)  # Kích thước n x n

        # 2. Tìm trị riêng và vector riêng của A^T * A
        eigenvalues, V_mat = SVDDecomposition.jacobi_eigen(S)

        # 3. Ghép cặp trị riêng - vector riêng và sắp xếp giảm dần
        eig_pairs = []
        for i in range(n):
            vec = [V_mat[j][i] for j in range(n)]
            eig_pairs.append((eigenvalues[i], vec))
        
        eig_pairs.sort(key=lambda x: x[0], reverse=True)

        singular_values = []
        V_T = []  # Ma trận V^T
        
        for val, vec in eig_pairs:
            # Ngăn lỗi số âm cực nhỏ do sai số dấu phẩy động
            sigma = math.sqrt(max(0.0, val))
            singular_values.append(sigma)
            V_T.append(vec)

        V_final = SVDDecomposition.transpose(V_T)  # Kích thước n x n (Đây là ma trận V)

        # 4. Khởi tạo ma trận đường chéo Sigma (kích thước m x n)
        Sigma = [[0.0] * n for _ in range(m)]
        for i in range(min(m, n)):
            Sigma[i][i] = singular_values[i]

        # 5. Tính toán ma trận U (kích thước m x m)
        U_cols = []
        tol = 1e-9

        # Tính u_i = (A * v_i) / sigma_i
        for i in range(n):
            if singular_values[i] > tol:
                v_i = [[V_final[j][i]] for j in range(n)]  # Chuyển thành vector cột
                Av_i = SVDDecomposition.matmul(A, v_i)
                u_i = [Av_i[j][0] / singular_values[i] for j in range(m)]
                U_cols.append(u_i)

        # Nếu U chưa đủ m cột (ma trận không vuông hoặc suy biến), bổ sung bằng Gram-Schmidt
        basis_idx = 0
        while len(U_cols) < m:
            # Tạo vector cơ sở tiêu chuẩn e_i
            e = [0.0] * m
            e[basis_idx] = 1.0
            basis_idx += 1

            # Trực giao hóa (Orthogonalize) với các cột đã có trong U
            for u in U_cols:
                dot = sum(e[k] * u[k] for k in range(m))
                for k in range(m):
                    e[k] -= dot * u[k]

            norm = SVDDecomposition.vector_norm(e)
            if norm > tol:
                # Chuẩn hóa (Normalize)
                e_norm = [e[k] / norm for k in range(m)]
                U_cols.append(e_norm)

        # Ma trận U hoàn chỉnh
        U = SVDDecomposition.transpose(U_cols)

        return U, Sigma, V_T

# ==========================================
# CÁCH CHẠY THỬ (TEST CASE)
# ==========================================
if __name__ == "__main__":
    # Test với một ma trận bất kỳ
    A = [
        [3, 2, 2],
        [2, 3, -2]
    ]

    try:
        U, Sigma, V_T = SVDDecomposition.svd(A)

        print("--- Ma trận U ---")
        for row in U: print([round(x, 4) for x in row])

        print("\n--- Ma trận Sigma ---")
        for row in Sigma: print([round(x, 4) for x in row])

        print("\n--- Ma trận V^T ---")
        for row in V_T: print([round(x, 4) for x in row])

    except Exception as e:
        print(f"Lỗi: {e}")