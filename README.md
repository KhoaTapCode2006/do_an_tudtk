# Đồ Án Toán Ứng Dụng và Thống Kê 

## 📌 Tổng quan dự án
Đồ án tập trung vào các việc sau đây:

+ Nghiên cứu và cài đặt các phương pháp giải hệ phương trình tuyến tính $Ax = b$, tìm ma trận nghịch đảo, hạng, cơ sở nghiệm, dòng , cột.
+ Cài đặt quá trình phân rã và chéo hoá bằng phương pháp SVD, đồng thời trực quan hoá sự phân rã và chéo hoá ma trận.
+ Vẽ biểu đồ, phân tích, so sánh các phương pháp khử dựa trên thời gian, sai số, số bước. Phân tích ổn định số giữa 2 loại ma trận Hilbert và SPD.

* **Trường:** Đại học Khoa học Tự nhiên - ĐHQG TP.HCM (HCMUS)
* **Học phần:** Toán ứng dụng và thống kê 
* **Lớp:** 24CTT5
* **Ngôn ngữ:** Python 3.10+
* **Công cụ hỗ trợ:** LaTeX, Jupyter Notebook, Manim.
* **Giảng viên thực hành:**
    * ThS. Võ Nam Thục Đoan
    * ThS. Lê Nhựt Nam
    
---

## Sinh viên thực hiện
| MSSV     | Họ và Tên              | 
| :---     | :---                   | 
| 24120075 | Trần Nguyễn Anh Khoa   | 
| 24120048 | Lê Hoàng Hiếu          | 
| 24120131 | Nguyễn Anh Sang        | 
| 24120061 | Lê Nguyễn Gia Huy      | 
| 24120097 | Nguyễn Hoàng Nam       | 


---

## Tổng quan các phần của đồ án

### Phần 1: Phương pháp giải trực tiếp
* **Lớp Matrix:** Xây dựng cấu trúc dữ liệu ma trận tùy chỉnh để quản lý các phép toán cơ bản mà không phụ thuộc quá nhiều vào thư viện ngoài.
* **Khử Gauss:** Cài đặt thuật toán khử Gauss với kỹ thuật chọn phần tử trụ (Partial Pivoting) để tối ưu hóa độ chính xác và tránh lỗi chia cho 0.
* **Thế ngược:** Giải hệ phương trình sau khi ma trận đã được đưa về dạng tam giác trên.
* **Nghịch đảo:** Tìm ma trận nghịch đảo. 
* **Định thức:** Tính định thức của ma trận.
* **Tìm hạng và cơ sở:** Tìm hạng và cơ sở của dòng, cột, nghiệm của ma trận.
* **Kiểm thử:** Kiểm thử sự đúng đắn của các hàm thủ công bằng Numpy.

### Phần 2: Phân rã giá trị đơn lẻ (SVD)
* **Thuật toán Jacobi:** Cài đặt phương pháp xoay Jacobi để tìm trị riêng và vector riêng cho ma trận đối xứng.
* **Phân rã SVD:** Cài đặt thủ công quá trình phân rã $A = U\Sigma V^T$.
* **Chéo hoá:** Chéo hoá ma trận bằng cách áp dụng thuật toán phân rã SVD.
* **Video Manim:** Trực quan hoá quá trình phân rã và chéo hoá bằng Manim, ứng dụng SVD để nén ảnh.

### Phần 3: Phương pháp lặp & Tính ổn định số
* **Gauss-Seidel:** Cài đặt phương pháp lặp để giải hệ phương trình, ưu tiên cho các ma trận chéo trội hoặc ma trận SPD.
* **Thực nghiệm:** Đánh giá thời gian chạy, sai số và bước nhảy giữa các phương pháp: Gauss Partial Pivoting, SVD, và Gauss-Seidel.
* **Phân tích ổn định:**
    * Sử dụng SVD để tính **Số điều kiện (Condition Number)** $\kappa(A) = \sigma_{max}/\sigma_{min}$.
    * So sánh ma trận **Hilbert** (thiếu ổn định) và ma trận **SPD** (ổn định tốt).
* **Kết luận:** Suy luận và đưa ra kết luận về ưu và nhược điểm của các loại phương pháp khử dựa trên số liệu đã phân tích, nhận xét khi nào nên dùng phương pháp khử nào.

---

## Cấu trúc thư mục 
```text
.
├── reports/
│   └── reports.pdf             # File report PDF
├── part1/
│   ├── matrix.py               # Định nghĩa lớp Matrix
│   ├── gaussian_eliminate.py   # Thuật toán khử Gauss
│   ├── back_substitution.py    # Hàm giải phương trình
│   ├── inverse.py              # Tìm ma trận nghịch đảo
│   ├── determinant.py          # Tìm định thức ma trận
│   ├── rank_and_basis.py       # tìm hạng và cơ sở nghiệm, dòng, cột
│   ├── part1_demo.ipynb        # File Jupyter Notebook kiểm thử hàm
│   ├── text_results.txt        # tìm hạng và cơ sở nghiệm, dòng, cột
│   └── verify_solution.py      # File Python kiểm thử hàm
├── part2/
│   ├── decomposition.py        # Thuật toán phân rã SVD
│   ├── diagonalization.py      # Thuật toán chéo hoá ma trận, áp dụng SVD
│   ├── SVD.py                  # File Manim viết bằng Python
│   ├── Manim_demo_link.txt     # File chứa link youtube video demo Manim trực quan hoá 
│   ├── part2_demo.ipynb        # File Jupyter Notebook kiểm thử hàm
│   └── Rose_BlackPink.jpg      # File ảnh dùng để ứng dụng nén ảnh bằng SVD
├── part3/
│   ├── solvers.py              # Các phương pháp giải hệ phương trình Ax = b
│   ├── benchmark.py            # Đo đạc thời gian chạy, sai số, số bước
│   ├── analysis.ipynb          # Phân tích ổn định số bằng đồ thị
│   ├── bieudo1.jpg             # Biểu đồ thời gian chạy Partial và Seidel
│   ├── bieudo2.jpg             # Đồ thị log-log
│   ├── bieudo3.jpg             # Độ hội tụ của Gauss Seidel
│   ├── remark.ipynb            # File Notebook suy luận kết quả từ phân tích
│   ├── ket_qua_console.txt     # Kết quả đo đạc in ra console, lưu vào txt
│   └── ket_qua_kiem_thu.xlsx   # File Excel lưu trữ kết quả đo đạc
|
├── requirements.txt    # File requirements chứa các thư viện cần thiết
└── README.md           # Markdown chứa tổng quan và hướng dẫn cài thư viện
```

## Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
* Python 3.10 trở lên.
* Trình quản lý gói `pip`.

### 2. Cài đặt thư viện phụ thuộc
Tất cả các thư viện cần thiết cho đồ án đều được lưu trữ trong file requirements.txt, mở terminal và chạy lệnh sau
+ pip install -r requirements.txt
