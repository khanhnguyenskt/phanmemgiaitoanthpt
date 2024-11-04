import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from sympy import symbols, diff, latex, sympify

class DerivativeCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Đạo Hàm")

        # Tạo và cấu hình các widget
        self.functionLineEdit = QLineEdit()
        self.variableLineEdit = QLineEdit()

        # Sử dụng QTextEdit để hiển thị kết quả dưới dạng mã LaTeX
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)  # Chỉ cho phép đọc, không cho phép chỉnh sửa
        self.resultTextEdit.setPlainText("Kết quả LaTeX: Chưa có")  # Sử dụng setPlainText() thay vì setText() cho QTextEdit

        self.calculateButton = QPushButton("Tính Đạo Hàm")
        self.calculateButton.clicked.connect(self.calculateDerivative)

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

    def calculateDerivative(self):
        function = self.functionLineEdit.text()
        variable = self.variableLineEdit.text()

        try:
            x = symbols(variable)
            expr = sympify(function)
            result = diff(expr, x)  # Tính đạo hàm
            result_latex = latex(result)  # Chuyển kết quả sang mã LaTeX

            # Định dạng kết quả bằng HTML, bao gồm màu sắc và kích thước chữ
            formatted_result = f"<div style='color: red; font-size: 30px;'>Kết quả dạng Python:<br> {result}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"

            # Cập nhật QTextEdit với kết quả đã được định dạng
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            error_message = f"<div style='color: red; font-size: 20px;'>Lỗi: {e}</div>"
            self.resultTextEdit.setHtml(error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DerivativeCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
