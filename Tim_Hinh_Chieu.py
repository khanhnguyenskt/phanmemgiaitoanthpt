import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit
from sympy import symbols, Matrix, solve, sympify, latex, Rational

class ProjectionCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Toán Hình Chiếu")
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        # Layout cho nhập điểm với QLabel canh hàng
        pointLayout = QHBoxLayout()
        pointLabel = QLabel("Điểm P(x,y,z):")
        pointLabel.setFixedWidth(500)  # Thiết lập độ rộng cố định là 150 pixels
        pointLayout.addWidget(pointLabel)
        self.pointXLineEdit = QLineEdit()
        self.pointYLineEdit = QLineEdit()
        self.pointZLineEdit = QLineEdit()
        pointLayout.addWidget(self.pointXLineEdit)
        pointLayout.addWidget(self.pointYLineEdit)
        pointLayout.addWidget(self.pointZLineEdit)
        mainLayout.addLayout(pointLayout)

        # Layout cho nhập đường thẳng với QLabel canh hàng
        lineLayout = QHBoxLayout()
        lineLabel = QLabel("Đường Thẳng qua A(x,y,z), VTCP:")
        lineLabel.setFixedWidth(500)  # Thiết lập độ rộng cố định là 150 pixels
        lineLayout.addWidget(lineLabel)
        self.linePointXLineEdit = QLineEdit()
        self.linePointYLineEdit = QLineEdit()
        self.linePointZLineEdit = QLineEdit()
        self.lineDirectionXLineEdit = QLineEdit()
        self.lineDirectionYLineEdit = QLineEdit()
        self.lineDirectionZLineEdit = QLineEdit()
        lineLayout.addWidget(self.linePointXLineEdit)
        lineLayout.addWidget(self.linePointYLineEdit)
        lineLayout.addWidget(self.linePointZLineEdit)
        lineLayout.addWidget(self.lineDirectionXLineEdit)
        lineLayout.addWidget(self.lineDirectionYLineEdit)
        lineLayout.addWidget(self.lineDirectionZLineEdit)
        mainLayout.addLayout(lineLayout)

        # Layout cho mặt phẳng với QLabel canh hàng
        self.planeLayout = QHBoxLayout()
        planeLabel = QLabel("Mặt phẳng (A.x + B.y + C.z + D = 0):")
        planeLabel.setFixedWidth(500)  # Thiết lập độ rộng cố định là 150 pixels
        self.planeLayout.addWidget(planeLabel)
        self.aLineEdit = QLineEdit()
        self.bLineEdit = QLineEdit()
        self.cLineEdit = QLineEdit()
        self.dLineEdit = QLineEdit()
        self.planeLayout.addWidget(self.aLineEdit)
        self.planeLayout.addWidget(self.bLineEdit)
        self.planeLayout.addWidget(self.cLineEdit)
        self.planeLayout.addWidget(self.dLineEdit)
        mainLayout.addLayout(self.planeLayout)

        # Layout cho các nút bấm, đặt cùng hàng và tô màu
        buttonLayout = QHBoxLayout()
        self.projectionLineButton = QPushButton("Hình Chiếu lên Đường Thẳng")
        self.projectionLineButton.setStyleSheet("background-color: lightblue;")
        buttonLayout.addWidget(self.projectionLineButton)

        self.projectionPlaneButton = QPushButton("Hình Chiếu lên Mặt Phẳng")
        self.projectionPlaneButton.setStyleSheet("background-color: lightgreen;")
        buttonLayout.addWidget(self.projectionPlaneButton)
        mainLayout.addLayout(buttonLayout)

        # ComboBox cho việc chọn giữa 2D và 3D
        self.dimensionComboBox = QComboBox()
        self.dimensionComboBox.addItems(["2D", "3D"])
        self.dimensionComboBox.currentIndexChanged.connect(self.toggleDimension)
        mainLayout.addWidget(self.dimensionComboBox)

        # TextEdit để hiển thị kết quả
        self.resultTextEdit = QTextEdit()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.resultTextEdit)

        self.setLayout(mainLayout)

        self.projectionLineButton.clicked.connect(self.calculateProjectionOnLine)
        self.projectionPlaneButton.clicked.connect(self.calculateProjectionOnPlane)

        self.toggleDimension()  # Khởi tạo với việc ẩn các trường của mặt phẳng

    def toggleDimension(self):
        is3D = self.dimensionComboBox.currentText() == "3D"
        self.pointZLineEdit.setVisible(is3D)
        self.linePointZLineEdit.setVisible(is3D)
        self.lineDirectionZLineEdit.setVisible(is3D)
        self.togglePlaneFields(is3D)  # Hiển thị hoặc ẩn các trường mặt phẳng

    def togglePlaneFields(self, show):
        # Hiển thị hoặc ẩn các trường nhập liệu cho mặt phẳng
        self.aLineEdit.setVisible(show)
        self.bLineEdit.setVisible(show)
        self.cLineEdit.setVisible(show)
        self.dLineEdit.setVisible(show)
        self.projectionPlaneButton.setVisible(show)

    def calculateProjectionOnPlane(self):
        try:
            # Lấy giá trị nhập vào và sử dụng Rational để giữ giá trị dưới dạng phân số
            px_val, py_val, pz_val = sympify(self.pointXLineEdit.text() or '0'), sympify(
                self.pointYLineEdit.text() or '0'), sympify(self.pointZLineEdit.text() or '0')
            a_val, b_val, c_val, d_val = Rational(self.aLineEdit.text() or '0'), Rational(
                self.bLineEdit.text() or '0'), Rational(self.cLineEdit.text() or '0'), Rational(
                self.dLineEdit.text() or '0')

            # Tạo vectơ pháp tuyến của mặt phẳng
            n_vector = Matrix([a_val, b_val, c_val])

            # Tính hình chiếu
            from sympy.abc import t
            p_vector = Matrix([px_val, py_val, pz_val])
            d_vector = n_vector  # Đường thẳng đi qua P và vuông góc với mặt phẳng
            line_eq = p_vector + t * d_vector  # Phương trình đường thẳng
            solutions = solve(a_val * line_eq[0] + b_val * line_eq[1] + c_val * line_eq[2] + d_val, t)

            if not solutions:
                raise ValueError("Không tìm thấy hình chiếu lên mặt phẳng.")

            # Tính tọa độ giao điểm
            projection_point = line_eq.subs(t, solutions[0])
            projection_tuple = tuple(projection_point)  # Chuyển Matrix thành tuple

            # Tạo biểu thức LaTeX từ tuple
            result_latex = '\\left(' + ', '.join(latex(elm) for elm in projection_tuple) + '\\right)'  # Tạo chuỗi LaTeX cho tuple

            # Hiển thị kết quả
            result_python = "Hình chiếu lên mặt phẳng (Python): {}".format(projection_tuple)
            self.resultTextEdit.setHtml(
                f"<div style='color: green; font-size: 30px;'>{result_python}<br>Hình chiếu (LaTeX):<br> {result_latex}</div>")
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red; font-size: 20px;'>Lỗi: {str(e)}</div>")

    def toggle1Dimension(self):
        is3D = self.dimensionComboBox.currentText() == "3D"
        self.pointZLineEdit.setVisible(is3D)
        self.linePointZLineEdit.setVisible(is3D)
        self.lineDirectionZLineEdit.setVisible(is3D)

    def calculateProjectionOnLine(self):
        try:
            # Lấy giá trị đã nhập và chuyển chúng thành các biểu thức sympy
            px_val, py_val, pz_val = sympify(self.pointXLineEdit.text() or '0'), sympify(
                self.pointYLineEdit.text() or '0'), sympify(self.pointZLineEdit.text() or '0')
            lx_val, ly_val, lz_val = sympify(self.lineDirectionXLineEdit.text() or '0'), sympify(
                self.lineDirectionYLineEdit.text() or '0'), sympify(self.lineDirectionZLineEdit.text() or '0')
            ax_val, ay_val, az_val = sympify(self.linePointXLineEdit.text() or '0'), sympify(
                self.linePointYLineEdit.text() or '0'), sympify(self.linePointZLineEdit.text() or '0')

            # Tính toán hình chiếu
            ap_vector = Matrix([px_val - ax_val, py_val - ay_val, pz_val - az_val])
            l_vector = Matrix([lx_val, ly_val, lz_val])
            projection_scalar = ap_vector.dot(l_vector) / l_vector.dot(l_vector)
            projection_point = Matrix([ax_val, ay_val, az_val]) + projection_scalar * l_vector

            # Tạo tuple từ kết quả hình chiếu
            projection_tuple = tuple(projection_point)

            # Chỉ sử dụng X và Y nếu ở chế độ 2D
            if self.dimensionComboBox.currentText() == "2D":
                projection_tuple = projection_tuple[:2]

            # Tạo biểu thức LaTeX từ tuple
            result_latex = '(' + ', '.join(latex(i) for i in projection_tuple) + ')'

            # Hiển thị kết quả
            result_python = f"Hình chiếu (Python): {projection_tuple}"
            self.resultTextEdit.setHtml(
                f"<div style='color: green; font-size: 25px;'><br>{result_python}<br>Hình chiếu (LaTeX): <br>{result_latex}</div>")
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red; font-size: 20px;'>Lỗi: {str(e)}</div>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectionCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
