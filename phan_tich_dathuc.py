import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from sympy import symbols, factor, expand, sympify, factorint, latex, div


class PolynomialOperationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phép toán Đa thức và Phân tích Số")
        self.setMinimumWidth(800)
        # Khung nhập đa thức hoặc số
        self.inputLineEdit = QLineEdit()
        self.resultTextEdit = QTextEdit()

        # Các nút cho các phép toán khác nhau
        self.factorButton = QPushButton("Phân Tích Đa thức")
        self.expandButton = QPushButton("Khai Triển Đa thức")
        self.simplifyButton = QPushButton("Phân Tích Nhân Tử")
        self.factorIntButton = QPushButton("Phân tích Số")
        self.divideButton = QPushButton("Chia Đa thức")
        self.divideButton.setStyleSheet(
            "QPushButton { background-color: #33D1FF; border-radius: 5px; min-height: 60px; max-height: 60px; }")
        self.divideButton.clicked.connect(self.dividePolynomial)

        # Đặt màu nền cho mỗi nút
        # Đặt màu nền và chiều cao cố định cho mỗi nút
        self.factorButton.setStyleSheet(
            "QPushButton { background-color: #FF5733; border-radius: 5px; min-height: 60px; max-height: 60px; }")
        self.expandButton.setStyleSheet(
            "QPushButton { background-color: #33CFFF; border-radius: 5px; min-height: 60px; max-height: 60px; }")
        self.simplifyButton.setStyleSheet(
            "QPushButton { background-color: #75CF33; border-radius: 5px; min-height: 60px; max-height: 60px; }")
        self.factorIntButton.setStyleSheet(
            "QPushButton { background-color: #F033FF; border-radius: 5px; min-height: 60px; max-height: 60px; }")

        # Kết nối các nút với phương thức xử lý tương ứng
        self.factorButton.clicked.connect(self.factorPolynomial)
        self.expandButton.clicked.connect(self.expandPolynomial)
        self.simplifyButton.clicked.connect(self.simplifyPolynomial)
        self.factorIntButton.clicked.connect(self.factorInteger)


        # Tạo layout
        layout = QVBoxLayout()
        formLayout = QHBoxLayout()

        formLayout.addWidget(QLabel("Nhập đa thức hoặc số:"))
        formLayout.addWidget(self.inputLineEdit)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.factorButton)
        buttonsLayout.addWidget(self.expandButton)
        buttonsLayout.addWidget(self.simplifyButton)
        buttonsLayout.addWidget(self.factorIntButton)
        buttonsLayout.addWidget(self.divideButton)
        layout.addLayout(formLayout)
        layout.addLayout(buttonsLayout)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)


    def dividePolynomial(self):
        input_text = self.inputLineEdit.text().split('/')
        if len(input_text) != 2:
            self.resultTextEdit.setHtml(
                "<div style='color: red;'>Lỗi: Nhập sai định dạng. Vui lòng nhập theo dạng 'đa thức 1 / đa thức 2'.</div>")
            return

        try:
            dividend = sympify(input_text[0])
            divisor = sympify(input_text[1])
            quotient, remainder = div(dividend, divisor)

            result_latex_quotient = latex(quotient)
            result_latex_remainder = latex(remainder)
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng python <br>Thương: {quotient}, Dư: {remainder} </div><br><div style='color: blue; font-size: 25px;'>Kết quả dạng Latex <br>LaTeX: {result_latex_quotient}, Dư: {result_latex_remainder}</div>"
            self.resultTextEdit.setHtml(formatted_result)

        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

    def factorPolynomial(self):
        polynomial = sympify(self.inputLineEdit.text())
        result = factor(polynomial)
        self.displayResult(result)

    def expandPolynomial(self):
        polynomial = sympify(self.inputLineEdit.text())
        result = expand(polynomial)
        self.displayResult(result)

    def simplifyPolynomial(self):
        polynomial = sympify(self.inputLineEdit.text())
        result = sympify(polynomial).simplify()
        self.displayResult(result)

    def factorInteger(self):
        try:
            # Chuyển đổi input từ người dùng thành biểu thức sympy
            input_value = self.inputLineEdit.text()
            integer = sympify(input_value)

            # Kiểm tra xem giá trị nhập vào có phải là số nguyên dương
            if integer.is_integer and integer > 0:
                # Thực hiện phân tích thừa số nguyên tố nếu là số nguyên dương
                result = factorint(integer)
                self.displayResult(result)
            else:
                # Hiển thị thông báo lỗi nếu không phải số nguyên dương
                self.resultTextEdit.setHtml("<div style='color: red;'>Lỗi: Vui lòng nhập một số nguyên dương.</div>")
        except Exception as e:
            # Bắt lỗi và hiển thị thông báo lỗi nếu có vấn đề với việc phân tích input
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

    def displayResult(self, result):
        result_latex = latex(result)
        formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {result}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
        self.resultTextEdit.setHtml(formatted_result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PolynomialOperationsDialog()
    dialog.show()
    sys.exit(app.exec_())
