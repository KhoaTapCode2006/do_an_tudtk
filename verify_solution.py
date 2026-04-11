import numpy as np
from scipy import linalg
import traceback
import gaussian_eliminate as ge
import back_substitution as bs
import determinant as dt
import inverse as inv
import rank_and_basis as rb

def verify_solutions():
    log_file = "test_results.txt"
    
    # QUY ƯỚC MÃ SỐ CHO HÀM BACK_SUBSTITUTION
    # Hãy thay đổi 2 con số này thành giá trị mà code của bạn đang trả về
    CODE_VO_NGHIEM = float('nan') # Hoặc -1, 0, v.v. tùy code của bạn
    CODE_VO_SO_NGHIEM = float('inf') # Hoặc -2, 1, v.v. tùy code của bạn

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== NHẬT KÝ KIỂM THỬ ĐỒ ÁN TOÁN ỨNG DỤNG ===\n")
        f.write("Lưu ý: Kết quả chuẩn của NumPy/SciPy chỉ hiển thị khi code của bạn tính sai.\n")
        f.write("="*60 + "\n\n")

        # ---------------------------------------------------------
        # 1. KIỂM TRA GAUSSIAN ELIMINATE & BACK SUBSTITUTION
        # ---------------------------------------------------------
        f.write("--- PHẦN 1: HỆ PHƯƠNG TRÌNH LINEAR (GAUSS & BACK SUB) ---\n")
        
        test_systems = [
            {
                "name": "1. Có nghiệm duy nhất (Cơ bản)",
                "A": np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]]),
                "b": np.array([8., -11., -3.])
            },
            {
                "name": "2. Có nghiệm duy nhất (Bắt buộc Partial Pivoting)",
                "A": np.array([[0., 2., 1.], [1., -2., -3.], [-1., 1., 2.]]),
                "b": np.array([-8., 0., 3.])
            },
            {
                "name": "3. Hệ Vô Nghiem (Dòng cuối 0 = c)",
                "A": np.array([[1., 1.], [1., 1.]]),
                "b": np.array([1., 2.])
            },
            {
                "name": "4. Hệ Vô Số Nghiệm",
                "A": np.array([[1., 2.], [2., 4.]]),
                "b": np.array([1., 2.])
            }
        ]

        for case in test_systems:
            A, b = case["A"], case["b"]
            f.write(f"\n[Test Case] {case['name']}\n")
            
            try:
                # Chạy hàm của bạn (Đảm bảo truyền copy để không làm hỏng data gốc)
                U, c, _ = ge.gaussian_eliminate(A.copy(), b.copy()) 
                x_your_code = bs.back_substitution(U, c)
                
                # --- GIẢ LẬP KẾT QUẢ ĐỂ CHẠY THỬ CODE NÀY (BẠN HÃY XÓA PHẦN NÀY ĐI) ---
                rank_A = np.linalg.matrix_rank(A)
                rank_aug = np.linalg.matrix_rank(np.column_stack((A, b)))
                if rank_A < rank_aug:
                    x_your_code = CODE_VO_NGHIEM
                elif rank_A < A.shape[1]:
                    x_your_code = CODE_VO_SO_NGHIEM
                else:
                    x_your_code = np.linalg.solve(A, b) # Code bạn tính đúng
                    # x_your_code = np.array([0, 0, 0]) # Mở dòng này ra để test chức năng báo sai
                # -----------------------------------------------------------------------

                f.write(f"  + Output của bạn: {x_your_code}\n")

                # Xác định kết quả chuẩn bằng Toán học
                is_correct = False
                expected_str = ""

                if rank_A < rank_aug:
                    expected_str = "Hệ vô nghiệm"
                    # Kiểm tra con số vô nghiệm
                    if np.isnan(CODE_VO_NGHIEM):
                        is_correct = np.isnan(x_your_code)
                    else:
                        is_correct = (x_your_code == CODE_VO_NGHIEM)

                elif rank_A < A.shape[1]:
                    expected_str = "Hệ vô số nghiệm"
                    # Kiểm tra con số vô số nghiệm
                    if np.isinf(CODE_VO_SO_NGHIEM):
                        is_correct = np.isinf(x_your_code)
                    else:
                        is_correct = (x_your_code == CODE_VO_SO_NGHIEM)

                else:
                    expected_res = np.linalg.solve(A, b)
                    expected_str = str(expected_res)
                    is_correct = np.allclose(x_your_code, expected_res, atol=1e-9)

                # Ghi kết quả
                if is_correct:
                    f.write("  => TRẠNG THÁI: [ ĐÚNG ]\n")
                else:
                    f.write("  => TRẠNG THÁI: [ SAI ]\n")
                    f.write(f"  => Kết quả chuẩn (NumPy/Math): {expected_str}\n")

            except Exception as e:
                f.write(f"  => LỖI THỰC THI (CRASH): {str(e)}\n")
                f.write(traceback.format_exc() + "\n")

        # ---------------------------------------------------------
        # 2. KIỂM TRA ĐỊNH THỨC (DETERMINANT)
        # ---------------------------------------------------------
        f.write("\n" + "="*60 + "\n")
        f.write("--- PHẦN 2: KIỂM TRA ĐỊNH THỨC (DETERMINANT) ---\n")
        
        test_dets = [
            {"name": "1. Ma trận 2x2 cơ bản", "A": np.array([[4., 7.], [2., 6.]])},
            {"name": "2. Ma trận cần hoán vị", "A": np.array([[0., 1.], [1., 0.]])},
            {"name": "3. Ma trận suy biến (det=0)", "A": np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])}
        ]

        for case in test_dets:
            A = case["A"]
            f.write(f"\n[Test Case] {case['name']}\n")
            
            try:
                # my_det = dt.determinant(A.copy())
                my_det = np.linalg.det(A) # Giả lập code chạy đúng

                np_det = np.linalg.det(A)
                # Xử lý sai số float với số 0
                if np.isclose(np_det, 0): np_det = 0.0

                f.write(f"  + Output của bạn: {my_det}\n")

                if np.isclose(my_det, np_det, atol=1e-9):
                    f.write("  => TRẠNG THÁI: [ ĐÚNG ]\n")
                else:
                    f.write("  => TRẠNG THÁI: [ SAI ]\n")
                    f.write(f"  => Kết quả chuẩn (NumPy): {np_det}\n")

            except Exception as e:
                f.write(f"  => LỖI THỰC THI (CRASH): {str(e)}\n")

        # ---------------------------------------------------------
        # 3. KIỂM TRA MA TRẬN NGHỊCH ĐẢO (INVERSE)
        # ---------------------------------------------------------
        f.write("\n" + "="*60 + "\n")
        f.write("--- PHẦN 3: KIỂM TRA NGHỊCH ĐẢO (INVERSE) ---\n")
        
        test_inv = [
            {"name": "1. Ma trận khả nghịch", "A": np.array([[4., 7.], [2., 6.]])},
            {"name": "2. Ma trận không khả nghịch (suy biến)", "A": np.array([[1., 2.], [2., 4.]])}
        ]

        for case in test_inv:
            A = case["A"]
            f.write(f"\n[Test Case] {case['name']}\n")
            
            try:
                # my_inv = inv.inverse(A.copy())
                # Giả lập:
                if np.isclose(np.linalg.det(A), 0):
                    my_inv = None # Giả sử code bạn trả về None nếu không thể nghịch đảo
                else:
                    my_inv = np.linalg.inv(A)

                f.write(f"  + Output của bạn:\n{my_inv}\n")

                if np.isclose(np.linalg.det(A), 0):
                    if my_inv is None: # Hãy sửa điều kiện này khớp với code của bạn
                        f.write("  => TRẠNG THÁI: [ ĐÚNG (Đã phát hiện không khả nghịch) ]\n")
                    else:
                        f.write("  => TRẠNG THÁI: [ SAI ]\n")
                        f.write("  => Kết quả chuẩn: Ma trận suy biến, không có nghịch đảo.\n")
                else:
                    np_inv = np.linalg.inv(A)
                    if np.allclose(my_inv, np_inv, atol=1e-9):
                        f.write("  => TRẠNG THÁI: [ ĐÚNG ]\n")
                    else:
                        f.write("  => TRẠNG THÁI: [ SAI ]\n")
                        f.write(f"  => Kết quả chuẩn (NumPy):\n{np_inv}\n")

            except Exception as e:
                f.write(f"  => LỖI THỰC THI (CRASH): {str(e)}\n")

        # ---------------------------------------------------------
        # 4. KIỂM TRA ĐỘC LẬP HÀM BACK SUBSTITUTION
        # ---------------------------------------------------------
        f.write("\n" + "="*60 + "\n")
        f.write("--- PHẦN 4: KIỂM TRA ĐỘC LẬP THẾ NGƯỢC (BACK SUBSTITUTION) ---\n")
        
        # Nhắc lại quy ước mã số:
        VO_NGHIEM = float(0)
        VO_SO_NGHIEM = float(-1)

        test_backsub = [
            {
                "name": "1. Cơ bản (Nghiệm duy nhất)",
                "U": np.array([[2., 1., -1.], [0., -0.5, 0.5], [0., 0., -1.]]),
                "c": np.array([8., 1., 1.]),
                "type": "unique"
            },
            {
                "name": "2. Nghiệm vector không",
                "U": np.array([[1., 2.], [0., 3.]]),
                "c": np.array([0., 0.]),
                "type": "unique"
            },
            {
                "name": "3. Edge case: Chia cho số cực nhỏ (Ổn định số)",
                "U": np.array([[1., 1.], [0., 1e-15]]),
                "c": np.array([2., 1e-15]),
                "type": "unique"
            },
            {
                "name": "4. Vô nghiệm (Dòng cuối U bằng 0, c khác 0)",
                "U": np.array([[1., 2., 3.], [0., 4., 5.], [0., 0., 0.]]),
                "c": np.array([1., 2., 5.]),
                "type": "no_solution"
            },
            {
                "name": "5. Vô số nghiệm (Dòng cuối U và c đều bằng 0)",
                "U": np.array([[1., -1., 2.], [0., 2., 1.], [0., 0., 0.]]),
                "c": np.array([4., 5., 0.]),
                "type": "inf_solution"
            }
        ]

        for case in test_backsub:
            U, c = case["U"], case["c"]
            f.write(f"\n[Test Case] {case['name']}\n")
            
            try:
                # 1. Chạy hàm của nhóm bạn
                # my_x = bs.back_substitution(U.copy(), c.copy())
                
                # --- GIẢ LẬP KẾT QUẢ ĐỂ CHẠY THỬ (BẠN HÃY XÓA PHẦN NÀY ĐI) ---
                if case["type"] == "unique":
                    my_x = linalg.solve_triangular(U, c)
                elif case["type"] == "no_solution":
                    my_x = VO_NGHIEM
                else:
                    my_x = VO_SO_NGHIEM
                # --------------------------------------------------------------

                f.write(f"  + Output của bạn: {my_x}\n")

                # 2. Đối chiếu logic
                if case["type"] == "no_solution":
                    # Kiểm tra code có trả về đúng biến đại diện Vô nghiệm không
                    if np.isnan(VO_NGHIEM) and np.isnan(my_x):
                        f.write("  => TRẠNG THÁI: [ ĐÚNG (Hệ Vô nghiệm) ]\n")
                    elif my_x == VO_NGHIEM:
                        f.write("  => TRẠNG THÁI: [ ĐÚNG (Hệ Vô nghiệm) ]\n")
                    else:
                        f.write("  => TRẠNG THÁI: [ SAI ] - Kỳ vọng: Mã Vô nghiệm\n")
                        
                elif case["type"] == "inf_solution":
                    # Kiểm tra code có trả về đúng biến đại diện Vô số nghiệm không
                    if np.isinf(VO_SO_NGHIEM) and np.isinf(my_x):
                        f.write("  => TRẠNG THÁI: [ ĐÚNG (Hệ Vô số nghiệm) ]\n")
                    elif my_x == VO_SO_NGHIEM:
                        f.write("  => TRẠNG THÁI: [ ĐÚNG (Hệ Vô số nghiệm) ]\n")
                    else:
                        f.write("  => TRẠNG THÁI: [ SAI ] - Kỳ vọng: Mã Vô số nghiệm\n")
                        
                else:
                    # Dùng scipy.linalg.solve_triangular cho các trường hợp có nghiệm
                    expected_x = linalg.solve_triangular(U, c)
                    if np.allclose(my_x, expected_x, atol=1e-9):
                        f.write("  => TRẠNG THÁI: [ ĐÚNG ]\n")
                    else:
                        f.write("  => TRẠNG THÁI: [ SAI ]\n")
                        f.write(f"  => Kết quả chuẩn (SciPy):\n{expected_x}\n")
                        # Ghi chú thêm phần dư (Residual) để đánh giá sai số
                        residual = np.linalg.norm(np.dot(U, my_x) - c)
                        f.write(f"  => Sai số dư (Residual Error): {residual}\n")

            except Exception as e:
                f.write(f"  => LỖI THỰC THI (CRASH): {str(e)}\n")

    print(f"✅ Đã chạy xong kiểm thử. Mở file '{log_file}' để xem kết quả chi tiết!")

if __name__ == "__main__":
    verify_solutions()