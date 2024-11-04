import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit
from sympy import symbols, Point3D, Line3D, sympify, latex, sqrt, Matrix


import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from sympy import symbols, Point3D, Line3D, sympify, latex, sqrt, Matrix

class Lines3DDistanceCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Khoảng Cách Giữa Hai Đường Thẳng")

        # Định nghĩa các biến tổng quát
        self.x1, self.y1, self.z1 = symbols('x1 y1 z1')
        self.dx1, self.dy1, self.dz1 = symbols('dx1 dy1 dz1')
        self.x2, self.y2, self.z2 = symbols('x2 y2 z2')
        self.dx2, self.dy2, self.dz2 = symbols('dx2 dy2 dz2')

        # Cấu hình các widget
        self.line1PointXLineEdit = QLineEdit()
        self.line1PointYLineEdit = QLineEdit()
        self.line1PointZLineEdit = QLineEdit()
        self.line1DirectionXLineEdit = QLineEdit()
        self.line1DirectionYLineEdit = QLineEdit()
        self.line1DirectionZLineEdit = QLineEdit()
        self.line2PointXLineEdit = QLineEdit()
        self.line2PointYLineEdit = QLineEdit()
        self.line2PointZLineEdit = QLineEdit()
        self.line2DirectionXLineEdit = QLineEdit()
        self.line2DirectionYLineEdit = QLineEdit()
        self.line2DirectionZLineEdit = QLineEdit()
        self.resultTextEdit = QTextEdit()
        self.calculateButton = QPushButton("Tính Khoảng Cách")
        self.calculateButton.clicked.connect(self.calculateDistance)

        # Tạo layout chính
        mainLayout = QVBoxLayout()

        # Tạo QGridLayout cho các dòng
        gridLayout = QGridLayout()

        # Thêm widget vào gridLayout
        gridLayout.addWidget(QLabel("Điểm Trên Đường Thẳng 1:"), 0, 0)
        gridLayout.addWidget(self.line1PointXLineEdit, 0, 1)
        gridLayout.addWidget(self.line1PointYLineEdit, 0, 2)
        gridLayout.addWidget(self.line1PointZLineEdit, 0, 3)

        gridLayout.addWidget(QLabel("VTCP Đường Thẳng 1:"), 1, 0)
        gridLayout.addWidget(self.line1DirectionXLineEdit, 1, 1)
        gridLayout.addWidget(self.line1DirectionYLineEdit, 1, 2)
        gridLayout.addWidget(self.line1DirectionZLineEdit, 1, 3)

        gridLayout.addWidget(QLabel("Điểm Trên Đường Thẳng 2:"), 2, 0)
        gridLayout.addWidget(self.line2PointXLineEdit, 2, 1)
        gridLayout.addWidget(self.line2PointYLineEdit, 2, 2)
        gridLayout.addWidget(self.line2PointZLineEdit, 2, 3)

        gridLayout.addWidget(QLabel("VTCP Đường Thẳng 2:"), 3, 0)
        gridLayout.addWidget(self.line2DirectionXLineEdit, 3, 1)
        gridLayout.addWidget(self.line2DirectionYLineEdit, 3, 2)
        gridLayout.addWidget(self.line2DirectionZLineEdit, 3, 3)

        # Thêm gridLayout và các widget còn lại vào mainLayout
        mainLayout.addLayout(gridLayout)
        mainLayout.addWidget(self.calculateButton)
        mainLayout.addWidget(self.resultTextEdit)

        self.setLayout(mainLayout)

    def calculateDistance(self):
        # Chuyển đổi input từ người dùng thành các biểu thức sympy
        point1 = Matrix(sympify(
            [self.line1PointXLineEdit.text(), self.line1PointYLineEdit.text(), self.line1PointZLineEdit.text()]))
        direction1 = Matrix(sympify([self.line1DirectionXLineEdit.text(), self.line1DirectionYLineEdit.text(),
                                     self.line1DirectionZLineEdit.text()]))
        point2 = Matrix(sympify(
            [self.line2PointXLineEdit.text(), self.line2PointYLineEdit.text(), self.line2PointZLineEdit.text()]))
        direction2 = Matrix(sympify([self.line2DirectionXLineEdit.text(), self.line2DirectionYLineEdit.text(),
                                     self.line2DirectionZLineEdit.text()]))

        try:
            # Tính vectơ chéo (cross product) của hai vectơ chỉ phương
            cross_product = direction1.cross(direction2)
            # Tính khoảng cách giữa hai đường thẳng dựa trên công thức
            numerator = (point1 - point2).dot(cross_product)
            denominator = sqrt(cross_product.dot(cross_product))
            distance = abs(numerator) / denominator

            # Xuất kết quả dạng số và LaTeX
            distance_eval = distance.evalf()
            distance_latex = latex(distance)
            # result_text = f"Khoảng cách: {distance_eval}\nLaTeX: {distance_latex}"
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {distance_eval}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{distance_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
            # self.resultTextEdit.setText(result_text)

        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Lines3DDistanceCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
