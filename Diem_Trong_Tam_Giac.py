import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton, \
    QTextEdit, QTabWidget, QDialog
from sympy import symbols, sqrt, Eq, solve, latex, Rational, SympifyError, sympify, Point, simplify, Matrix


class SpecialPointsTab(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Các CheckBox cho 2D và 3D
        self.cb2D = QCheckBox("2D")
        self.cb3D = QCheckBox("3D")
        self.cb2D.setChecked(True)  # Mặc định là 2D

        cbLayout = QHBoxLayout()
        cbLayout.addWidget(self.cb2D)
        cbLayout.addWidget(self.cb3D)
        layout.addLayout(cbLayout)

        self.cb2D.stateChanged.connect(self.toggleDimensions)
        self.cb3D.stateChanged.connect(self.toggleDimensions)

        # Tạo QLineEdit cho ba điểm A, B, C
        self.pointEdits = {}
        for point in ['A', 'B', 'C']:
            self.pointEdits[point] = [QLineEdit() for _ in range(3)]  # X, Y, Z
            pointLayout = QHBoxLayout()
            pointLayout.addWidget(QLabel(f"Điểm {point}:"))
            for edit in self.pointEdits[point]:
                pointLayout.addWidget(edit)
            layout.addLayout(pointLayout)

        self.toggleDimensions()

        # Thêm hàng các nút cho tính toán
        buttonsLayout = QHBoxLayout()
        self.buttons = {
            "Trực Tâm": QPushButton("Trực Tâm"),
            "Tâm Nội Tiếp": QPushButton("Tâm Nội Tiếp"),
            "Tâm Ngoại Tiếp": QPushButton("Tâm Ngoại Tiếp"),
            "Chân Đường Cao Đỉnh A": QPushButton("Chân Đường Cao Đỉnh A"),
            "Chân Phân Giác Trong A": QPushButton("Chân Phân Giác Trong A"),
            "Phân Giác Ngoài A": QPushButton("Phân Giác Ngoài A")
        }
        for key, button in self.buttons.items():
            buttonsLayout.addWidget(button)
            button.clicked.connect(self.calculateSpecialPoint)

        layout.addLayout(buttonsLayout)

        # Thêm QTextEdit để hiển thị kết quả
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)
        layout.addWidget(self.resultTextEdit)
        self.buttons["Trực Tâm"].setStyleSheet("background-color: #FFA07A;")  # Màu hồng đào
        self.buttons["Tâm Nội Tiếp"].setStyleSheet("background-color: #FFD700;")  # Màu vàng đậm
        self.buttons["Tâm Ngoại Tiếp"].setStyleSheet("background-color: #00BFFF;")  # Màu xanh dương đậm
        self.buttons["Chân Đường Cao Đỉnh A"].setStyleSheet("background-color: #32CD32;")  # Màu xanh lá đậm
        self.buttons["Chân Phân Giác Trong A"].setStyleSheet("background-color: #FF69B4;")  # Màu hồng đậm
        self.buttons["Phân Giác Ngoài A"].setStyleSheet("background-color: #BA55D3;")  # Màu tím nhạt đậm

        self.setLayout(layout)

    def toggleDimensions(self):
        is3D = self.cb3D.isChecked()
        for edits in self.pointEdits.values():
            edits[2].setVisible(is3D)

        if self.sender() == self.cb2D and self.cb2D.isChecked():
            self.cb3D.setChecked(False)
        elif self.sender() == self.cb3D and self.cb3D.isChecked():
            self.cb2D.setChecked(False)

    def calcula1teSpecialPoint(self):
        # Xử lý tính toán cho từng nút được nhấn
        sender = self.sender()
        if sender == self.buttons["Trực Tâm"]:
            try:
                Ax = sympify(self.pointEdits['A'][0].text() or '0')
                Ay = sympify(self.pointEdits['A'][1].text() or '0')
                Bx = sympify(self.pointEdits['B'][0].text() or '0')
                By = sympify(self.pointEdits['B'][1].text() or '0')
                Cx = sympify(self.pointEdits['C'][0].text() or '0')
                Cy = sympify(self.pointEdits['C'][1].text() or '0')

                # Định nghĩa biến cho chân đường cao từ đỉnh A
                Hx, Hy = symbols('Hx Hy')

                # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                equation1 = Eq((Hx - Ax) * (Cx - Bx) + (Hy - Ay) * (Cy - By), 0)
                equation2 = Eq((Hx - Bx) * (Ax - Cx) + (Hy - By) * (Ay - Cy), 0)

                # Giải hệ phương trình
                solutions = solve((equation1, equation2), (Hx, Hy))
                if solutions:
                    # Xử lý trường hợp solve trả về một danh sách các giải pháp
                    if isinstance(solutions, list) and solutions:
                        solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                        Hx_sol, Hy_sol = solution[Hx], solution[Hy]
                    # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                    elif isinstance(solutions, dict):
                        Hx_sol, Hy_sol = solutions[Hx], solutions[Hy]
                    else:
                        self.resultTextEdit.setHtml(
                            "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                        return

                    # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                    Hx_latex = latex(Hx_sol)
                    Hy_latex = latex(Hy_sol)
                    formatted_result = f"Chân đường cao từ đỉnh A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                    self.resultTextEdit.setHtml(formatted_result)
                else:
                    self.resultTextEdit.setHtml(
                        "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
            except Exception as e:
                error_message = f"Lỗi: {e}"
                self.resultTextEdit.setHtml(f"<div style='color: red;'>{error_message}</div>")

        elif sender == self.buttons["Tâm Nội Tiếp"]:
            try:
                Ax = sympify(self.pointEdits['A'][0].text() or '0')
                Ay = sympify(self.pointEdits['A'][1].text() or '0')
                Bx = sympify(self.pointEdits['B'][0].text() or '0')
                By = sympify(self.pointEdits['B'][1].text() or '0')
                Cx = sympify(self.pointEdits['C'][0].text() or '0')
                Cy = sympify(self.pointEdits['C'][1].text() or '0')

                # Tạo điểm A, B, C
                A = Point(Ax, Ay)
                B = Point(Bx, By)
                C = Point(Cx, Cy)

                # Tính độ dài các cạnh
                a = B.distance(C)
                b = C.distance(A)
                c = A.distance(B)

                # Tính tọa độ tâm nội tiếp I
                Ix = (a * Ax + b * Bx + c * Cx) / (a + b + c)
                Iy = (a * Ay + b * By + c * Cy) / (a + b + c)

                # Rút gọn biểu thức
                Ix_simplified = simplify(Ix)
                Iy_simplified = simplify(Iy)

                # Chuyển đổi kết quả sang dạng LaTeX
                Ix_latex = latex(Ix_simplified)
                Iy_latex = latex(Iy_simplified)

                # Hiển thị kết quả dạng LaTeX
                formatted_result = f"Tâm nội tiếp: $\\left({Ix_latex};{Iy_latex}\\right)$"
                self.resultTextEdit.setHtml(formatted_result)

            except Exception as e:
                self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")
        elif sender == self.buttons["Chân Phân Giác Trong A"]:
            try:
                Ax = sympify(self.pointEdits['A'][0].text() or '0')
                Ay = sympify(self.pointEdits['A'][1].text() or '0')
                Bx = sympify(self.pointEdits['B'][0].text() or '0')
                By = sympify(self.pointEdits['B'][1].text() or '0')
                Cx = sympify(self.pointEdits['C'][0].text() or '0')
                Cy = sympify(self.pointEdits['C'][1].text() or '0')

                # Tạo điểm A, B, C
                A = Point(Ax, Ay)
                B = Point(Bx, By)
                C = Point(Cx, Cy)
                # Tính độ dài các cạnh
                AB = A.distance(B)
                AC = A.distance(C)
                # Tính tỉ số k
                k = AB / AC
                # Tính tọa độ chân phân giác H bằng cách lấy điểm trên đoạn BC sao cho BH/HC = k
                Hx = (Bx + k * Cx) / (1 + k)
                Hy = (By + k * Cy) / (1 + k)
                # Rút gọn biểu thức
                Hx_simplified = simplify(Hx)
                Hy_simplified = simplify(Hy)
                # Chuyển đổi kết quả sang dạng LaTeX
                Hx_latex = latex(Hx_simplified)
                Hy_latex = latex(Hy_simplified)
                # Hiển thị kết quả dạng LaTeX
                formatted_result = f"Chân phân giác trong từ đỉnh A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                self.resultTextEdit.setHtml(formatted_result)
            except Exception as e:
                self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")
        elif sender == self.buttons["Phân Giác Ngoài A"]:
            try:
                Ax = sympify(self.pointEdits['A'][0].text() or '0')
                Ay = sympify(self.pointEdits['A'][1].text() or '0')
                Bx = sympify(self.pointEdits['B'][0].text() or '0')
                By = sympify(self.pointEdits['B'][1].text() or '0')
                Cx = sympify(self.pointEdits['C'][0].text() or '0')
                Cy = sympify(self.pointEdits['C'][1].text() or '0')

                # Tạo điểm A, B, C
                A = Point(Ax, Ay)
                B = Point(Bx, By)
                C = Point(Cx, Cy)
                # Tính độ dài các cạnh
                AB = A.distance(B)
                AC = A.distance(C)
                # Tính tỉ số k
                k = AB / AC
                # Tính tọa độ chân phân giác H bằng cách lấy điểm trên đoạn BC sao cho BH/HC = k
                Hx = (Bx - k * Cx) / (1 - k)
                Hy = (By - k * Cy) / (1 - k)
                # Rút gọn biểu thức
                Hx_simplified = simplify(Hx)
                Hy_simplified = simplify(Hy)
                # Chuyển đổi kết quả sang dạng LaTeX
                Hx_latex = latex(Hx_simplified)
                Hy_latex = latex(Hy_simplified)
                # Hiển thị kết quả dạng LaTeX
                formatted_result = f"Chân phân giác trong từ đỉnh A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                self.resultTextEdit.setHtml(formatted_result)
            except Exception as e:
                self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")
        elif sender == self.buttons["Tâm Ngoại Tiếp"]:
            Ax = sympify(self.pointEdits['A'][0].text() or '0')
            Ay = sympify(self.pointEdits['A'][1].text() or '0')
            Bx = sympify(self.pointEdits['B'][0].text() or '0')
            By = sympify(self.pointEdits['B'][1].text() or '0')
            Cx = sympify(self.pointEdits['C'][0].text() or '0')
            Cy = sympify(self.pointEdits['C'][1].text() or '0')

            # Định nghĩa biến cho tâm ngoại tiếp
            x, y = symbols('x y')

            # Thiết lập phương trình IA = IB và IB = IC
            equation1 = Eq(sqrt((x - Ax) ** 2 + (y - Ay) ** 2), sqrt((x - Bx) ** 2 + (y - By) ** 2))
            equation2 = Eq(sqrt((x - Bx) ** 2 + (y - By) ** 2), sqrt((x - Cx) ** 2 + (y - Cy) ** 2))

            # Giải hệ phương trình
            solution = solve((equation1, equation2), (x, y))

            # Chuyển đổi kết quả sang dạng LaTeX
            x_latex = latex(solution[0][0])
            y_latex = latex(solution[0][1])

            # Hiển thị kết quả
            formatted_result = f"Tâm ngoại tiếp: $\\left({x_latex};{y_latex}\\right)$"
            self.resultTextEdit.setHtml(formatted_result)
        elif sender == self.buttons["Chân Đường Cao Đỉnh A"]:
            try:
                Ax = sympify(self.pointEdits['A'][0].text() or '0')
                Ay = sympify(self.pointEdits['A'][1].text() or '0')
                Bx = sympify(self.pointEdits['B'][0].text() or '0')
                By = sympify(self.pointEdits['B'][1].text() or '0')
                Cx = sympify(self.pointEdits['C'][0].text() or '0')
                Cy = sympify(self.pointEdits['C'][1].text() or '0')


                # Định nghĩa biến cho chân đường cao từ đỉnh A
                Hx, Hy = symbols('Hx Hy')

                # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                equation1 = Eq((Hx - Ax) * (Cx - Bx) + (Hy - Ay) * (Cy - By), 0)
                equation2 = Eq((Hx - Bx) * (Bx - Cx), (Hy - By) * (By - Cy))

                # Giải hệ phương trình
                solutions = solve((equation1, equation2), (Hx, Hy))
                if solutions:
                    # Xử lý trường hợp solve trả về một danh sách các giải pháp
                    if isinstance(solutions, list) and solutions:
                        solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                        Hx_sol, Hy_sol = solution[Hx], solution[Hy]
                    # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                    elif isinstance(solutions, dict):
                        Hx_sol, Hy_sol = solutions[Hx], solutions[Hy]
                    else:
                        self.resultTextEdit.setHtml(
                            "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                        return

                    # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                    Hx_latex = latex(Hx_sol)
                    Hy_latex = latex(Hy_sol)
                    formatted_result = f"Chân đường cao từ đỉnh A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                    self.resultTextEdit.setHtml(formatted_result)
                else:
                    self.resultTextEdit.setHtml(
                        "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")

            except Exception as e:
                error_message = f"Lỗi: {e}"
                self.resultTextEdit.setHtml(f"<div style='color: red;'>{error_message}</div>")

    def calculateSpecialPoint(self):
        sender = self.sender()
        is2D = self.cb2D.isChecked()
        result = ''
        # Hàm để lấy giá trị từ QLineEdit và chuyển đổi thành sympy expression
        def getValue(edit):
            return sympify(edit.text() or '0')

        # Lấy giá trị cho tất cả các điểm từ QLineEdit
        Ax, Ay, Az = getValue(self.pointEdits['A'][0]), getValue(self.pointEdits['A'][1]), 0 if is2D else getValue(
            self.pointEdits['A'][2])
        Bx, By, Bz = getValue(self.pointEdits['B'][0]), getValue(self.pointEdits['B'][1]), 0 if is2D else getValue(
            self.pointEdits['B'][2])
        Cx, Cy, Cz = getValue(self.pointEdits['C'][0]), getValue(self.pointEdits['C'][1]), 0 if is2D else getValue(
            self.pointEdits['C'][2])

        try:
            if sender == self.buttons["Chân Phân Giác Trong A"]:
                if is2D:
                    # Tạo điểm A, B, C
                    A = Point(Ax, Ay)
                    B = Point(Bx, By)
                    C = Point(Cx, Cy)
                    # Tính độ dài các cạnh
                    AB = A.distance(B)
                    AC = A.distance(C)
                    # Tính tỉ số k
                    k = AB / AC
                    # Tính tọa độ chân phân giác H bằng cách lấy điểm trên đoạn BC sao cho BH/HC = k
                    Hx = (Bx + k * Cx) / (1 + k)
                    Hy = (By + k * Cy) / (1 + k)
                    # Rút gọn biểu thức
                    Hx_simplified = simplify(Hx)
                    Hy_simplified = simplify(Hy)
                    # Chuyển đổi kết quả sang dạng LaTeX
                    Hx_latex = latex(Hx_simplified)
                    Hy_latex = latex(Hy_simplified)
                    # Hiển thị kết quả dạng LaTeX
                    result = f"Chân phân giác trong từ đỉnh A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                else:
                    # # Tạo điểm A, B, C
                    A = Point(Ax, Ay,Az)
                    B = Point(Bx, By,Bz)
                    C = Point(Cx, Cy,Cz)
                    # Tính độ dài các cạnh
                    AB = A.distance(B)
                    AC = A.distance(C)
                    # Tính tỉ số k
                    k = AB / AC
                    # Tính tọa độ chân phân giác H bằng cách lấy điểm trên đoạn BC sao cho BH/HC = k
                    Hx = (Bx + k * Cx) / (1 + k)
                    Hy = (By + k * Cy) / (1 + k)
                    Hz = (Bz + k * Cz) / (1 + k)
                    # Rút gọn biểu thức
                    Hx_simplified = simplify(Hx)
                    Hy_simplified = simplify(Hy)
                    Hz_simplified = simplify(Hz)
                    # Chuyển đổi kết quả sang dạng LaTeX
                    Hx_latex = latex(Hx_simplified)
                    Hy_latex = latex(Hy_simplified)
                    Hz_latex = latex(Hz_simplified)
                    # Hiển thị kết quả dạng LaTeX
                    result = f"Chân phân giác trong từ đỉnh A: $\\left({Hx_latex};{Hy_latex};{Hz_latex}\\right)$"
            elif sender == self.buttons["Trực Tâm"]:
                # Ví dụ: Xử lý tính toán cho Trực Tâm (tương tự cho các trường hợp khác)
                # Sử dụng phép tính 2D hoặc 3D tùy thuộc vào giá trị của is2D
                if is2D:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy = symbols('Hx Hy')
                    # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                    equation1 = Eq((Hx - Ax) * (Cx - Bx) + (Hy - Ay) * (Cy - By), 0)
                    equation2 = Eq((Hx - Bx) * (Ax - Cx) + (Hy - By) * (Ay - Cy), 0)

                    # Giải hệ phương trình
                    solutions = solve((equation1, equation2), (Hx, Hy))
                    if solutions:
                        # Xử lý trường hợp solve trả về một danh sách các giải pháp
                        if isinstance(solutions, list) and solutions:
                            solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                            Hx_sol, Hy_sol = solution[Hx], solution[Hy]
                        # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                        elif isinstance(solutions, dict):
                            Hx_sol, Hy_sol = solutions[Hx], solutions[Hy]
                        else:
                            self.resultTextEdit.setHtml(
                                "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                            return

                        # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                        Hx_latex = latex(Hx_sol)
                        Hy_latex = latex(Hy_sol)
                        result = f"Trực Tâm: $\\left({Hx_latex};{Hy_latex}\\right)$"
                        # self.resultTextEdit.setHtml(formatted_result)
                else:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy, Hz = symbols('Hx Hy Hz')
                    # Tính toán vectơ
                    AH = Matrix([Hx - Ax, Hy - Ay, Hz - Az])
                    BH = Matrix([Hx - Bx, Hy - By, Hz - Bz])
                    BC = Matrix([Cx - Bx, Cy - By, Cz - Bz])
                    AC = Matrix([Cx - Ax, Cy - Ay, Cz - Az])
                    AB = Matrix([Bx - Ax, By - Ay, Bz - Az])

                    # Phương trình 1: AH dot BC = 0
                    eq1 = Eq(AH.dot(BC), 0)

                    # Phương trình 2: BH dot AC = 0
                    eq2 = Eq(BH.dot(AC), 0)

                    # Phương trình 3: Tích hỗn tạp [AB, AC, AH] = 0
                    # Để tính tích hỗn tạp, ta dùng định thức của ma trận gồm 3 vectơ AB, AC, và AH
                    mixed_product = AB.cross(AC).dot(AH)
                    eq3 = Eq(mixed_product, 0)

                    # Giải hệ phương trình
                    solution = solve((eq1, eq2, eq3), (Hx, Hy, Hz))
                    if solution:
                        # Chuyển đổi từng giải pháp sang dạng LaTeX
                        Hx_latex = latex(solution[Hx])
                        Hy_latex = latex(solution[Hy])
                        Hz_latex = latex(solution[Hz])

                        # Tạo chuỗi LaTeX biểu diễn kết quả cuối cùng
                        result = f"Trực Tâm: $\\left({Hx_latex}; {Hy_latex}; {Hz_latex}\\right)$"

                        # Hiển thị kết quả dưới dạng LaTeX trong QTextEdit
                        self.resultTextEdit.setHtml(f"<div style='font-size: 25px;'>Kết quả: <br>{result}</div>")
                    else:
                        # Xử lý trường hợp không tìm thấy nghiệm
                        self.resultTextEdit.setHtml(
                            "<div style='font-size: 25px; color: red;'>Không thể tìm thấy giải pháp.</div>")

            # Thêm các trường hợp khác tương tự
            elif sender == self.buttons["Tâm Nội Tiếp"]:
                if is2D:
                    # Tạo điểm A, B, C
                    A = Point(Ax, Ay)
                    B = Point(Bx, By)
                    C = Point(Cx, Cy)

                    # Tính độ dài các cạnh
                    a = B.distance(C)
                    b = C.distance(A)
                    c = A.distance(B)

                    # Tính tọa độ tâm nội tiếp I
                    Ix = (a * Ax + b * Bx + c * Cx) / (a + b + c)
                    Iy = (a * Ay + b * By + c * Cy) / (a + b + c)

                    # Rút gọn biểu thức
                    Ix_simplified = simplify(Ix)
                    Iy_simplified = simplify(Iy)

                    # Chuyển đổi kết quả sang dạng LaTeX
                    Ix_latex = latex(Ix_simplified)
                    Iy_latex = latex(Iy_simplified)

                    # Hiển thị kết quả dạng LaTeX
                    result = f"$\\left({Ix_latex};{Iy_latex}\\right)$"
                    # self.resultTextEdit.setHtml(formatted_result)
                else:
                    # Tạo điểm A, B, C
                    A = Point(Ax, Ay,Az)
                    B = Point(Bx, By,Bz)
                    C = Point(Cx, Cy,Cz)

                    # Tính độ dài các cạnh
                    a = B.distance(C)
                    b = C.distance(A)
                    c = A.distance(B)

                    # Tính tọa độ tâm nội tiếp I
                    Ix = (a * Ax + b * Bx + c * Cx) / (a + b + c)
                    Iy = (a * Ay + b * By + c * Cy) / (a + b + c)
                    Iz = (a * Az + b * Bz + c * Cz) / (a + b + c)

                    # Rút gọn biểu thức
                    Ix_simplified = simplify(Ix)
                    Iy_simplified = simplify(Iy)
                    Iz_simplified = simplify(Iz)

                    # Chuyển đổi kết quả sang dạng LaTeX
                    Ix_latex = latex(Ix_simplified)
                    Iy_latex = latex(Iy_simplified)
                    Iz_latex = latex(Iz_simplified)

                    # Hiển thị kết quả dạng LaTeX
                    result = f"$\\left({Ix_latex};{Iy_latex};{Iz_latex}\\right)$"
                    # self.resultTextEdit.setHtml(formatted_result)
            # Hiển thị kết quả (Giả sử 'result' là kết quả của tính toán)
            elif sender == self.buttons["Phân Giác Ngoài A"]:
                if is2D:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy = symbols('Hx Hy')
                    # Tạo điểm A, B, C
                    A = Point(Ax, Ay)
                    B = Point(Bx, By)
                    C = Point(Cx, Cy)
                    # Tính độ dài các cạnh
                    AB = A.distance(B)
                    AC = A.distance(C)
                    # Tính tỉ số k
                    k = AB / AC
                    # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                    equation1 = Eq((Hx - Bx),k*(Hx - Cx))
                    equation2 = Eq((Hy - By),k*(Hy - Cy))
                    # Giải hệ phương trình
                    solutions = solve((equation1, equation2), (Hx, Hy))
                    if solutions:
                        # Xử lý trường hợp solve trả về một danh sách các giải pháp
                        if isinstance(solutions, list) and solutions:
                            solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                            Hx_sol, Hy_sol = solution[Hx], solution[Hy]
                        # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                        elif isinstance(solutions, dict):
                            Hx_sol, Hy_sol = solutions[Hx], solutions[Hy]
                        else:
                            self.resultTextEdit.setHtml(
                                "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                            return
                        # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                        Hx_latex = latex(Hx_sol)
                        Hy_latex = latex(Hy_sol)
                        # Hiển thị kết quả dạng LaTeX
                        result = f"Chân phân giác ngoài góc A: $\\left({Hx_latex};{Hy_latex}\\right)$"
                else:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy, Hz = symbols('Hx Hy Hz')
                    # Tạo điểm A, B, C
                    A = Point(Ax, Ay, Az)
                    B = Point(Bx, By, Bz)
                    C = Point(Cx, Cy, Cz)
                    # Tính độ dài các cạnh
                    AB = A.distance(B)
                    AC = A.distance(C)
                    # Tính tỉ số k
                    k = AB / AC
                    # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                    equation1 = Eq((Hx - Bx), k * (Hx - Cx))
                    equation2 = Eq((Hy - By), k * (Hy - Cy))
                    equation3 = Eq((Hz - Bz), k * (Hz - Cz))
                    # Giải hệ phương trình
                    solutions = solve((equation1, equation2,equation3), (Hx, Hy,Hz))
                    if solutions:
                        # Xử lý trường hợp solve trả về một danh sách các giải pháp
                        if isinstance(solutions, list) and solutions:
                            solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                            Hx_sol, Hy_sol, Hz_sol = solution[Hx], solution[Hy], solution[Hz]
                        # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                        elif isinstance(solutions, dict):
                            Hx_sol, Hy_sol,Hz_sol = solutions[Hx], solutions[Hy], solutions[Hz]
                        else:
                            self.resultTextEdit.setHtml(
                                "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                            return
                        # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                        Hx_latex = latex(Hx_sol)
                        Hy_latex = latex(Hy_sol)
                        Hz_latex = latex(Hz_sol)
                        # Hiển thị kết quả dạng LaTeX
                        result = f"Chân phân giác ngoài góc A: $\\left({Hx_latex};{Hy_latex};{Hz_latex}\\right)$"
            elif sender == self.buttons["Tâm Ngoại Tiếp"]:
                if is2D:
                    x, y = symbols('x y')
                    # Thiết lập phương trình IA = IB và IB = IC
                    equation1 = Eq(sqrt((x - Ax) ** 2 + (y - Ay) ** 2), sqrt((x - Bx) ** 2 + (y - By) ** 2))
                    equation2 = Eq(sqrt((x - Bx) ** 2 + (y - By) ** 2), sqrt((x - Cx) ** 2 + (y - Cy) ** 2))

                    # Giải hệ phương trình
                    solution = solve((equation1, equation2), (x, y))

                    # Chuyển đổi kết quả sang dạng LaTeX
                    x_latex = latex(solution[0][0])
                    y_latex = latex(solution[0][1])

                    # Hiển thị kết quả
                    result = f"Tâm ngoại tiếp: $\\left({x_latex};{y_latex}\\right)$"
                    # self.resultTextEdit.setHtml(formatted_result)
                else:

                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy, Hz = symbols('Hx Hy Hz')
                    # Tính toán vectơ
                    AH = Matrix([Hx - Ax, Hy - Ay, Hz - Az])
                    AC = Matrix([Cx - Ax, Cy - Ay, Cz - Az])
                    AB = Matrix([Bx - Ax, By - Ay, Bz - Az])

                    # Phương trình 3: Tích hỗn tạp [AB, AC, AH] = 0
                    # Để tính tích hỗn tạp, ta dùng định thức của ma trận gồm 3 vectơ AB, AC, và AH
                    mixed_product = AB.cross(AC).dot(AH)
                    eq3 = Eq(mixed_product, 0)

                    # Thiết lập phương trình IA = IB và IB = IC
                    equation1 = Eq(sqrt((Hx - Ax) ** 2 + (Hy - Ay) ** 2+ (Hz - Az) ** 2), sqrt((Hx - Bx) ** 2 + (Hy - By) ** 2+ (Hz - Bz) ** 2))
                    equation2 = Eq(sqrt((Hx - Bx) ** 2 + (Hy - By) ** 2+ (Hz - Bz) ** 2), sqrt((Hx - Cx) ** 2 + (Hy - Cy) ** 2+ (Hz - Cz) ** 2))

                    # Giải hệ phương trình
                    solution = solve((equation1, equation2,eq3), (Hx, Hy,Hz))

                    # Chuyển đổi kết quả sang dạng LaTeX
                    x_latex = latex(solution[0][0])
                    y_latex = latex(solution[0][1])
                    z_latex = latex(solution[0][2])

                    # Hiển thị kết quả
                    result = f"Tâm ngoại tiếp: $\\left({x_latex};{y_latex};{z_latex}\\right)$"
                    # self.resultTextEdit.setHtml(formatted_result)
            elif sender == self.buttons["Chân Đường Cao Đỉnh A"]:
                if is2D:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy = symbols('Hx Hy')
                    # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                    equation1 = Eq((Hx - Ax) * (Cx - Bx) + (Hy - Ay) * (Cy - By), 0)
                    equation2 = Eq((Hx - Bx) * (By - Cy), (Hy - By) * (Bx - Cx))
                    # Giải hệ phương trình
                    solutions = solve((equation1, equation2), (Hx, Hy))
                    if solutions:
                        # Xử lý trường hợp solve trả về một danh sách các giải pháp
                        if isinstance(solutions, list) and solutions:
                            solution = solutions[0]  # Giả sử giải pháp đầu tiên là giải pháp hợp lệ
                            Hx_sol, Hy_sol = solution[Hx], solution[Hy]
                        # Xử lý trường hợp solve trả về một giải pháp duy nhất trong một dictionary
                        elif isinstance(solutions, dict):
                            Hx_sol, Hy_sol = solutions[Hx], solutions[Hy]
                        else:
                            self.resultTextEdit.setHtml(
                                "<div style='color: red;'>Không tìm được chân đường cao từ đỉnh A.</div>")
                            return
                        # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
                        Hx_latex = latex(Hx_sol)
                        Hy_latex = latex(Hy_sol)
                        result = f"$Chân đường cao kẻ từ đỉnh A là \\n \\left({Hx_latex};{Hy_latex}\\right)$"
                else:
                    # Định nghĩa biến cho chân đường cao từ đỉnh A
                    Hx, Hy, Hz, t = symbols('Hx Hy Hz t')
                    # Thiết lập phương trình AH * BC = 0 và BH, BC cùng phương
                    equation1 = Eq((Hx - Ax) * (Cx - Bx) + (Hy - Ay) * (Cy - By)+ (Hz - Az) * (Cz - Bz), 0)
                    equation2 = Eq((Hx - Bx) , t*(Bx - Cx))
                    equation3 = Eq((Hy - By) , t*(By - Cy))
                    equation4 = Eq((Hz - Bz) , t*(Bz - Cz))
                    # Giải hệ phương trình
                    solutions = solve((equation1, equation2,equation3, equation4), (Hx, Hy, Hz, t))
                    if solutions:
                        if isinstance(solutions, dict):
                            Hx_sol, Hy_sol, Hz_sol = solutions[Hx], solutions[Hy], solutions[Hz]
                        else:
                            Hx_sol, Hy_sol, Hz_sol = solutions[0][0], solutions[0][1], solutions[0][2]

                        x_latex = latex(Hx_sol)
                        y_latex = latex(Hy_sol)
                        z_latex = latex(Hz_sol)
                        result = f"Chân đường cao kể từ A: $\\left({x_latex};{y_latex};{z_latex}\\right)$"
                    else:
                        result = "Không tìm thấy giải pháp."

            if result:
                # self.resultTextEdit.setHtml(f"<div style='color: blue;'>Kết quả: <br>{result}</div>")
                self.resultTextEdit.setHtml(f"<div style='color: blue; font-size: 30px;'>Kết quả: <br>{result}</div>")

            else:
                self.resultTextEdit.setHtml("<div style='color: red; font-size: 25px;'>Không thể có kết quả vì tam giác ABC cân tại A kết quả.</div>")

        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     specialPointsTab = SpecialPointsTab()
#     specialPointsTab.show()
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication([])
    dialog = SpecialPointsTab()
    dialog.show()
    app.exec_()