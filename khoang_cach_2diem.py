import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit
from sympy import symbols, Point, sqrt, latex, sympify

class DistanceCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Khoảng Cách")

        # Định nghĩa các biến tổng quát
        self.x1, self.y1, self.z1 = symbols('x1 y1 z1')
        self.x2, self.y2, self.z2 = symbols('x2 y2 z2')

        # Cấu hình các widget
        self.point1XLineEdit = QLineEdit()
        self.point1YLineEdit = QLineEdit()
        self.point1ZLineEdit = QLineEdit()
        self.point2XLineEdit = QLineEdit()
        self.point2YLineEdit = QLineEdit()
        self.point2ZLineEdit = QLineEdit()
        self.dimensionCheckBox = QCheckBox("3D")
        self.resultTextEdit = QTextEdit()
        self.calculateButton = QPushButton("Tính Khoảng Cách")
        self.calculateButton.clicked.connect(self.calculateDistance)

        # Tạo layout
        layout = QVBoxLayout()
        formLayout = QHBoxLayout()

        # Thêm widget vào layout
        formLayout.addWidget(QLabel("Toạ Độ Điểm 1:"))
        formLayout.addWidget(self.point1XLineEdit)
        formLayout.addWidget(self.point1YLineEdit)
        formLayout.addWidget(self.point1ZLineEdit)
        formLayout.addWidget(QLabel("Toạ Độ Điểm 2:"))
        formLayout.addWidget(self.point2XLineEdit)
        formLayout.addWidget(self.point2YLineEdit)
        formLayout.addWidget(self.point2ZLineEdit)

        # Thêm các layout và widget vào dialog
        layout.addLayout(formLayout)
        layout.addWidget(self.dimensionCheckBox)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

        # Ban đầu ẩn các trường Z
        self.point1ZLineEdit.hide()
        self.point2ZLineEdit.hide()
        self.dimensionCheckBox.stateChanged.connect(self.toggleDimension)

    def toggleDimension(self, state):
        if state == 2:  # Checkbox được chọn
            self.point1ZLineEdit.show()
            self.point2ZLineEdit.show()
        else:
            self.point1ZLineEdit.hide()
            self.point2ZLineEdit.hide()

    def calculateDistance(self):
        # Sử dụng sympify để chuyển đổi chuỗi nhập vào thành các biểu thức sympy
        point1_coords = sympify([self.point1XLineEdit.text(), self.point1YLineEdit.text(), self.point1ZLineEdit.text() if self.dimensionCheckBox.isChecked() else '0'])
        point2_coords = sympify([self.point2XLineEdit.text(), self.point2YLineEdit.text(), self.point2ZLineEdit.text() if self.dimensionCheckBox.isChecked() else '0'])

        try:
            point1 = Point(*point1_coords)
            point2 = Point(*point2_coords)
            distance = sqrt(point1.distance(point2)**2).simplify()
            result_latex = latex(distance)

            formatted_result = f"<div style='color: red; font-size: 30px;'>Kết quả dạng Python:<br> {distance}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)

        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DistanceCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
