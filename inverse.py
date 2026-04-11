import matrix as mt
import gaussian_eliminate as ge

def inverse(self, A): 
    """ Tìm ma trận nghịch đảo bằng phương pháp Gauss-Jordan trên ma trận mở rộng [A | I] """
    n = len(A)
    if n == 0:
        raise ValueError("Matrix is empty")
    if n != len(A[0]):
        raise ValueError("The matrix is not a square one")
    
    # tạo ma trận mở rộng [A|I]
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]

    for col in range(n):
        # tìm hàng chứa pivot lớn nhất
        max_row = col
        for i in range(col + 1, n):
            if abs(aug[i][col]) > abs(aug[max_row][col]):
                max_row = i
        
        # kiểm tra ma trận suy biến
        if abs(aug[max_row][col]) <= mt.Matrix.Zero:
            raise ValueError("Can't find inverse of singular matrix")

        # hoán đổi hàng hiện tại với hàng có pivot lớn nhất
        aug[col], aug[max_row] = aug[max_row], aug[col]

        # chia cả hàng cho phần tử đường chéo để nó biến thành số 1
        pivot = aug[col][col]
        for j in range(col, 2 * n):
            aug[col][j] /= pivot

        # biến tất cả các số KHÁC (trên và dưới) thành số 0
        for i in range(n):
            if i != col:
                factor = aug[i][col]
                for j in range(col, 2 * n):
                    aug[i][j] -= factor * aug[col][j]

    # lấy nửa bên phải, tức inverse của A
    return [row[n:] for row in aug]