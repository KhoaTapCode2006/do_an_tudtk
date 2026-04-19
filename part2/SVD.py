from manim import *
import numpy as np
from PIL import Image
import math
import random

# Khởi tạo template dùng LaTeX để có thể gõ tiếng Việt có dấu trong video Manim
my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage[utf8]{inputenc}")
my_template.add_to_preamble(r"\usepackage[T5]{fontenc}")

# PHẦN 1: TRÌNH BÀY LÝ THUYẾT SVD 
class SVDTheory(Scene):
    def construct(self):
        
        # 1. TIÊU ĐỀ VÀ MỞ BÀI
        title = Tex("I. Định lý Phân tích Giá trị Suy biến (SVD)", tex_template=my_template, font_size=45, color=YELLOW)
        title.to_edge(UP)
        
        # Bổ sung tính tổng quát: SVD áp dụng cho mọi ma trận (kể cả chữ nhật)
        intro_text = Tex("Mọi ma trận $A_{m \\times n}$ bất kỳ đều có thể phân tách thành tích của 3 ma trận:", tex_template=my_template, font_size=32)
        intro_text.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(intro_text))
        self.wait(1.5) 

        # 2. CÔNG THỨC CHÍNH
        formula = MathTex("A", "=", "U", "\\Sigma", "V^T", font_size=80)
        formula.next_to(intro_text, DOWN, buff=1)
        self.play(Write(formula), run_time=2) 
        self.wait(1)

        self.play(
            FadeOut(intro_text),
            formula.animate.shift(UP * 1.5)
        )

        def create_detail_box(texts, color):
            group = VGroup()
            for text in texts:
                dot = Dot(color=color, radius=0.08)
                line = Tex(text, tex_template=my_template, font_size=30)
                item = VGroup(dot, line).arrange(RIGHT, buff=0.3)
                group.add(item)
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            group.next_to(formula, DOWN, buff=1)
            return group

        # --- BƯỚC 1: Phân tích V^T ---
        details_V = create_detail_box([
            "Là ma trận trực giao (Orthogonal Matrix) kích thước $n \\times n$.",
            "Các cột của $V$ gọi là \\textbf{Vector suy biến phải} (Right singular vectors).",
            "\\textbf{Hình học:} Xoay không gian n-chiều gốc để căn chỉnh các trục tọa độ."
        ], RED)

        self.play(
            formula[4].animate.set_color(RED),
            formula[0:4].animate.set_opacity(0.3) 
        )
        self.play(Write(details_V), run_time=2)
        self.wait(3)
        self.play(FadeOut(details_V))

        # --- BƯỚC 2: Phân tích \Sigma ---
        # Bổ sung mối liên hệ với hạng ma trận
        details_S = create_detail_box([
            "Là ma trận đường chéo (Diagonal) kích thước $m \\times n$.",
            "Chứa các \\textbf{giá trị suy biến} $\\sigma_1 \\geq \\sigma_2 \\geq \\dots \\geq 0$.",
            "Số lượng $\\sigma_i > 0$ chính là \\textbf{Hạng (Rank)} của ma trận $A$.",
            "\\textbf{Hình học:} Co giãn không gian theo tỷ lệ $\\sigma_i$ (Nén/Kéo dài)."
        ], YELLOW)

        self.play(
            formula[4].animate.set_opacity(0.3),
            formula[3].animate.set_color(YELLOW).set_opacity(1)
        )
        self.play(Write(details_S), run_time=2)
        self.wait(3.5)
        self.play(FadeOut(details_S))

        # --- BƯỚC 3: Phân tích U ---
        details_U = create_detail_box([
            "Là ma trận trực giao (Orthogonal Matrix) kích thước $m \\times m$.",
            "Các cột của $U$ gọi là \\textbf{Vector suy biến trái} (Left singular vectors).",
            "\\textbf{Hình học:} Xoay hệ trục lần cuối để chiếu vào không gian đích m-chiều."
        ], BLUE)

        self.play(
            formula[3].animate.set_opacity(0.3),
            formula[2].animate.set_color(BLUE).set_opacity(1)
        )
        self.play(Write(details_U), run_time=2)
        self.wait(3)
        self.play(FadeOut(details_U))

        # 4. TỔNG KẾT & ỨNG DỤNG MỞ RỘNG
        self.play(formula[0:5].animate.set_opacity(1), formula[0].animate.set_color(WHITE))
        
        summary_text = Tex(
            "Tóm lại: Bất kỳ biến đổi tuyến tính nào cũng là tổ hợp của:\\\\ \\textbf{Xoay ($V^T$) $\\rightarrow$ Co giãn ($\\Sigma$) $\\rightarrow$ Xoay ($U$)}", 
            tex_template=my_template, 
            font_size=36
        )
        summary_text.next_to(formula, DOWN, buff=1)
        summary_box = SurroundingRectangle(summary_text, color=WHITE, buff=0.3)

        app_text = Tex(
            "* Ứng dụng: Bằng cách bỏ đi các $\\sigma_i$ nhỏ, ta có thể nén ảnh\\\\ hoặc giảm chiều dữ liệu (Truncated SVD / PCA).",
            tex_template=my_template,
            font_size=28,
            color=LIGHT_GREY
        )
        app_text.next_to(summary_box, DOWN, buff=0.7)

        self.play(Write(summary_text))
        self.play(Create(summary_box))
        self.wait(1)
        self.play(FadeIn(app_text))
        self.wait(4)
        self.play(FadeOut(VGroup(title, formula, summary_text, summary_box, app_text)))

# Hàm giải thuật toán SVD
def custom_svd_general(A, num_iterations=1000, epsilon=1e-10):
    m = len(A)
    n = len(A[0])
    k = min(m, n)
    
    # Các hàm toán học cơ bản
    def mat_vec_mult(M, v):
        return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]
    def transpose(M):
        return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]
    def vec_norm(v):
        return math.sqrt(sum(x*x for x in v))
    def sub_mat(M1, M2):
        return [[M1[i][j] - M2[i][j] for j in range(len(M1[0]))] for i in range(len(M1))]
    def outer_product(u, v, sigma):
        return [[sigma * u[i] * v[j] for j in range(len(v))] for i in range(len(u))]

    A_k = [[A[i][j] for j in range(n)] for i in range(m)]
    U_cols, Sigmas, Vt_rows = [], [], []
    
    for _ in range(k):
        # 1. Khởi tạo ngẫu nhiên
        v = [random.random() for _ in range(n)]
        norm_v = vec_norm(v)
        v = [x / norm_v for x in v]
        
        A_k_T = transpose(A_k)
        # 2. Lặp Power Iteration
        for _ in range(num_iterations):
            Av = mat_vec_mult(A_k, v)
            v_new = mat_vec_mult(A_k_T, Av)
            
            norm_new = vec_norm(v_new)
            if norm_new == 0: break
            v_new = [x / norm_new for x in v_new]
            
            diff1 = vec_norm([v_new[i] - v[i] for i in range(n)])
            diff2 = vec_norm([v_new[i] + v[i] for i in range(n)])
            if diff1 < epsilon or diff2 < epsilon:
                v = v_new
                break
            v = v_new
            
        # 3. Trích xuất thành phần
        u_unnorm = mat_vec_mult(A_k, v)
        sigma = vec_norm(u_unnorm)
        
        if sigma < epsilon: break
            
        u = [x / sigma for x in u_unnorm]
        
        U_cols.append(u)
        Sigmas.append(sigma)
        Vt_rows.append(v)
        
        # 4. Kỹ thuật khử (Deflation)
        A_k = sub_mat(A_k, outer_product(u, v, sigma))
        
    U_matrix = transpose(U_cols)
    return U_matrix, Sigmas, Vt_rows

