import sys

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from sympy import symbols, limit, sympify, oo, latex

class LimitCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Giới Hạn")

        self.functionLineEdit = QLineEdit()
        self.variableLineEdit = QLineEdit()
        self.pointLineEdit = QLineEdit()
        self.directionComboBox = QComboBox()
        self.resultTextEdit = QTextEdit()
        self.calculateButton = QPushButton("Tính Giới Hạn")

        self.directionComboBox.addItem("Hai Phía", None)
        self.directionComboBox.addItem("Bên Phải", '+')
        self.directionComboBox.addItem("Bên Trái", '-')

        self.calculateButton.clicked.connect(self.calculateLimit)

        layout = QVBoxLayout()
        formLayout = QHBoxLayout()

        formLayout.addWidget(QLabel("Hàm số:"))
        formLayout.addWidget(self.functionLineEdit)
        formLayout.addWidget(QLabel("Biến:"))
        formLayout.addWidget(self.variableLineEdit)
        formLayout.addWidget(QLabel("Tại điểm:"))
        formLayout.addWidget(self.pointLineEdit)
        formLayout.addWidget(QLabel("Hướng:"))
        formLayout.addWidget(self.directionComboBox)
        # Đặt chiều rộng lớn hơn cho QLineEdit của hàm số
        self.functionLineEdit.setFixedWidth(500)  # Giả sử bạn muốn chiều rộng là 300px

        # Đặt chiều rộng nhỏ hơn cho QLineEdit của biến và điểm
        self.variableLineEdit.setFixedWidth(100)  # Giả sử bạn muốn chiều rộng là 50px
        self.pointLineEdit.setFixedWidth(100)  # Tương tự như trên

        layout.addLayout(formLayout)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def calculateLimit(self):
        function = self.functionLineEdit.text()
        variable = symbols(self.variableLineEdit.text())
        point = self.pointLineEdit.text().replace('oo', 'oo')
        direction = self.directionComboBox.currentText()  # Lấy văn bản hiện tại từ ComboBox

        if point == 'oo':
            point = oo
        elif point == '-oo':
            point = -oo
        else:
            point = sympify(point)

        try:
            if direction == "Hai Phía":
                limit_plus = limit(sympify(function), variable, point, dir='+')
                limit_minus = limit(sympify(function), variable, point, dir='-')
                if limit_plus == limit_minus:
                    result = limit_plus  # Giới hạn tồn tại và giống nhau từ cả hai phía
                else:
                    result = "Không tồn tại"  # Giới hạn không tồn tại do khác biệt giữa hai phía
            else:
                dir_symbol = '+' if direction == "Bên Phải" else '-'
                result = limit(sympify(function), variable, point, dir=dir_symbol)

            # Định dạng và hiển thị kết quả
            if result == "Không tồn tại":
                formatted_result = "<div style='color: red; font-size: 30px;'>Giới hạn không tồn tại do sự khác biệt giữa giới hạn từ phía dương và phía âm.</div>"
            else:
                result_latex = latex(result)
                formatted_result = f"<div style='color: blue; font-size: 30px;'>Kết quả: {result}</div><div style='color: red; font-size: 30px;'>Kết quả: {result_latex}</div>"

            self.resultTextEdit.setHtml(formatted_result)

        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LimitCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
