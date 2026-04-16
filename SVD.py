from manim import *
import numpy as np
from PIL import Image

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage[utf8]{inputenc}")
my_template.add_to_preamble(r"\usepackage[T5]{fontenc}")

# ==========================================
# PHẦN 1: TRÌNH BÀY LÝ THUYẾT SVD 
# ==========================================
class SVDTheory(Scene):
    def construct(self):
        # 1. TIÊU ĐỀ VÀ MỞ BÀI
        title = Tex("Định lý Phân tích Giá trị Suy biến (SVD)", tex_template=my_template, font_size=45, color=YELLOW)
        title.to_edge(UP)
        
        intro_text = Tex("Mọi phép biến đổi tuyến tính (ma trận $A$) đều có thể phân tích thành 3 bước cơ bản:", tex_template=my_template, font_size=32)
        intro_text.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(intro_text))
        self.wait(1)

        # 2. CÔNG THỨC CHÍNH
        # Cắt nhỏ công thức để dễ tô màu từng phần: 0: A, 1: =, 2: U, 3: \Sigma, 4: V^T
        formula = MathTex("A", "=", "U", "\\Sigma", "V^T", font_size=80)
        formula.next_to(intro_text, DOWN, buff=1)
        self.play(Write(formula), run_time=2)
        self.wait(1)

        # Đẩy công thức lên một chút để nhường chỗ cho phần giải thích chi tiết bên dưới
        self.play(
            FadeOut(intro_text),
            formula.animate.shift(UP * 1.5)
        )

        # Hàm tiện ích để tạo danh sách giải thích chi tiết (Bullet points)
        def create_detail_box(texts, color):
            group = VGroup()
            for text in texts:
                dot = Dot(color=color, radius=0.08)
                line = Tex(text, tex_template=my_template, font_size=30)
                item = VGroup(dot, line).arrange(RIGHT, buff=0.3)
                group.add(item)
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            # Căn giữa khung chữ xuống dưới công thức
            group.next_to(formula, DOWN, buff=1)
            return group

        # ==========================================
        # 3. GIẢI THÍCH CHI TIẾT TỪNG THÀNH PHẦN
        # ==========================================

        # --- BƯỚC 1: Phân tích V^T ---
        details_V = create_detail_box([
            "Là ma trận trực giao (Orthogonal Matrix) kích thước $n \\times n$.",
            "Chứa các vector riêng (eigenvectors) của $A^T A$.",
            "\\textbf{Ý nghĩa hình học:} Đại diện cho phép xoay hệ trục tọa độ ban đầu."
        ], RED)

        self.play(
            formula[4].animate.set_color(RED),
            formula[0:4].animate.set_opacity(0.3) # Làm mờ các phần khác
        )
        self.play(Write(details_V), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(details_V))

        # --- BƯỚC 2: Phân tích \Sigma ---
        details_S = create_detail_box([
            "Là ma trận đường chéo (Diagonal Matrix).",
            "Chứa các \\textbf{giá trị suy biến} $\\sigma_i \\geq 0$, được sắp xếp giảm dần.",
            "$\\sigma_i$ càng lớn, thông tin mang theo càng quan trọng.",
            "\\textbf{Ý nghĩa hình học:} Kéo giãn không gian dọc theo các trục tọa độ mới."
        ], YELLOW)

        self.play(
            formula[4].animate.set_opacity(0.3),
            formula[3].animate.set_color(YELLOW).set_opacity(1)
        )
        self.play(Write(details_S), run_time=2)
        self.wait(3)
        self.play(FadeOut(details_S))

        # --- BƯỚC 3: Phân tích U ---
        details_U = create_detail_box([
            "Là ma trận trực giao (Orthogonal Matrix) kích thước $m \\times m$.",
            "Chứa các vector riêng (eigenvectors) của $A A^T$.",
            "\\textbf{Ý nghĩa hình học:} Xoay hệ trục lần cuối để khớp với không gian đích."
        ], BLUE)

        self.play(
            formula[3].animate.set_opacity(0.3),
            formula[2].animate.set_color(BLUE).set_opacity(1)
        )
        self.play(Write(details_U), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(details_U))

        # ==========================================
        # 4. TỔNG KẾT BẢN CHẤT
        # ==========================================
        
        # Bật sáng lại toàn bộ công thức
        self.play(formula[0:5].animate.set_opacity(1), formula[0].animate.set_color(WHITE))
        
        summary_text = Tex(
            "Vậy, mọi sự bóp méo không gian phức tạp ($A$) đều là tổ hợp của:\\\\ Xoay ($V^T$) $\\rightarrow$ Kéo giãn ($\\Sigma$) $\\rightarrow$ Xoay ($U$)", 
            tex_template=my_template, 
            font_size=36
        )
        summary_text.next_to(formula, DOWN, buff=1.5)
        
        # Tạo khung viền nổi bật cho câu chốt
        summary_box = SurroundingRectangle(summary_text, color=WHITE, buff=0.3)

        self.play(Write(summary_text))
        self.play(Create(summary_box))
        self.wait(4)

        # Dọn dẹp màn hình để chuẩn bị sang Scene 2
        self.play(FadeOut(VGroup(title, formula, summary_text, summary_box)))