# CLASS MANIM TRỰC QUAN HÓA SVD
class SVDGeometry(Scene):
    def construct(self):
        title = Tex("Trực quan hóa hình học: Phép biến đổi SVD", tex_template=my_template, font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        # 1. ĐỊNH NGHĨA MA TRẬN BẰNG PYTHON THUẦN (List)
        A_list = [
            [2.0, 1.0], 
            [1.0, 2.0]
        ]
        
        # 2. GIẢI SVD
        U_list, S_list, Vt_list = custom_svd_general(A_list)
        
        # 3. ÉP KIỂU SANG NUMPY ARRAY ĐỂ ĐƯA CHO MANIM VẼ HÌNH
        U_mat = np.array(U_list)
        S_val = np.array(S_list)
        VT_mat = np.array(Vt_list)
        A_array = np.array(A_list)
        
        # 4. KIỂM CHỨNG BẰNG NUMPY 
        np_U, np_S, np_VT = np.linalg.svd(A_array)
        print("\n" + "="*50)
        print("KIỂM CHỨNG THUẬT TOÁN (GHI RA CONSOLE)")
        print("Sigma từ thuật toán tự cài: ", S_val)
        print("Sigma chuẩn từ Numpy:       ", np_S)
        print("="*50 + "\n")

        # VẼ HÌNH
        V_mat = VT_mat.T 
        v1_vec, v2_vec = V_mat[:, 0], V_mat[:, 1]
        Sigma_mat = np.diag(S_val)

        # GIAI ĐOẠN 1: HIỆU ỨNG BIẾN HÌNH ---
        grid = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], background_line_style={"stroke_opacity": 0.4})
        circle = Circle(radius=1, color=YELLOW).set_fill(YELLOW, opacity=0.4)
        
        v1 = Vector(v1_vec, color=RED)
        v2 = Vector(v2_vec, color=RED)
        v1_lab = MathTex("v_1", color=RED, font_size=30).next_to(v1.get_end(), RIGHT, buff=0.1)
        v2_lab = MathTex("v_2", color=RED, font_size=30).next_to(v2.get_end(), UP, buff=0.1)
        
        geo_group = VGroup(grid, circle, v1, v2, v1_lab, v2_lab).scale(0.7).shift(LEFT * 3.5)
        self.play(Create(grid), Create(circle), Create(v1), Create(v2), Write(v1_lab), Write(v2_lab))

        step0_matrix = np.eye(2)                    
        step1_matrix = VT_mat                     
        step2_matrix = Sigma_mat @ VT_mat       
        step3_matrix = U_mat @ step2_matrix       

        def get_math_state(label_str, matrix_array):
            label = MathTex(label_str, "=")
            matrix_mob = Matrix(np.round(matrix_array, 2)).scale(0.8) 
            return VGroup(label, matrix_mob).arrange(RIGHT)

        step_desc = Tex("Trạng thái ban đầu: Lưới chuẩn ($I$)", tex_template=my_template, font_size=30)
        current_math = get_math_state("I", step0_matrix)
        right_group = VGroup(step_desc, current_math).arrange(DOWN, buff=0.8).shift(RIGHT * 3.5)
        
        self.play(Write(right_group))
        self.wait(1)

        # B1: Xoay
        new_desc_1 = Tex("Bước 1: Áp dụng phép xoay $V^T$", tex_template=my_template, font_size=30, color=RED).move_to(step_desc)
        new_math_1 = get_math_state("V^T", step1_matrix).move_to(current_math)
        self.play(
            Transform(step_desc, new_desc_1),
            Transform(current_math, new_math_1),
            geo_group.animate.apply_matrix(VT_mat, about_point=LEFT * 3.5), 
            run_time=2
        )
        self.wait(1.5)

        # B2: Kéo giãn
        new_desc_2 = Tex("Bước 2: Kéo giãn với $\\Sigma$", tex_template=my_template, font_size=30, color=YELLOW).move_to(step_desc)
        new_math_2 = get_math_state("\\Sigma V^T", step2_matrix).move_to(current_math)
        self.play(
            Transform(step_desc, new_desc_2),
            Transform(current_math, new_math_2),
            geo_group.animate.apply_matrix(Sigma_mat, about_point=LEFT * 3.5),
            run_time=2
        )
        self.wait(1.5)

        # B3: Xoay
        new_desc_3 = Tex("Bước 3: Xoay hoàn thiện với $U$", tex_template=my_template, font_size=30, color=BLUE).move_to(step_desc)
        new_math_3 = get_math_state("A = U \\Sigma V^T", step3_matrix).move_to(current_math)
        self.play(
            Transform(step_desc, new_desc_3),
            Transform(current_math, new_math_3),
            geo_group.animate.apply_matrix(U_mat, about_point=LEFT * 3.5),
            run_time=2
        )
        self.wait(2)
        
        self.play(FadeOut(geo_group), FadeOut(step_desc), FadeOut(current_math))

        # GIAI ĐOẠN 2: PIPELINE VIEW ---
        pipe_title = Tex("Tóm tắt quá trình biến đổi (Pipeline View)", tex_template=my_template, font_size=40, color=YELLOW).to_edge(UP)
        self.play(Transform(title, pipe_title))

        pos = [LEFT * 5.1, LEFT * 1.7, RIGHT * 1.7, RIGHT * 5.1]
        colors = [WHITE, RED, YELLOW, GREEN]
        labels = ["x", "V^T x", "\\Sigma V^T x", "A x"]
        transforms = [np.eye(2), VT_mat, Sigma_mat @ VT_mat, A_array] 

        stations = VGroup()
        for i in range(4):
            grid_s = NumberPlane(x_range=[-3, 3], y_range=[-3, 3], background_line_style={"stroke_opacity": 0.2})
            circ_s = Circle(radius=1, color=colors[i], stroke_width=4)
            st = VGroup(grid_s, circ_s).scale(0.35).move_to(pos[i])
            st.apply_matrix(transforms[i], about_point=pos[i])
            
            lab = MathTex(labels[i], font_size=30, color=colors[i]).next_to(st, UP, buff=0.2)
            stations.add(st, lab) 

        self.play(FadeIn(stations[0:2])) 
        for i in range(1, 4):
            arrow = Arrow(pos[i-1] + RIGHT*1.2, pos[i] + LEFT*1.2, color=colors[i], buff=0.1)
            self.play(Create(arrow), FadeIn(stations[i*2:i*2+2]), run_time=1.5) 
        
        self.wait(4)
        self.play(FadeOut(stations), FadeOut(title))

