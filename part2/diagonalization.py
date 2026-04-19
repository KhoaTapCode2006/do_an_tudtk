import decomposition as decom
import numpy as np # Dùng để kiểm thử kết quả

class Diagonalization:
    @staticmethod
    def is_symmetric(A, tol=1e-9):
        """Kiểm tra ma trận đối xứng ."""
        n = len(A)
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j] - A[j][i]) > tol:
                    return False
        return True

    @staticmethod
    def diagonalize(A):
        """
        Chéo hóa ma trận A: A = P * D * P^-1
        """
        if not A or not A[0]:
            raise ValueError("Ma trận A không được rỗng.")
            
        m = len(A)
        n = len(A[0])
        
        if m != n:
            raise ValueError("Ma trận A phải là ma trận vuông để có thể chéo hóa.")
            
        if not Diagonalization.is_symmetric(A):
            raise ValueError("Thuật toán Jacobi hiện tại chỉ hỗ trợ chéo hóa ma trận đối xứng.")

        # Tìm trị riêng và vector riêng bằng thuật toán Jacobi từ file decomposition.py
        eigenvalues, P = decom.SVDDecomposition.jacobi_eigen(A)

        # Xây dựng ma trận đường chéo D
        D = [[0.0] * n for _ in range(n)]
        for i in range(n):
            D[i][i] = eigenvalues[i]

        # Tính P^-1
        P_inv = decom.SVDDecomposition.transpose(P)

        return P, D, P_inv

    @staticmethod
    def reconstruct(P, D, P_inv):
        """Hàm hỗ trợ kiểm tra kết quả chéo hoá"""
        PD = decom.SVDDecomposition.matmul(P, D)
        A_reconstructed = decom.SVDDecomposition.matmul(PD, P_inv)
        return A_reconstructed

# Kiểm thử hàm diagonalize(A)
if __name__ == "__main__":
    test_diagonalize = [
        {
            "name": "Ma trận 3x3",
            "A": [
                    [4.0, 1.0, -2.0],
                    [1.0, 2.0,  0.0],
                    [-2.0, 0.0, 3.0]
                ]
        },
        

        {
            "name": "Ma trận 2x2",
            "A": [
                [2.0, 1.0],
                [1.0, 2.0]
            ]
        },

        {
            "name": "Ma trận 3x3 (2)",
            "A": [
                [1.0, 2.0, 0.0],
                [2.0, 0.0,  2.0],
                [0.0, 2.0, -1.0]
            ]
        },

        {
            "name": "Ma trận đặc biệt",
            "A": [
                [1.0, 1.0], 
                [1.0, 1.0]
            ]
        },

        {
            "name": "Ma trận đơn vị",
            "A": [
                [1, 0], 
                [0, 1]
            ]
        }
    ]
    for test in test_diagonalize:
        print(f"\n=== Test: {test['name']} ===")
        A = test["A"]
        A_np = np.array(A)
        print("--- Ma trận A ban đầu ---")
        for row in A: 
            print([round(x, 4) for x in row])

        try:
            P, D, P_inv = Diagonalization.diagonalize(A)

            A_rec = Diagonalization.reconstruct(P, D, P_inv)


            print("\n--- Ma trận P (Chứa các vector riêng) ---")
            for row in P: 
                print([round(x, 4) for x in row])

            print("\n--- Ma trận đường chéo D (Chứa các trị riêng) ---")
            for row in D: 
                print([round(x, 4) for x in row])

            print("\n--- Ma trận P^-1 (Tương đương P^T do tính trực giao) ---")
            for row in P_inv: 
                print([round(x, 4) for x in row])

            print("\n--- Kiểm chứng: P * D * P^-1 ---")
            A_rec= Diagonalization.reconstruct(P, D, P_inv)
            A_rec_np = np.array(A_rec)

            for row in A_rec: 
                print([round(x, 4) for x in row])

            if np.allclose(A_np, A_rec_np, atol=1e-7):
                print(f"  => KẾT QUẢ: ĐÚNG")
            else:
                print(f"  => KẾT QUẢ: SAI")

        except Exception as e:
            print(f"Lỗi: {e}")