# ==========================================
# PHẦN 2: TRỰC QUAN HÓA BÀI TOÁN HÌNH HỌC 2D
# ==========================================
class SVDGeometry(Scene):
    def construct(self):
        # ==========================================
        # 1. SETUP HÌNH HỌC (Đẩy sang TRÁI màn hình)
        # ==========================================
        grid = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], background_line_style={"stroke_opacity": 0.4})
        circle = Circle(radius=1, color=YELLOW).set_fill(YELLOW, opacity=0.5)
        basis_i = Vector([1, 0], color=GREEN)
        basis_j = Vector([0, 1], color=RED)
        
        # Nhóm lại, thu nhỏ và đẩy sang trái
        geo_group = VGroup(grid, circle, basis_i, basis_j).scale(0.7).shift(LEFT * 3.5)
        self.play(Create(grid), Create(circle), Create(basis_i), Create(basis_j))

        # ==========================================
        # 2. TOÁN HỌC - TÍNH TOÁN TRƯỚC CÁC BƯỚC
        # ==========================================
        A_array = np.array([[2, 1], 
                            [1, 2]])
        
        U_array, S_array, VT_array = np.linalg.svd(A_array)
        Sigma_array = np.diag(S_array)

        # Tính các ma trận trạng thái ở từng bước
        step0_matrix = np.eye(2)                    # Trạng thái gốc (Ma trận đơn vị I)
        step1_matrix = VT_array                     # Sau khi nhân V^T
        step2_matrix = Sigma_array @ VT_array       # Sau khi nhân tiếp Sigma
        step3_matrix = U_array @ step2_matrix       # Sau khi nhân tiếp U (Chính là A)

        # ==========================================
        # 3. SETUP GIAO DIỆN BÊN PHẢI
        # ==========================================
        title = Tex("Mục tiêu: Biến đổi lưới theo ma trận $A$", tex_template=my_template, font_size=36, color=YELLOW)
        title.to_edge(UP).shift(RIGHT * 3.5)

        # Hàm tiện ích để tạo nhanh nhóm (Công thức = Ma trận số)
        def get_math_state(label_str, matrix_array):
            label = MathTex(label_str, "=")
            # np.round(..., 2) giúp làm tròn 2 chữ số thập phân cho gọn màn hình
            matrix_mob = Matrix(np.round(matrix_array, 2)).scale(0.8)
            return VGroup(label, matrix_mob).arrange(RIGHT)

        # Trạng thái ban đầu
        step_desc = Tex("Trạng thái ban đầu: Lưới chuẩn ($I$)", tex_template=my_template, font_size=30)
        current_math = get_math_state("I", step0_matrix)
        
        # Sắp xếp chữ giải thích và ma trận theo chiều dọc
        right_group = VGroup(step_desc, current_math).arrange(DOWN, buff=0.8).next_to(title, DOWN, buff=1)
        
        self.play(Write(title), Write(right_group))
        self.wait(1)

        # ==========================================
        # 4. CHẠY HIỆU ỨNG ĐỒNG BỘ
        # ==========================================
        
        # Bước 1: Áp dụng V^T (Xoay)
        new_desc_1 = Tex("Bước 1: Áp dụng phép xoay $V^T$", tex_template=my_template, font_size=30, color=RED).move_to(step_desc)
        new_math_1 = get_math_state("V^T", step1_matrix).move_to(current_math)
        
        self.play(
            Transform(step_desc, new_desc_1),
            Transform(current_math, new_math_1),
            # Thêm about_point vào đây
            geo_group.animate.apply_matrix(VT_array, about_point=LEFT * 3.5),
            run_time=2
        )
        self.wait(1.5)

        # Bước 2: Áp dụng Sigma (Kéo giãn)
        new_desc_2 = Tex("Bước 2: Kéo giãn hệ trục với $\Sigma$", tex_template=my_template, font_size=30, color=YELLOW).move_to(step_desc)
        new_math_2 = get_math_state("\Sigma V^T", step2_matrix).move_to(current_math)
        
        self.play(
            Transform(step_desc, new_desc_2),
            Transform(current_math, new_math_2),
            # Thêm about_point vào đây
            geo_group.animate.apply_matrix(Sigma_array, about_point=LEFT * 3.5),
            run_time=2
        )
        self.wait(1.5)

        # Bước 3: Áp dụng U (Xoay lần cuối)
        new_desc_3 = Tex("Bước 3: Hoàn thiện với phép xoay $U$", tex_template=my_template, font_size=30, color=BLUE).move_to(step_desc)
        new_math_3 = get_math_state("U \Sigma V^T = A", step3_matrix).move_to(current_math)
        
        self.play(
            Transform(step_desc, new_desc_3),
            Transform(current_math, new_math_3),
            # Thêm about_point vào đây
            geo_group.animate.apply_matrix(U_array, about_point=LEFT * 3.5),
            run_time=2
        )
        self.wait(2)

        # Kết thúc phân cảnh
        self.play(FadeOut(geo_group), FadeOut(title), FadeOut(step_desc), FadeOut(current_math))