# Lý thuyết chéo hóa ma trận
class DiagonalizationTheory(Scene):
    def construct(self):
        # 1. TIÊU ĐỀ VÀ ĐỊNH NGHĨA
        title = Tex("II. Chéo hóa ma trận (Diagonalization)", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        def_text = Tex("Chéo hóa là việc phân rã một ma trận vuông $A$ thành tích của 3 ma trận:", tex_template=my_template, font_size=32)
        def_text.next_to(title, DOWN, buff=0.8)
        
        formula = MathTex("A", "=", "P", "D", "P^{-1}", font_size=70)
        formula.next_to(def_text, DOWN, buff=0.5)
        
        self.play(FadeIn(def_text))
        self.play(Write(formula), run_time=1.5)
        self.wait(1)

        # Phân tách ý nghĩa của từng phần
        def create_bullet(text, color):
            dot = Dot(color=color, radius=0.08)
            lbl = Tex(text, tex_template=my_template, font_size=30)
            return VGroup(dot, lbl).arrange(RIGHT, buff=0.3)

        bullet_D = create_bullet("$\\mathbf{D}$: Ma trận đường chéo chứa các \\textbf{giá trị riêng} $\\lambda_i$. (Bản chất: Sự co giãn)", YELLOW)
        bullet_P = create_bullet("$\\mathbf{P}$: Ma trận chứa các \\textbf{vector riêng} $v_i$. (Bản chất: Đổi hệ cơ sở)", BLUE)
        bullet_Pinv = create_bullet("$\\mathbf{P^{-1}}$: Phép biến đổi cơ sở ngược lại.", RED)

        bullets = VGroup(bullet_D, bullet_P, bullet_Pinv).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets.next_to(formula, DOWN, buff=1)

        # Đổi màu từng chữ trong công thức tương ứng với giải thích bên dưới
        self.play(
            formula[3].animate.set_color(YELLOW),
            FadeIn(bullet_D)
        )
        self.wait(1)
        self.play(
            formula[2].animate.set_color(BLUE),
            FadeIn(bullet_P)
        )
        self.wait(1)
        self.play(
            formula[4].animate.set_color(RED),
            FadeIn(bullet_Pinv)
        )
        self.wait(2.5)

        # Dọn dẹp màn hình để sang phần Ứng dụng
        self.play(FadeOut(def_text), FadeOut(bullets), formula.animate.shift(UP * 1.2))

        # Điểm mạnh của chéo hóa nằm ở tính lũy thừa
        app_title = Tex("\\textbf{Quyền năng lớn nhất: Tính lũy thừa ma trận $A^n$}", tex_template=my_template, font_size=34, color=GREEN)
        app_title.next_to(formula, DOWN, buff=1)
        
        # Mô phỏng sự triệt tiêu của P^-1 và P
        app_math = MathTex(
            "A^n", "=", "(P D P^{-1})", "(P D P^{-1})", "\\dots", "(P D P^{-1})", 
            font_size=36
        )
        app_math.next_to(app_title, DOWN, buff=0.5)

        # Trực quan hóa việc P^{-1}P = I triệt tiêu lẫn nhau ở giữa
        cancel_line1 = Line(app_math[2][-3:].get_corner(DL), app_math[3][:1].get_corner(UR), color=RED, stroke_width=3)
        cancel_line2 = Line(app_math[3][-3:].get_corner(DL), app_math[5][:1].get_corner(UR), color=RED, stroke_width=3)

        app_res = MathTex(
            "A^n", "=", "P", "D^n", "P^{-1}", 
            font_size=55, color=GREEN
        )
        app_res.next_to(app_math, DOWN, buff=0.8)

        box = SurroundingRectangle(app_res, color=YELLOW, buff=0.3)
        note_Dn = Tex("(Chỉ cần tính lũy thừa các số trên đường chéo của $D$)", tex_template=my_template, font_size=24).next_to(box, DOWN, buff=0.3)

        self.play(Write(app_title))
        self.play(FadeIn(app_math))
        self.wait(1)
        
        # Gạch bỏ các phần tử triệt tiêu
        self.play(Create(cancel_line1), Create(cancel_line2))
        self.wait(0.5)
        
        # Rút gọn thành công thức chốt
        self.play(TransformFromCopy(app_math, app_res))
        self.play(Create(box), FadeIn(note_Dn))
        self.wait(4)

        # Xóa sạch màn hình chuẩn bị chuyển sang Scene tính toán
        self.play(FadeOut(VGroup(title, formula, app_title, app_math, cancel_line1, cancel_line2, app_res, box, note_Dn)))

# Ví dụ thực tế chéo hóa ma trận
class Diagonalization(Scene):
    def construct(self):
        title = Tex("Ví dụ thực tế cho việc chéo hóa ma trận:", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        # Hiển thị Ma trận A ban đầu trên cùng
        mat_A = Matrix([[2, 1], [1, 2]])
        eq_A = VGroup(MathTex("A = "), mat_A).arrange(RIGHT).to_edge(UP, buff=1.2)
        self.play(FadeIn(eq_A))

        # BƯỚC 1: TÍNH GIÁ TRỊ RIÊNG (Eigenvalues)
        step1_title = Tex("Bước 1: Tìm Giá trị riêng $\\lambda$ từ phương trình đặc trưng", tex_template=my_template, font_size=30, color=BLUE)
        eq_det = MathTex("\\det(A - \\lambda I) = 0", font_size=32)
        eq_calc = MathTex("\\Rightarrow (2-\\lambda)^2 - 1 = 0 \\quad \\Rightarrow \\quad \\lambda^2 - 4\\lambda + 3 = 0", font_size=32)
        eq_res = MathTex("\\Rightarrow \\lambda_1 = 3, \\quad \\lambda_2 = 1", font_size=32, color=YELLOW)
        
        # Sắp xếp các dòng giải toán theo chiều dọc
        step1_group = VGroup(step1_title, eq_det, eq_calc, eq_res).arrange(DOWN, buff=0.3).next_to(eq_A, DOWN, buff=0.5)
        
        self.play(Write(step1_title))
        self.play(FadeIn(eq_det))
        self.play(Write(eq_calc))
        self.play(FadeIn(eq_res))
        self.wait(1.5)

        # BƯỚC 2: TÍNH VECTOR RIÊNG (Eigenvectors)
        step2_title = Tex("Bước 2: Tìm Vector riêng $v$ từ hệ $(A - \\lambda I)v = 0$", tex_template=my_template, font_size=30, color=GREEN)
        v1_eq = MathTex("\\text{Với } \\lambda_1 = 3 \\Rightarrow v_1 = \\begin{bmatrix} 1/\\sqrt{2} \\\\ 1/\\sqrt{2} \\end{bmatrix}", tex_template=my_template, font_size=32)
        v2_eq = MathTex("\\text{Với } \\lambda_2 = 1 \\Rightarrow v_2 = \\begin{bmatrix} -1/\\sqrt{2} \\\\ 1/\\sqrt{2} \\end{bmatrix}", tex_template=my_template, font_size=32)
        
        # Đặt 2 vector nằm ngang hàng nhau
        vec_group = VGroup(v1_eq, v2_eq).arrange(RIGHT, buff=1)
        step2_group = VGroup(step2_title, vec_group).arrange(DOWN, buff=0.3).next_to(step1_group, DOWN, buff=0.5)

        self.play(Write(step2_title))
        self.play(FadeIn(v1_eq), FadeIn(v2_eq))
        self.wait(2)

        self.play(FadeOut(eq_A), FadeOut(step1_group), FadeOut(step2_group))

        # BƯỚC 3: LẮP RÁP THÀNH P, D, P^-1 
        step3_title = Tex("Bước 3: Lập phân tích $A = P D P^{-1}$", tex_template=my_template, font_size=36, color=YELLOW)
        step3_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(step3_title))

        math_A2 = MathTex("A =").scale(0.85)
        
        matrix_P = Matrix(
            [["\\frac{1}{\\sqrt{2}}", "-\\frac{1}{\\sqrt{2}}"], 
             ["\\frac{1}{\\sqrt{2}}", "\\frac{1}{\\sqrt{2}}"]],
            v_buff=1.3, h_buff=1.2
        ).scale(0.85)
        
        matrix_D = Matrix([[3, 0], [0, 1]]).scale(0.85)
        
        matrix_Pinv = Matrix(
            [["\\frac{1}{\\sqrt{2}}", "\\frac{1}{\\sqrt{2}}"], 
             ["-\\frac{1}{\\sqrt{2}}", "\\frac{1}{\\sqrt{2}}"]],
            v_buff=1.3, h_buff=1.2
        ).scale(0.85)

        pdp_group = VGroup(math_A2, matrix_P, matrix_D, matrix_Pinv).arrange(RIGHT, buff=0.2)
        pdp_group.next_to(step3_title, DOWN, buff=0.8)
        
        lbl_P = MathTex("P", font_size=30, color=BLUE).next_to(matrix_P, DOWN)
        lbl_D = MathTex("D", font_size=30, color=YELLOW).next_to(matrix_D, DOWN)
        lbl_Pinv = MathTex("P^{-1}", font_size=30, color=RED).next_to(matrix_Pinv, DOWN)

        # Hiệu ứng Lắp ráp có giải thích
        self.play(FadeIn(math_A2))
        
        # 1. Hiện P và dùng SurroundingRectangle đóng khung làm nổi bật từng cột
        self.play(FadeIn(matrix_P), FadeIn(lbl_P))
        col1_P = matrix_P.get_columns()[0]
        col2_P = matrix_P.get_columns()[1]
        box_v1 = SurroundingRectangle(col1_P, color=GREEN, buff=0.1)
        box_v2 = SurroundingRectangle(col2_P, color=GREEN, buff=0.1)
        note_P = Tex("Lắp từ $v_1, v_2$", tex_template=my_template, font_size=24, color=GREEN).next_to(lbl_P, DOWN, buff=0.2)
        
        self.play(Create(box_v1), Create(box_v2), Write(note_P))
        self.wait(1.5)
        self.play(FadeOut(box_v1), FadeOut(box_v2))

        # 2. Hiện D và đóng khung 2 giá trị trên đường chéo chính
        self.play(FadeIn(matrix_D), FadeIn(lbl_D))
        diag_D = VGroup(matrix_D.get_entries()[0], matrix_D.get_entries()[3]) # Vị trí 0 và 3 là đường chéo
        box_D = SurroundingRectangle(diag_D, color=ORANGE, buff=0.1)
        note_D = Tex("Lắp từ $\\lambda_1, \\lambda_2$", tex_template=my_template, font_size=24, color=ORANGE).next_to(lbl_D, DOWN, buff=0.2)
        
        self.play(Create(box_D), Write(note_D))
        self.wait(1.5)
        self.play(FadeOut(box_D))

        # 3. Hiện P_inv (Ma trận nghịch đảo)
        self.play(FadeIn(matrix_Pinv), FadeIn(lbl_Pinv))
        self.wait(1)

        # Xóa  ghi chú, lấy không gian viết kết luận
        self.play(FadeOut(note_P), FadeOut(note_D))

        connection_note = Tex(
            "Ma trận $A$ đối xứng $\\Rightarrow$ Giá trị suy biến ($\\sigma$) = Giá trị riêng ($\\lambda$)\\\\"
            "$\\sigma_1 = \\lambda_1 = 3, \\quad \\sigma_2 = \\lambda_2 = 1$", 
            tex_template=my_template, font_size=32
        )
        box = SurroundingRectangle(connection_note, color=GREEN, buff=0.3)
        conn_group = VGroup(connection_note, box).next_to(pdp_group, DOWN, buff=1.2)
        
        self.play(Write(connection_note), Create(box))
        self.wait(4)

        self.play(FadeOut(VGroup(title, step3_title, pdp_group, lbl_P, lbl_D, lbl_Pinv, conn_group)))

# CHỨNG MINH MỐI LIÊN HỆ GIỮA SVD VÀ CHÉO HÓA
class SVDConnection(Scene):
    def construct(self):
        # 1. TIÊU ĐỀ & CÔNG THỨC CHUẨN
        title = Tex("Mối liên hệ giữa SVD và Chéo hóa", tex_template=my_template, font_size=45, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        formula = MathTex("\\sigma_i = \\sqrt{\\lambda_i(A^T A)}", font_size=50, color=GREEN)
        formula.next_to(title, DOWN, buff=0.5) 
        
        formula_desc = Tex("Singular Value của $A$ bằng căn bậc hai Eigenvalue của $A^T A$", tex_template=my_template, font_size=32)

        formula_desc.next_to(formula, DOWN, buff=0.3)
        
        self.play(FadeIn(formula), FadeIn(formula_desc))
        self.wait(1.5)

        self.play(
            VGroup(formula, formula_desc).animate.scale(0.6).to_corner(UR).shift(DOWN * 1.0)
        )

        # 2. KHAI BÁO MA TRẬN A
        mat_A = Matrix([[2, 1], [1, 2]]).scale(0.7)
        eq_A = VGroup(MathTex("A = "), mat_A).arrange(RIGHT).to_edge(LEFT, buff=1).shift(UP * 1.5)
        self.play(FadeIn(eq_A))

        # Bước 1: Tính A^T A
        step1_text = Tex("1. Tính ma trận $A^T A$:", tex_template=my_template, font_size=30, color=BLUE)
        step1_text.next_to(eq_A, DOWN, buff=0.5).align_to(eq_A, LEFT)
        
        mat_ATA = Matrix([[5, 4], [4, 5]]).scale(0.7)
        eq_ATA = VGroup(
            MathTex("A^T A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} ="), 
            mat_ATA
        ).arrange(RIGHT).next_to(step1_text, RIGHT, buff=0.3)
        
        self.play(Write(step1_text))
        self.play(FadeIn(eq_ATA))
        self.wait(1.5)

        # Bước 2: Giải trị riêng của A^T A
        step2_text = Tex("2. Giải trị riêng ($\\lambda$) của $A^T A$:", tex_template=my_template, font_size=30, color=BLUE)
        step2_text.next_to(step1_text, DOWN, buff=1.2).align_to(step1_text, LEFT)
        
        eq_eig = MathTex("\\det(A^T A - \\lambda I) = 0 \\Rightarrow \\lambda^2 - 10\\lambda + 9 = 0", font_size=32).next_to(step2_text, RIGHT, buff=0.3)
        res_eig = MathTex("\\Rightarrow \\lambda_1 = 9, \\quad \\lambda_2 = 1", font_size=35, color=YELLOW).next_to(eq_eig, DOWN, buff=0.3).align_to(eq_eig, LEFT)

        self.play(Write(step2_text))
        self.play(FadeIn(eq_eig))
        self.play(Write(res_eig))
        self.wait(1.5)

        # Bước 3: Rút căn bậc hai đối chiếu SVD
        step3_text = Tex("3. Căn bậc hai ($\\sigma_i = \\sqrt{\\lambda_i}$):", tex_template=my_template, font_size=30, color=BLUE)
        step3_text.next_to(step2_text, DOWN, buff=1.5).align_to(step2_text, LEFT)
        
        res_svd = MathTex("\\sigma_1 = \\sqrt{9} = 3, \\quad \\sigma_2 = \\sqrt{1} = 1", font_size=38, color=GREEN).next_to(step3_text, RIGHT, buff=0.3)
        
        self.play(Write(step3_text))
        self.play(Write(res_svd))
        self.wait(1)

        box = SurroundingRectangle(res_svd, color=GREEN, buff=0.2)
        self.play(Create(box))
        
        final_note = Tex("Kết quả khớp chính xác với ma trận $\\Sigma = \\begin{bmatrix} 3 & 0 \\\\ 0 & 1 \\end{bmatrix}$ trong phân rã SVD!", tex_template=my_template, font_size=32, color=YELLOW)
        final_note.next_to(res_svd, DOWN, buff=0.8)
        self.play(Write(final_note))
        self.wait(3)

        self.play(FadeOut(VGroup(formula, formula_desc, eq_A, step1_text, eq_ATA, step2_text, eq_eig, res_eig, step3_text, res_svd, box, final_note)))

        # Câu hỏi chuyển 
        q_text = Tex("Tại sao lại có sự trùng hợp này? Hãy cùng xem những gì xảy ra bên dưới:", tex_template=my_template, font_size=36, color=GREEN)
        q_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(q_text))

        # Bước 1: Khởi đầu từ công thức SVD gốc
        eq1 = MathTex("A = U \\Sigma V^T")
        
        # Bước 2: Lấy công thức SVD ráp vào phép tính A^T A
        eq2 = MathTex("A^T A = (U \\Sigma V^T)^T (U \\Sigma V^T)")
        
        # Bước 3: Phá ngoặc theo luật (ABC)^T = C^T B^T A^T
        eq3 = MathTex("A^T A = V \\Sigma^T U^T U \\Sigma V^T")
        
        # Bước 4: Triệt tiêu U^T U vì U là ma trận trực giao 
        eq4 = MathTex("A^T A = V \\Sigma^2 V^T")
        note4 = Tex("(vì $U$ trực giao nên $U^T U = I$)", tex_template=my_template, font_size=28, color=GRAY)
        group4 = VGroup(eq4, note4).arrange(RIGHT, buff=0.5) 
        
        # Bước 5: Đổi V^T thành V^-1 vì V cũng là ma trận trực giao
        eq5 = MathTex("A^T A = V \\Sigma^2 V^{-1}")
        note5 = Tex("(vì $V$ trực giao nên $V^T = V^{-1}$)", tex_template=my_template, font_size=28, color=GRAY)
        group5 = VGroup(eq5, note5).arrange(RIGHT, buff=0.5)

        proof_group = VGroup(eq1, eq2, eq3, group4, group5).arrange(DOWN, buff=0.3).scale(0.9).next_to(q_text, DOWN, buff=0.3)

        self.play(FadeIn(eq1))
        self.wait(1)
        self.play(FadeIn(eq2))
        self.wait(1)
        self.play(FadeIn(eq3))
        self.wait(1)
        self.play(FadeIn(group4))
        self.wait(1)
        self.play(FadeIn(group5))
        self.wait(2)

        # CHỐT Ý
        conclusion_text = Tex(
            "Dạng $V \\Sigma^2 V^{-1}$ chính xác là dạng $P D P^{-1}$ của phép Chéo hóa!\\\\",
            "$\\Rightarrow$ SVD của ma trận $A$ thực chất là phép chéo hóa của $A^T A$.",
            tex_template=my_template, font_size=34, color=YELLOW
        )
        conclusion_box = SurroundingRectangle(conclusion_text, color=YELLOW, buff=0.2)
        
        conclusion_group = VGroup(conclusion_text, conclusion_box).next_to(proof_group, DOWN, buff=0.4)

        self.play(Write(conclusion_text), Create(conclusion_box))
        self.wait(5)

        # Xóa sạch màn hình trước khi end video
        self.play(FadeOut(Group(*self.mobjects)))

# Phần 4: Ứng dung SVD để nén ảnh trong thực tế ( dùng np.linalg.svd của thư viện numpy )
class ImageCompression(Scene):
    def construct(self):
        title = Tex("Ứng dụng thực tế: Nén ảnh (Truncated SVD)", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        try:
            # Thư viện PIL Image dùng để mở file ảnh, convert('L') chuyển ảnh thành đen trắng (Grayscale)
            img = Image.open("Rose_BlackPink.jpg").convert('L')
            img = img.resize((300, 300)) 
            img_array = np.array(img) # Chuyển ảnh thành ma trận điểm ảnh (pixels)
            h, w = img_array.shape 
            
            # Tính toán SVD cho toàn bộ ma trận ảnh gốc
            U, S, VT = np.linalg.svd(img_array, full_matrices=False)
            
            # Chuyển một ma trận số học trở lại thành một tấm ảnh để hiển thị lên Manim
            def get_image_mobject(matrix):
                matrix = np.clip(matrix, 0, 255).astype(np.uint8) # Ép giá trị điểm ảnh vào khung an toàn [0, 255]
                return ImageMobject(matrix).set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"]).scale(2)

            # Hiện ảnh gốc bên trái màn hình
            current_image = get_image_mobject(img_array).shift(LEFT * 3.5)
            img_label = Tex("Ảnh gốc ($100\\%$ dung lượng)", tex_template=my_template, font_size=30).next_to(current_image, DOWN)
            
            self.play(FadeIn(current_image), Write(img_label))
            self.wait(1)

            # Hàm tự động tạo bảng thông tin 
            def get_info_panel(k_val):
                formula = Tex(f"$A_{{{k_val}}} \\approx U_{{{k_val}}} \\Sigma_{{{k_val}}} V_{{{k_val}}}^T$", font_size=40, color=BLUE)
                
                original_size = h * w
                compressed_size = k_val * (h + w + 1)
                ratio = (compressed_size / original_size) * 100
                
                color_ratio = GREEN if ratio <= 30 else (YELLOW if ratio <= 60 else RED)

                stats = VGroup(
                    Tex(f"- Số lượng đặc trưng ($k$): {k_val}", tex_template=my_template, font_size=30),
                    Tex(f"- Dung lượng lưu trữ: {compressed_size:,} số", tex_template=my_template, font_size=30),
                    Tex(f"- Tỉ lệ so với ảnh gốc: {ratio:.1f}\\%", tex_template=my_template, font_size=30, color=color_ratio)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
                
                return VGroup(formula, stats).arrange(DOWN, buff=0.8).shift(RIGHT * 3.5)

            # List chứa các mốc k 
            k_values = [5, 20, 50, 150]
            current_panel = get_info_panel(k_values[0])
            
            # Vòng lặp duyệt qua từng mốc k để tái tạo ảnh ngày càng rõ nét hơn
            for i, k in enumerate(k_values):
                # Công thức lấy SVD cắt xén (Truncated): Chỉ lấy k cột của U, k số của Sigma, k hàng của VT
                reconstructed_matrix = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]
                new_image = get_image_mobject(reconstructed_matrix).shift(LEFT * 3.5)
                new_label = Tex(f"Ảnh khôi phục ($k={k}$)", tex_template=my_template, font_size=30, color=YELLOW).next_to(new_image, DOWN)
                
                new_panel = get_info_panel(k)

                if i == 0:
                    # Lần đầu: Thay đổi từ ảnh Gốc sang ảnh k=5 
                    self.play(
                        FadeTransform(current_image, new_image),
                        Transform(img_label, new_label),
                        Write(current_panel),
                        run_time=2
                    )
                else:
                    # Lần sau: Tăng dần k lên
                    self.play(
                        FadeTransform(current_image, new_image),
                        Transform(img_label, new_label),
                        Transform(current_panel, new_panel),
                        run_time=1.5
                    )
                
                current_image = new_image
                self.wait(1.5)

            conclusion = Tex("Chỉ với $\\sim 50\\%$ dữ liệu, mắt người đã thấy nét gần như gốc!", tex_template=my_template, font_size=20, color=GREEN)
            conclusion.next_to(current_panel, DOWN, buff=1)
            self.play(Write(conclusion))
            self.wait(3)
            # Group dùng thay cho VGroup 
            self.play(FadeOut(Group(title, current_image, img_label, current_panel, conclusion)))

        except FileNotFoundError:
            error_msg = Tex("Lỗi: Không tìm thấy file 'Rose_BlackPink.jpg'.\\\\ Vui lòng để ảnh cùng thư mục với code.", tex_template=my_template, color=RED)
            self.play(Write(error_msg))
            self.wait(3)


# PHẦN 5: TÀI LIỆU THAM KHẢO 
class References(Scene):
    def construct(self):
        title = Tex("Tài Liệu Tham Khảo", tex_template=my_template, font_size=50, color=YELLOW)
        title.to_edge(UP, buff=1)
        
        refs = VGroup(
            Tex("[1] TOÁN HỌC MUÔN NƠI. \\textit{Giới thiệu Manim | Intro Manim | Manim tutorial | ManimCE | Animation with Manim} (YouTube). 2024", tex_template=my_template, font_size=30),
            Tex("[2] Stochastic. \\textit{What is the Singular Value Decomposition?}. 2020", tex_template=my_template, font_size=30)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        refs.next_to(title, DOWN, buff=1)

        self.play(Write(title))
        self.play(FadeIn(refs, shift=UP))
        self.wait(4)
        
        thanks = Tex("Cảm ơn Thầy/Cô đã theo dõi!", tex_template=my_template, font_size=40, color=GREEN)
        thanks.next_to(refs, DOWN, buff=1.5)
        self.play(Write(thanks))
        self.wait(3)


# TỔNG KẾT SỰ KHÁC BIỆT 

class SummaryComparison(Scene):
    def construct(self):
        # 1. TIÊU ĐỀ
        title = Tex("Tổng kết: SVD vs. Chéo hóa (Về mặt hình học)", tex_template=my_template, font_size=40, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        # 2. CHUẨN BỊ KHUNG BẢNG
        divider = Line(UP * 2, DOWN * 3, color=GRAY)
        self.play(Create(divider))

        # --- THIẾT LẬP CỘT TRÁI: SVD ---
        svd_label = Tex("\\textbf{Phân rã SVD}", tex_template=my_template, font_size=36, color=GREEN).shift(LEFT * 3.5 + UP * 2)
        svd_formula = MathTex("A = U \\Sigma V^T", font_size=34).next_to(svd_label, DOWN, buff=0.5)
        
        svd_points = VGroup(
            Tex("$\\bullet$ $U, V$ luôn là phép \\textbf{Xoay}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Vector suy biến luôn \\textbf{Vuông góc}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Áp dụng cho \\textbf{Mọi loại ma trận}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Thao tác: \\textit{Xoay $\\rightarrow$ Co giãn $\\rightarrow$ Xoay}.", tex_template=my_template, font_size=28, color=GREEN_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(svd_formula, DOWN, buff=0.8)

        # --- THIẾT LẬP CỘT PHẢI: CHÉO HÓA ---
        diag_label = Tex("\\textbf{Chéo hóa}", tex_template=my_template, font_size=36, color=BLUE).shift(RIGHT * 3.5 + UP * 2)
        diag_formula = MathTex("A = P D P^{-1}", font_size=34).next_to(diag_label, DOWN, buff=0.5)
        
        diag_points = VGroup(
            Tex("$\\bullet$ $P$ thường là phép \\textbf{Bóp méo xiên}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Vector riêng \\textbf{Không nhất thiết vuông góc}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Chỉ áp dụng cho \\textbf{Ma trận vuông}.", tex_template=my_template, font_size=28),
            Tex("$\\bullet$ Thao tác: \\textit{Xiên $\\rightarrow$ Co giãn $\\rightarrow$ Trả xiên}.", tex_template=my_template, font_size=28, color=BLUE_A)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(diag_formula, DOWN, buff=0.8)

        # --- HIỆU ỨNG HIỆN TỪNG BÊN THEO LỜI NÓI ---

        # Giai đoạn 1: Nói về SVD 
        self.play(FadeIn(svd_label), Write(svd_formula))
        self.wait(1)
        for point in svd_points:
            self.play(FadeIn(point, shift=RIGHT))
            self.wait(1.5) # Khoảng nghỉ để ông lồng tiếng giải thích từng dòng

        self.wait(2) # Nghỉ một nhịp trước khi sang Chéo hóa

        # Giai đoạn 2: Nói về Chéo hóa 
        self.play(FadeIn(diag_label), Write(diag_formula))
        self.wait(1)
        for point in diag_points:
            self.play(FadeIn(point, shift=LEFT))
            self.wait(1.5)

        self.wait(2)

        # 3. KẾT LUẬN
        conclusion_text = Tex(
            "\\textbf{Kết luận: SVD là sự tổng quát hóa của Chéo hóa.}\\\\"
            "Nó giúp ta nhìn thấy cấu trúc thực sự của ma trận mà không cần quan tâm đến tính vuông góc hay đối xứng.",
            tex_template=my_template, font_size=30, color=YELLOW
        )
        
        # Thu nhỏ và đẩy bảng lên để nhường chỗ cho kết luận
        self.play(
            VGroup(svd_label, diag_label, svd_formula, diag_formula, svd_points, diag_points, divider).animate.shift(UP * 0.5).scale(0.85)
        )
        
        box = SurroundingRectangle(conclusion_text, color=YELLOW, buff=0.4)
        conclusion_group = VGroup(conclusion_text, box).to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion_text), Create(box))
        self.wait(5)

        # Xóa sạch để kết thúc video
        self.play(FadeOut(VGroup(title, svd_label, diag_label, svd_formula, diag_formula, svd_points, diag_points, divider, conclusion_group)))

# INTRO GIỚI THIỆU TÊN ĐỒ ÁN
class IntroScene(Scene):
    def construct(self):
        # Khai báo các dòng text
        course_name = Tex("Đồ án môn Toán Ứng Dụng và Thống Kê", tex_template=my_template, font_size=40, color=BLUE)
        title = Tex("\\textbf{Phân tích Giá trị Suy biến (SVD)}", tex_template=my_template, font_size=60, color=YELLOW)
        subtitle = Tex("Singular Value Decomposition", font_size=36, color=LIGHT_GREY)

        # Gom nhóm và căn lề dọc
        intro_group = VGroup(course_name, title, subtitle).arrange(DOWN, buff=0.5)

        # Hiệu ứng hiện chữ 
        self.play(FadeIn(course_name, shift=UP)) # Trượt nhẹ từ trên xuống
        self.wait(0.5)
        self.play(Write(title), run_time=1.5)    # Viết từng nét
        self.play(FadeIn(subtitle))
        self.wait(1) 

        # Xóa sạch màn hình cực ngầu để chuyển cảnh sang phần Lý thuyết
        self.play(FadeOut(intro_group, shift=DOWN)) 
        self.wait(0.5)

#  SVD VÀ CHÉO HÓA 
class SVDvsDiagAnimation(Scene):
    def construct(self):
        # 1. TIÊU ĐỀ
        title = Tex("Trực quan so sánh: Cùng một ma trận $A$, hai số phận!", tex_template=my_template, font_size=38, color=YELLOW)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title))

        # Ép tọa độ cho dòng trạng thái ở trên cùng 
        TEXT_POS = UP * 2.8
        status_text = Tex("Trạng thái: \\textbf{Không gian ban đầu ($x$)}", tex_template=my_template, font_size=30)
        status_text.move_to(TEXT_POS)

        # 2. NHÃN HAI BÊN 
        label_svd = Tex("\\textbf{SVD} ($A = U \\Sigma V^T$)", tex_template=my_template, font_size=32, color=GREEN)
        label_svd.move_to(LEFT * 3.5 + UP * 2.1)

        label_diag = Tex("\\textbf{Chéo hóa} ($A = P D P^{-1}$)", tex_template=my_template, font_size=32, color=YELLOW)
        label_diag.move_to(RIGHT * 3.5 + UP * 2.1)

        # chuẩn bị
        A_array = np.array([[1.5, 0.5], [0.0, 0.8]])

        U_mat, S_val, VT_mat = np.linalg.svd(A_array)
        Sigma_mat = np.diag(S_val)
        V_mat = VT_mat.T
        v1_svd, v2_svd = V_mat[:, 0], V_mat[:, 1]

        w, P_mat = np.linalg.eig(A_array)
        D_mat = np.diag(w)
        P_inv_mat = np.linalg.inv(P_mat)
        p1_diag, p2_diag = P_mat[:, 0], P_mat[:, 1]

        # --- SETUP HÌNH HỌC BÊN TRÁI & PHẢI  ---
        GRAPH_Y = 0.2
        
        # Nhóm SVD
        grid_svd = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], background_line_style={"stroke_opacity": 0.4})
        circle_svd = Circle(radius=1, color=GREEN).set_fill(GREEN, opacity=0.3)
        vec_v1 = Vector(v1_svd, color=RED)
        vec_v2 = Vector(v2_svd, color=RED)
        group_svd = VGroup(grid_svd, circle_svd, vec_v1, vec_v2)
        group_svd.scale(0.4).move_to(LEFT * 3.5 + UP * GRAPH_Y) 

        # Nhóm Chéo hóa
        grid_diag = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], background_line_style={"stroke_opacity": 0.4})
        circle_diag = Circle(radius=1, color=YELLOW).set_fill(YELLOW, opacity=0.3)
        vec_p1 = Vector(p1_diag, color=RED)
        vec_p2 = Vector(p2_diag, color=RED)
        group_diag = VGroup(grid_diag, circle_diag, vec_p1, vec_p2)
        group_diag.scale(0.4).move_to(RIGHT * 3.5 + UP * GRAPH_Y) 

        # MA TRẬN Ở DƯỚI CÙNG
        MAT_Y = DOWN * 3.3
        
        def get_mat_mob(prefix, mat_array):
            lbl = MathTex(prefix, font_size=28)
            m = Matrix(np.round(mat_array, 2)).scale(0.65)
            return VGroup(lbl, m).arrange(RIGHT, buff=0.2)

        current_mat_svd = get_mat_mob("I =", np.eye(2)).move_to(LEFT * 3.5 + MAT_Y)
        current_mat_diag = get_mat_mob("I =", np.eye(2)).move_to(RIGHT * 3.5 + MAT_Y)

        # Vách ngăn chia đôi màn hình 
        divider = Line(UP * 2.4, DOWN * 3.8, color=GRAY)

        # HIỆN TẤT CẢ LÊN
        self.play(
            FadeIn(divider), Write(label_svd), Write(label_diag), 
            Write(status_text), FadeIn(current_mat_svd), FadeIn(current_mat_diag)
        )
        self.play(
            Create(grid_svd), Create(circle_svd), Create(vec_v1), Create(vec_v2),
            Create(grid_diag), Create(circle_diag), Create(vec_p1), Create(vec_p2)
        )
        self.wait(2)

        self.play(
            FadeOut(vec_v1), FadeOut(vec_v2),
            FadeOut(vec_p1), FadeOut(vec_p2)
        )

        #  V^T (Xoay) vs P^-1 (Xiên) 
        step1_text = Tex("Bước 1: \\textbf{Xoay} ($V^T$) vs. \\textbf{Bóp méo xiên} ($P^{-1}$)", tex_template=my_template, font_size=30).move_to(TEXT_POS)
        new_mat_svd_1 = get_mat_mob("V^T =", VT_mat).move_to(LEFT * 3.5 + MAT_Y)
        new_mat_diag_1 = get_mat_mob("P^{-1} =", P_inv_mat).move_to(RIGHT * 3.5 + MAT_Y)

        # Dùng ReplacementTransform để sửa lỗi chồng bóng chữ
        self.play(
            ReplacementTransform(status_text, step1_text),
            ReplacementTransform(current_mat_svd, new_mat_svd_1),
            ReplacementTransform(current_mat_diag, new_mat_diag_1),
            group_svd.animate.apply_matrix(VT_mat, about_point=LEFT * 3.5 + UP * GRAPH_Y),
            group_diag.animate.apply_matrix(P_inv_mat, about_point=RIGHT * 3.5 + UP * GRAPH_Y),
            run_time=2.5
        )
        # Cập nhật lại biến hiện tại để bước sau lôi ra xài tiếp
        status_text, current_mat_svd, current_mat_diag = step1_text, new_mat_svd_1, new_mat_diag_1
        self.wait(1.5)

        # Sigma vs D (Kéo giãn)
        step2_text = Tex("Bước 2: Cùng \\textbf{Kéo giãn} ($\\Sigma$ và $D$)", tex_template=my_template, font_size=30).move_to(TEXT_POS)
        new_mat_svd_2 = get_mat_mob("\\Sigma V^T =", Sigma_mat @ VT_mat).move_to(LEFT * 3.5 + MAT_Y)
        new_mat_diag_2 = get_mat_mob("D P^{-1} =", D_mat @ P_inv_mat).move_to(RIGHT * 3.5 + MAT_Y)

        self.play(
            ReplacementTransform(status_text, step2_text),
            ReplacementTransform(current_mat_svd, new_mat_svd_2),
            ReplacementTransform(current_mat_diag, new_mat_diag_2),
            group_svd.animate.apply_matrix(Sigma_mat, about_point=LEFT * 3.5 + UP * GRAPH_Y),
            group_diag.animate.apply_matrix(D_mat, about_point=RIGHT * 3.5 + UP * GRAPH_Y),
            run_time=2.5
        )
        status_text, current_mat_svd, current_mat_diag = step2_text, new_mat_svd_2, new_mat_diag_2
        self.wait(1.5)

        # U (Xoay chốt) vs P (Trả xiên chốt)
        step3_text = Tex("Bước 3: \\textbf{Xoay đích} ($U$) vs. \\textbf{Trả về hệ quy chiếu} ($P$)", tex_template=my_template, font_size=30).move_to(TEXT_POS)
        new_mat_svd_3 = get_mat_mob("A = U \\Sigma V^T =", A_array).move_to(LEFT * 3.5 + MAT_Y)
        new_mat_diag_3 = get_mat_mob("A = P D P^{-1} =", A_array).move_to(RIGHT * 3.5 + MAT_Y)

        self.play(
            ReplacementTransform(status_text, step3_text),
            ReplacementTransform(current_mat_svd, new_mat_svd_3),
            ReplacementTransform(current_mat_diag, new_mat_diag_3),
            group_svd.animate.apply_matrix(U_mat, about_point=LEFT * 3.5 + UP * GRAPH_Y),
            group_diag.animate.apply_matrix(P_mat, about_point=RIGHT * 3.5 + UP * GRAPH_Y),
            run_time=2.5
        )
        status_text, current_mat_svd, current_mat_diag = step3_text, new_mat_svd_3, new_mat_diag_3
        self.wait(2)

        final_text = Tex("\\textbf{Kết quả:} Hai con đường khác nhau, nhưng chung một đích đến ($Ax$)!", tex_template=my_template, font_size=32, color=GREEN).move_to(TEXT_POS)
        
        self.play(ReplacementTransform(status_text, final_text))
        self.play(
            Indicate(group_svd, color=WHITE, scale_factor=1.05),
            Indicate(group_diag, color=WHITE, scale_factor=1.05),
            run_time=2
        )
        self.wait(3)

        self.play(FadeOut(Group(*self.mobjects)))