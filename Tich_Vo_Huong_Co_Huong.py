import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit
from sympy import symbols, Matrix, cos, acos, sqrt, sympify, latex, sin, tan, cot


class VectorCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Toán Vectơ")
        # Định nghĩa các biến
        self.x1, self.y1, self.z1 = symbols('x1 y1 z1')
        self.x2, self.y2, self.z2 = symbols('x2 y2 z2')
        self.x3, self.y3, self.z3 = symbols('x3 y3 z3')
        # Cấu hình các widget
        self.vector1LineEditX = QLineEdit()
        self.vector1LineEditY = QLineEdit()
        self.vector1LineEditZ = QLineEdit()
        self.vector2LineEditX = QLineEdit()
        self.vector2LineEditY = QLineEdit()
        self.vector2LineEditZ = QLineEdit()
        self.vector3LineEditX = QLineEdit()
        self.vector3LineEditY = QLineEdit()
        self.vector3LineEditZ = QLineEdit()
        self.dimensionComboBox = QComboBox()
        self.resultTextEdit = QTextEdit()
        self.dotProductButton = QPushButton("Tích Vô Hướng")
        self.crossProductButton = QPushButton("Tích Có Hướng")
        self.crossProduc2tButton = QPushButton("Tích Hỗn Tạp")
        self.cosineButton = QPushButton("Cosin giữa vectơ 1-2 ")

        # Cấu hình sự kiện click cho mỗi nút
        self.dotProductButton.clicked.connect(self.calculateDotProduct)
        self.crossProductButton.clicked.connect(self.calculateCrossProduct)
        self.crossProduc2tButton.clicked.connect(self.calculateCrossProduct2)
        self.cosineButton.clicked.connect(self.calculateCosine)

        self.dotProductButton.setStyleSheet("background-color: #FFA07A; color: white;")  # Màu nền cam nhạt
        self.crossProduc2tButton.setStyleSheet("background-color: #90EE90; color: magenta;")  # Màu nền xanh lá  nhạt
        # Đặt màu nền cho các nút
        self.crossProductButton.setStyleSheet("background-color: #4CAF50; color: white;")
        self.cosineButton.setStyleSheet("background-color: #2196F3; color: white;")

        # Cấu hình ComboBox cho việc chọn chiều
        self.dimensionComboBox.addItem("2D")
        self.dimensionComboBox.addItem("3D")
        self.dimensionComboBox.currentIndexChanged.connect(self.toggleDimension)

        # Tạo layout
        layout = QVBoxLayout()
        formLayout1 = QHBoxLayout()
        formLayout2 = QHBoxLayout()
        formLayout3 = QHBoxLayout()

        # Thêm widget vào layout
        formLayout1.addWidget(QLabel("Vectơ 1:"))
        formLayout1.addWidget(self.vector1LineEditX)
        formLayout1.addWidget(self.vector1LineEditY)
        formLayout1.addWidget(self.vector1LineEditZ)
        formLayout2.addWidget(QLabel("Vectơ 2:"))
        formLayout2.addWidget(self.vector2LineEditX)
        formLayout2.addWidget(self.vector2LineEditY)
        formLayout2.addWidget(self.vector2LineEditZ)
        formLayout3.addWidget(QLabel("Vectơ 3:"))
        formLayout3.addWidget(self.vector3LineEditX)
        formLayout3.addWidget(self.vector3LineEditY)
        formLayout3.addWidget(self.vector3LineEditZ)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.dotProductButton)
        buttonLayout.addWidget(self.crossProductButton)
        buttonLayout.addWidget(self.crossProduc2tButton)
        buttonLayout.addWidget(self.cosineButton)

        # Thêm các layout và widget vào dialog
        layout.addLayout(formLayout1)
        layout.addLayout(formLayout2)
        layout.addLayout(formLayout3)
        layout.addWidget(self.dimensionComboBox)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

        # Mặc định ẩn trường Z
        self.toggleDimension()

    def toggleDimension(self):
        is3D = self.dimensionComboBox.currentText() == "3D"
        self.vector1LineEditZ.setVisible(is3D)
        self.vector2LineEditZ.setVisible(is3D)
        self.vector3LineEditZ.setVisible(is3D)

    def calculateDotProduct(self):
        try:
            # Kiểm tra và chuyển đổi giá trị nhập từ QLineEdit thành các biểu thức sympy
            vector1_x = sympify(self.vector1LineEditX.text() if self.vector1LineEditX.text() else '0')
            vector1_y = sympify(self.vector1LineEditY.text() if self.vector1LineEditY.text() else '0')
            vector1_z = sympify(self.vector1LineEditZ.text()) if self.dimensionComboBox.currentText() == "3D" else 0
            vector2_x = sympify(self.vector2LineEditX.text() if self.vector2LineEditX.text() else '0')
            vector2_y = sympify(self.vector2LineEditY.text() if self.vector2LineEditY.text() else '0')
            vector2_z = sympify(self.vector2LineEditZ.text()) if self.dimensionComboBox.currentText() == "3D" else 0

            # Tạo ma trận vectơ và tính tích vô hướng
            vector1 = Matrix([vector1_x, vector1_y, vector1_z])
            vector2 = Matrix([vector2_x, vector2_y, vector2_z])
            dot_product = vector1.dot(vector2)
            # Chuyển đổi kết quả sang dạng LaTeX
            result_latex = latex(dot_product)
            formatted_result = f"<div style='color: red; font-size: 25px;'>Tích vô hướng (Python): {dot_product}</div>\n<div style='color: blue; font-size: 25px;'>Tích vô hướng (LaTeX): {result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {str(e)}")

    def calculateCrossProduct(self):
        if self.dimensionComboBox.currentText() == "3D":
            try:
                # Kiểm tra và chuyển đổi giá trị nhập từ QLineEdit thành các biểu thức sympy
                vector1_x = sympify(self.vector1LineEditX.text() if self.vector1LineEditX.text() else '0')
                vector1_y = sympify(self.vector1LineEditY.text() if self.vector1LineEditY.text() else '0')
                vector1_z = sympify(self.vector1LineEditZ.text() if self.vector1LineEditZ.text() else '0')

                vector2_x = sympify(self.vector2LineEditX.text() if self.vector2LineEditX.text() else '0')
                vector2_y = sympify(self.vector2LineEditY.text() if self.vector2LineEditY.text() else '0')
                vector2_z = sympify(self.vector2LineEditZ.text() if self.vector2LineEditZ.text() else '0')

                # Tạo ma trận vectơ và tính tích có hướng
                vector1 = Matrix([vector1_x, vector1_y, vector1_z])
                vector2 = Matrix([vector2_x, vector2_y, vector2_z])
                cross_product = vector1.cross(vector2)

                # Chuyển kết quả sang dạng toạ độ
                coordinate_form = tuple(cross_product)

                # Chuyển đổi kết quả sang dạng LaTeX
                result_latex = latex(coordinate_form)
                formatted_result = f"<div style='color: red; font-size: 25px;'>Tích có hướng (Python): {coordinate_form}</div>\n<div style='color: blue; font-size: 25px;'>Tích có hướng (LaTeX): {result_latex}</div>"
                self.resultTextEdit.setHtml(formatted_result)
            except Exception as e:
                # Hiển thị thông báo lỗi nếu nhập liệu không hợp lệ
                self.resultTextEdit.setHtml(
                    f"<div style='color: red;'>Lỗi: Đã xảy ra sự cố khi xử lý đầu vào. Vui lòng kiểm tra lại đầu vào của bạn.</div>")
        else:
            self.resultTextEdit.setText("Tích có hướng chỉ áp dụng cho vectơ 3D.")
    def calculateCrossProduct2(self):
        if self.dimensionComboBox.currentText() == "3D":
            try:
                # Kiểm tra và chuyển đổi giá trị nhập từ QLineEdit thành các biểu thức sympy
                vector1_x = sympify(self.vector1LineEditX.text() if self.vector1LineEditX.text() else '0')
                vector1_y = sympify(self.vector1LineEditY.text() if self.vector1LineEditY.text() else '0')
                vector1_z = sympify(self.vector1LineEditZ.text() if self.vector1LineEditZ.text() else '0')

                vector2_x = sympify(self.vector2LineEditX.text() if self.vector2LineEditX.text() else '0')
                vector2_y = sympify(self.vector2LineEditY.text() if self.vector2LineEditY.text() else '0')
                vector2_z = sympify(self.vector2LineEditZ.text() if self.vector2LineEditZ.text() else '0')

                vector3_x = sympify(self.vector3LineEditX.text() if self.vector3LineEditX.text() else '0')
                vector3_y = sympify(self.vector3LineEditY.text() if self.vector3LineEditY.text() else '0')
                vector3_z = sympify(self.vector3LineEditZ.text() if self.vector3LineEditZ.text() else '0')

                # Tạo ma trận vectơ và tính tích có hướng
                vector1 = Matrix([vector1_x, vector1_y, vector1_z])
                vector2 = Matrix([vector2_x, vector2_y, vector2_z])
                vector3 = Matrix([vector3_x, vector3_y, vector3_z])
                cross_product = (vector1.cross(vector2)).dot(vector3)

                # Chuyển kết quả sang dạng toạ độ
                # coordinate_form = tuple(cross_product)

                # Chuyển đổi kết quả sang dạng LaTeX
                result_latex = latex(cross_product)
                formatted_result = f"<div style='color: red; font-size: 25px;'>Tích có hướng (Python): {cross_product}</div>\n<div style='color: blue; font-size: 25px;'>Tích có hướng (LaTeX): {result_latex}</div>"
                self.resultTextEdit.setHtml(formatted_result)
            except Exception as e:
                # Hiển thị thông báo lỗi nếu nhập liệu không hợp lệ
                self.resultTextEdit.setHtml(
                    f"<div style='color: red;'>Lỗi: Đã xảy ra sự cố khi xử lý đầu vào. Vui lòng kiểm tra lại đầu vào của bạn.</div>")
        else:
            self.resultTextEdit.setText("Tích có hướng chỉ áp dụng cho vectơ 3D.")

    def calculateCosine(self):
        try:
            # Tính cosin và các giá trị liên quan
            vector1 = Matrix([sympify(self.vector1LineEditX.text()if self.vector1LineEditX.text() else '0'), sympify(self.vector1LineEditY.text()if self.vector1LineEditY.text() else '0'), sympify(
                self.vector1LineEditZ.text()if self.vector1LineEditZ.text() else '0') if self.dimensionComboBox.currentText() == "3D" else 0])
            vector2 = Matrix([sympify(self.vector2LineEditX.text()if self.vector2LineEditX.text() else '0'), sympify(self.vector2LineEditY.text()if self.vector2LineEditY.text() else '0'), sympify(
                self.vector2LineEditZ.text()if self.vector2LineEditZ.text() else '0') if self.dimensionComboBox.currentText() == "3D" else 0])
            dot_product = vector1.dot(vector2)
            magnitude_vector1 = sqrt(vector1.dot(vector1))
            magnitude_vector2 = sqrt(vector2.dot(vector2))
            cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)
            angle = acos(cosine_angle)

            # Tính sin, tan, cot từ cos
            sin_angle = sin(angle)
            tan_angle = tan(angle)
            cot_angle = cot(angle)

            # Chuyển đổi kết quả sang dạng LaTeX và hiển thị
            result_latex_cos = latex(cosine_angle)
            result_latex_sin = latex(sin_angle)
            result_latex_tan = latex(tan_angle)
            result_latex_cot = latex(cot_angle)
            formatted_result = f"<div style='color: blue; font-size: 25px;'>Cos: {result_latex_cos}<br>Sin: {result_latex_sin}<br>Tan: {result_latex_tan}<br>Cot: {result_latex_cot}</div>"

            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = VectorCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())