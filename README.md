# do_an_tudtk






# Hàm `rank_and_basis` - Tìm Hạng và Cơ sở Không gian Ma trận-----------------------------------------------------------------------------------

## Mô tả
Hàm `rank_and_basis` thực hiện phân tích một ma trận để tìm ra **Hạng** và các vector cơ sở cho 3 không gian cốt lõi trong Đại số tuyến tính:
- **Không gian Dòng (Row Space)**
- **Không gian Cột (Column Space)**
- **Không gian Nghiệm (Null Space / Kernel)**

**Thuật toán sử dụng:** 
- Hàm gọi phương pháp **Khử Gauss (Gaussian Elimination)** để đưa ma trận về dạng bậc thang (Row Echelon Form - REF).
- Sử dụng phương pháp **Thế ngược (Back-substitution)** để giải hệ phương trình thuần nhất Ax = 0 nhằm tìm ra không gian nghiệm.
- Có xử lý sai số số thập phân (Floating-point error) bằng hằng số `Zero` để đảm bảo độ chính xác khi xác định các phần tử Pivot.

---

## Tham số đầu vào (Parameters)
- `A` *(list of lists, tùy chọn)*: Ma trận đầu vào cần tính toán. 
- *Lưu ý:* Nếu không truyền `A` (hoặc `A=None`), hàm sẽ tự động lấy thuộc tính `self.A` của đối tượng (được gọi như một phương thức của class).

---

## Kết quả trả về (Returns)
Hàm trả về một `tuple` gồm 4 giá trị theo đúng thứ tự:
1. `rank` *(int)*: Hạng của ma trận (tương ứng với số lượng cột Pivot).
2. `col_basis` *(list)*: Danh sách các vector cột tạo thành cơ sở của không gian cột (được trích xuất trực tiếp từ ma trận gốc A).
3. `row_basis` *(list)*: Danh sách các vector dòng tạo thành cơ sở của không gian dòng (được trích xuất từ ma trận bậc thang).
4. `null_basis` *(list)*: Danh sách các vector tạo thành cơ sở của không gian nghiệm. Nếu ma trận chỉ có nghiệm tầm thường, danh sách này sẽ rỗng.

---

## Ví dụ sử dụng

```python
import matrix as mt

# 1. Khởi tạo ma trận A
A = [
    [1, 2, 4],
    [2, 3, 1],
    [3, 1, 2]
]
# Giả sử hàm rank_and_basis được tích hợp trong class Matrix
my_matrix = mt.Matrix(A)
# 2. Gọi hàm thực thi
rank, col_b, row_b, null_b = my_matrix.rank_and_basis()
# 3. In kết quả
print(f"Hạng của ma trận (Rank): {rank}")
print(f"Cơ sở Không gian Cột: {col_b}")
print(f"Cơ sở Không gian Dòng: {row_b}")
print(f"Cơ sở Không gian Nghiệm: {null_b}")