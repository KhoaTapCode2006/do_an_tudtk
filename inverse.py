import matrix as mt
import gaussian_eliminate as ge
import back_substitution as bs

def inverse(self, A): 
    """ Tính ma trận nghịch đảo qua khử Gauss và thế ngược """
    n = len(A)

    # chỉ xử lý ma trận vuông
    if n == 0 or n != len(A[0]):
        raise ValueError("The matrix is not a square one")
    
    # khởi tạo ma trận rỗng n x n
    inverseOfA = [[0.0 for _ in range(n)] for _ in range(n)]

    for j in range(n):
        # tạo cột thứ j của ma trận đơn vị
        e_j = [1.0 if i == j else 0.0 for i in range(n)]

        # khử Gauss đưa về dạng tam giác trên U
        U, y, _ = ge.gaussian_eliminate(A, e_j)
        
        # thế ngược tìm vector cột x của ma trận nghịch đảo
        x = bs.back_substitution(self, U, y)

        # thêm vector nghiệm vào cột tương ứng của kết quả
        for i in range(n):
            inverseOfA[i][j] = x[i]

    return inverseOfA