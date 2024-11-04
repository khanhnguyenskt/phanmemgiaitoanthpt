import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from sympy import symbols, integrate, sympify, latex


class AntiderivativeCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Nguyên Hàm")

        # Tạo và cấu hình các widget
        self.functionLineEdit = QLineEdit()
        self.variableLineEdit = QLineEdit()

        # Sử dụng QTextEdit thay vì QLabel
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)  # Đặt là chỉ đọc
        self.resultTextEdit.setAlignment(Qt.AlignCenter)
        self.resultTextEdit.setStyleSheet("""
            QTextEdit {
                color: red;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        self.calculateButton = QPushButton("Tính Nguyên Hàm")
        self.calculateButton.clicked.connect(self.calculateAntiderivative)

        # Tạo layout
        layout = QVBoxLayout()
        formLayout = QHBoxLayout()

        # Thêm widget vào layout
        formLayout.addWidget(QLabel("Hàm số:"))
        formLayout.addWidget(self.functionLineEdit)
        formLayout.addWidget(QLabel("Biến:"))
        formLayout.addWidget(self.variableLineEdit)

        # Thêm các layout và widget vào dialog
        layout.addLayout(formLayout)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.resultTextEdit)  # Thêm QTextEdit vào layout

        self.setLayout(layout)

    def calculateAntiderivative(self):
        function = self.functionLineEdit.text()
        variable = self.variableLineEdit.text()

        try:
            x = symbols(variable)
            expr = sympify(function)
            result = integrate(expr, x)  # Tính nguyên hàm
            result_latex = latex(result)  # Chuyển kết quả sang dạng LaTeX
            # Định dạng kết quả bằng HTML, bao gồm màu sắc và kích thước chữ
            formatted_result = f"<div style='color: red; font-size: 30px;'>Kết quả dạng Python:<br> {result}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"

            # Cập nhật QTextEdit với kết quả đã được định dạng
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setPlainText(f"Lỗi: {e}")  # Hiển thị lỗi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AntiderivativeCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