# ==========================================
# PHẦN 3: ỨNG DỤNG NÉN ẢNH VỚI SVD (SỐ NHẢY MƯỢT MÀ)
# ==========================================
class ImageCompression(Scene):
    def construct(self):
        # 1. SETUP TIÊU ĐỀ
        title = Tex("Ứng dụng thực tế: Nén ảnh (Truncated SVD)", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        try:
            # 2. XỬ LÝ ẢNH & TOÁN HỌC
            img = Image.open("sample.jpg").convert('L')
            img = img.resize((300, 300)) 
            img_array = np.array(img)
            h, w = img_array.shape 
            original_size = h * w
            
            U, S, VT = np.linalg.svd(img_array, full_matrices=False)
            
            def get_image_mobject(matrix):
                matrix = np.clip(matrix, 0, 255).astype(np.uint8)
                return ImageMobject(matrix).set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"]).scale(2)

            # 3. HIỂN THỊ ẢNH GỐC BAN ĐẦU
            current_image = get_image_mobject(img_array).shift(LEFT * 3.5)
            # Cố định tọa độ của nhãn để chữ không bị giật khi ảnh thay đổi
            label_pos = LEFT * 3.5 + DOWN * 2.5
            
            img_label = Tex("Ảnh gốc ($100\%$ dung lượng)", tex_template=my_template, font_size=30).move_to(label_pos)
            self.play(FadeIn(current_image), Write(img_label))
            self.wait(1)

            # =======================================================
            # KỸ THUẬT VALUETRACKER: ĐỂ SỐ NHẢY MƯỢT MÀ
            # =======================================================
            # Khởi tạo bộ đếm ẩn, bắt đầu từ k = 5
            k_tracker = ValueTracker(5)

            # Hàm này sẽ được Manim gọi LẠI MỖI KHUNG HÌNH (60 lần/giây)
            def get_dynamic_panel():
                # Lấy giá trị float hiện tại của ValueTracker (ví dụ: 12.45)
                k_val = k_tracker.get_value() 
                compressed_size = k_val * (h + w + 1)
                ratio = (compressed_size / original_size) * 100
                
                color_ratio = GREEN if ratio <= 30 else (YELLOW if ratio <= 60 else RED)

                # Dùng int() để k là số nguyên, và {:.1f} để tỉ lệ nhảy từng 0.1
                stats = VGroup(
                    Tex(f"- Số lượng đặc trưng ($k$): {int(k_val)}", tex_template=my_template, font_size=30),
                    Tex(f"- Dung lượng lưu trữ: {int(compressed_size):,} số", tex_template=my_template, font_size=30),
                    Tex(f"- Tỉ lệ so với gốc: {ratio:.1f}\%", tex_template=my_template, font_size=30, color=color_ratio)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
                
                formula = Tex(f"$A_{{{int(k_val)}}} \\approx U_{{{int(k_val)}}} \\Sigma_{{{int(k_val)}}} V_{{{int(k_val)}}}^T$", font_size=40, color=BLUE)
                
                panel = VGroup(formula, stats).arrange(DOWN, buff=0.8)
                
                # MẸO: Cố định mép trái (aligned_edge=LEFT) vào một tọa độ để khi
                # con số dài ra (ví dụ 9 -> 10), khung chữ không bị giật lùi.
                panel.move_to(RIGHT * 1.5, aligned_edge=LEFT)
                return panel

            # Biến panel và nhãn ảnh thành đối tượng "Sống" (luôn cập nhật)
            dynamic_panel = always_redraw(get_dynamic_panel)
            dynamic_label = always_redraw(lambda: Tex(f"Ảnh khôi phục ($k={int(k_tracker.get_value())}$)", tex_template=my_template, font_size=30, color=YELLOW).move_to(label_pos))

            # =======================================================
            # 5. CHẠY HIỆU ỨNG TĂNG DẦN
            # =======================================================
            
            # Bước đầu tiên: Biến ảnh gốc thành ảnh k=5 và hiện bảng bên phải
            k_matrix_5 = U[:, :5] @ np.diag(S[:5]) @ VT[:5, :]
            img_5 = get_image_mobject(k_matrix_5).shift(LEFT * 3.5)
            
            self.play(
                FadeTransform(current_image, img_5),
                Transform(img_label, dynamic_label), 
                Write(dynamic_panel), 
                run_time=2
            )
            current_image = img_5
            self.wait(1)

            # Các bước tiếp theo: Các số sẽ chạy vù vù như đồng hồ!
            k_values = [20, 50, 150]
            for k in k_values:
                reconstructed_matrix = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]
                new_image = get_image_mobject(reconstructed_matrix).shift(LEFT * 3.5)
                
                self.play(
                    FadeTransform(current_image, new_image),
                    # Dòng này là linh hồn: Yêu cầu ValueTracker chạy dần lên số k mới
                    k_tracker.animate.set_value(k),
                    run_time=3, # Chạy trong 3 giây để người xem kịp ngắm số nhảy
                    rate_func=linear # linear giúp số nhảy với tốc độ đều đặn
                )
                current_image = new_image
                self.wait(1.5)

            # 6. KẾT LUẬN CÚ CHỐT
            conclusion = Tex("Chỉ với $\\sim 50\%$ dữ liệu, mắt người đã thấy nét gần như gốc!", tex_template=my_template, font_size=30, color=GREEN)
            # Neo câu chốt vào dưới mép trái của panel
            conclusion.next_to(dynamic_panel, DOWN, buff=1, aligned_edge=LEFT)
            self.play(Write(conclusion))
            self.wait(3)

        except FileNotFoundError:
            error_msg = Tex("Lỗi: Không tìm thấy file 'sample.jpg'.", tex_template=my_template, color=RED)
            self.play(Write(error_msg))
            self.wait(3)
    def construct(self):
        # 1. SETUP TIÊU ĐỀ
        title = Tex("Ứng dụng thực tế: Nén ảnh (Truncated SVD)", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        try:
            # 2. XỬ LÝ ẢNH & TOÁN HỌC
            img = Image.open("Rose_BlackPink.jpg").convert('L')
            # Thu nhỏ ảnh lại kích thước 300x300 để có không gian viết chữ bên phải
            img = img.resize((300, 300)) 
            img_array = np.array(img)
            h, w = img_array.shape 
            
            # Phân tích SVD
            U, S, VT = np.linalg.svd(img_array, full_matrices=False)
            
            def get_image_mobject(matrix):
                matrix = np.clip(matrix, 0, 255).astype(np.uint8)
                return ImageMobject(matrix).set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"]).scale(2)

            # 3. BỐ CỤC MÀN HÌNH TRÁI (HIỂN THỊ ẢNH)
            # Ảnh gốc ban đầu
            current_image = get_image_mobject(img_array).shift(LEFT * 3.5)
            img_label = Tex("Ảnh gốc ($100\%$ dung lượng)", tex_template=my_template, font_size=30).next_to(current_image, DOWN)
            
            self.play(FadeIn(current_image), Write(img_label))
            self.wait(1)

            # 4. HÀM TẠO BẢNG THÔNG SỐ BÊN PHẢI
            def get_info_panel(k_val):
                # Công thức toán học
                formula = Tex(f"$A_{{{k_val}}} \\approx U_{{{k_val}}} \\Sigma_{{{k_val}}} V_{{{k_val}}}^T$", font_size=40, color=BLUE)
                
                # Tính toán dung lượng lưu trữ thực tế
                original_size = h * w
                compressed_size = k_val * (h + w + 1)
                ratio = (compressed_size / original_size) * 100
                
                # Đổi màu cảnh báo tùy theo dung lượng
                color_ratio = GREEN if ratio <= 30 else (YELLOW if ratio <= 60 else RED)

                # Dòng Text thông số
                stats = VGroup(
                    Tex(f"- Số lượng đặc trưng ($k$): {k_val}", tex_template=my_template, font_size=30),
                    Tex(f"- Dung lượng lưu trữ: {compressed_size:,} số", tex_template=my_template, font_size=30),
                    Tex(f"- Tỉ lệ so với ảnh gốc: {ratio:.1f}\%", tex_template=my_template, font_size=30, color=color_ratio)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
                
                return VGroup(formula, stats).arrange(DOWN, buff=0.8).shift(RIGHT * 3.5)

            # 5. CHẠY HIỆU ỨNG CÁC BƯỚC NÉN K
            k_values = [5, 20, 50, 150]
            
            # Khởi tạo panel hiển thị thông số bên phải
            current_panel = get_info_panel(k_values[0])
            
            for i, k in enumerate(k_values):
                # Tái tạo ảnh bằng cách nhân ma trận
                reconstructed_matrix = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]
                new_image = get_image_mobject(reconstructed_matrix).shift(LEFT * 3.5)
                new_label = Tex(f"Ảnh khôi phục ($k={k}$)", tex_template=my_template, font_size=30, color=YELLOW).next_to(new_image, DOWN)
                
                new_panel = get_info_panel(k)

                if i == 0:
                    # Lần k=5 đầu tiên: Biến ảnh gốc thành ảnh mờ, xuất hiện panel thông số
                    self.play(
                        FadeTransform(current_image, new_image),
                        Transform(img_label, new_label),
                        Write(current_panel),
                        run_time=2
                    )
                else:
                    # Các lần sau: Cập nhật ảnh nét dần lên và thay đổi thông số
                    self.play(
                        FadeTransform(current_image, new_image),
                        Transform(img_label, new_label),
                        Transform(current_panel, new_panel),
                        run_time=1.5
                    )
                
                current_image = new_image
                self.wait(1.5)

            # 6. KẾT LUẬN CÚ CHỐT
            conclusion = Tex("Chỉ với $\\sim 50\%$ dữ liệu, mắt người đã thấy nét gần như gốc!", tex_template=my_template, font_size=20, color=GREEN)
            conclusion.next_to(current_panel, DOWN, buff=1)
            self.play(Write(conclusion))
            self.wait(3)

        except FileNotFoundError:
            error_msg = Tex("Lỗi: Không tìm thấy file 'sample.jpg'.\\ Vui lòng để ảnh cùng thư mục với code.", tex_template=my_template, color=RED)
            self.play(Write(error_msg))
            self.wait(3)