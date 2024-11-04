import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit
from sympy import symbols, Point, Line, latex, sympify

class LineDistanceCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Khoảng Cách")

        # Cấu hình các widget
        self.pointXLineEdit = QLineEdit()
        self.pointYLineEdit = QLineEdit()
        self.pointZLineEdit = QLineEdit()
        self.linePointXLineEdit = QLineEdit()
        self.linePointYLineEdit = QLineEdit()
        self.linePointZLineEdit = QLineEdit()
        self.directionXLineEdit = QLineEdit()
        self.directionYLineEdit = QLineEdit()
        self.directionZLineEdit = QLineEdit()
        self.dimensionCheckBox = QCheckBox("3D")
        self.resultTextEdit = QTextEdit()
        self.calculateButton = QPushButton("Tính Khoảng Cách")
        self.calculateButton.clicked.connect(self.calculateDistance)

        # Tạo layout
        layout = QVBoxLayout()
        pointLayout = QHBoxLayout()
        linePointLayout = QHBoxLayout()
        directionLayout = QHBoxLayout()

        # Định nghĩa label với chiều rộng cố định
        pointLabel = QLabel("Toạ Độ Điểm:")
        pointLabel.setFixedWidth(200)
        linePointLabel = QLabel("Điểm trên Đường Thẳng:")
        linePointLabel.setFixedWidth(200)
        directionLabel = QLabel("Vectơ Chỉ Phương:")
        directionLabel.setFixedWidth(200)

        # Thêm widget vào layout
        pointLayout.addWidget(pointLabel)
        pointLayout.addWidget(self.pointXLineEdit)
        pointLayout.addWidget(self.pointYLineEdit)
        pointLayout.addWidget(self.pointZLineEdit)
        linePointLayout.addWidget(linePointLabel)
        linePointLayout.addWidget(self.linePointXLineEdit)
        linePointLayout.addWidget(self.linePointYLineEdit)
        linePointLayout.addWidget(self.linePointZLineEdit)
        directionLayout.addWidget(directionLabel)
        directionLayout.addWidget(self.directionXLineEdit)
        directionLayout.addWidget(self.directionYLineEdit)
        directionLayout.addWidget(self.directionZLineEdit)

        # Thêm các layout và widget vào dialog
        layout.addLayout(pointLayout)
        layout.addLayout(linePointLayout)
        layout.addLayout(directionLayout)
        layout.addWidget(self.dimensionCheckBox)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

        # Ban đầu ẩn các trường Z
        self.pointZLineEdit.hide()
        self.linePointZLineEdit.hide()
        self.directionZLineEdit.hide()
        self.dimensionCheckBox.stateChanged.connect(self.toggleDimension)
    def toggleDimension(self, state):
        if state == 2:  # Checkbox được chọn
            self.pointZLineEdit.show()
            self.linePointZLineEdit.show()
            self.directionZLineEdit.show()
        else:
            self.pointZLineEdit.hide()
            self.linePointZLineEdit.hide()
            self.directionZLineEdit.hide()

    def calculateDistance(self):
        point_coords = [self.pointXLineEdit.text(), self.pointYLineEdit.text(), self.pointZLineEdit.text() if self.dimensionCheckBox.isChecked() else '0']
        line_point_coords = [self.linePointXLineEdit.text(), self.linePointYLineEdit.text(), self.linePointZLineEdit.text() if self.dimensionCheckBox.isChecked() else '0']
        direction_coords = [self.directionXLineEdit.text(), self.directionYLineEdit.text(), self.directionZLineEdit.text() if self.dimensionCheckBox.isChecked() else '0']

        try:
            point = Point(*sympify(point_coords))
            line_point = Point(*sympify(line_point_coords))
            line = Line(line_point, direction_ratio=sympify(direction_coords))
            distance = point.distance(line)

            result_latex = latex(distance)
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {distance}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LineDistanceCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
