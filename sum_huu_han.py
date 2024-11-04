import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from sympy import symbols, Sum, sympify, latex, Product


class FiniteSumCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Tổng Hữu Hạn và Giá Trị Tại x_0")

        # Cấu hình các widget
        self.expressionLineEdit = QLineEdit()
        self.lowerLimitLineEdit = QLineEdit()
        self.upperLimitLineEdit = QLineEdit()
        self.variableLineEdit = QLineEdit()
        self.x0LineEdit = QLineEdit()
        self.resultTextEdit = QTextEdit()
        self.calculateSumButton = QPushButton("Tính Tổng")
        self.calculateValueButton = QPushButton("Giá Trị tại x_0")
        # Thêm nút tính tích
        self.calculateProductButton = QPushButton("Tính Tích")
        self.calculateProductButton.setStyleSheet("background-color: #FFA07A; color: white;")  # Màu nền cam nhạt
        self.calculateProductButton.clicked.connect(self.calculateFiniteProduct)



        # Đặt màu nền cho các nút
        self.calculateSumButton.setStyleSheet("background-color: #4CAF50; color: white;")
        self.calculateValueButton.setStyleSheet("background-color: #2196F3; color: white;")

        # Cấu hình sự kiện click cho các nút
        self.calculateSumButton.clicked.connect(self.calculateFiniteSum)
        self.calculateValueButton.clicked.connect(self.calculateValueAtX0)

        # Tạo layout
        layout = QVBoxLayout()
        formLayout = QHBoxLayout()

        # Thêm widget vào layout
        formLayout.addWidget(QLabel("Biểu thức:"))
        formLayout.addWidget(self.expressionLineEdit)
        formLayout.addWidget(QLabel("Giới hạn dưới:"))
        formLayout.addWidget(self.lowerLimitLineEdit)
        formLayout.addWidget(QLabel("Giới hạn trên:"))
        formLayout.addWidget(self.upperLimitLineEdit)
        formLayout.addWidget(QLabel("Theo biến:"))
        formLayout.addWidget(self.variableLineEdit)
        formLayout.addWidget(QLabel("x_0:"))
        formLayout.addWidget(self.x0LineEdit)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.calculateSumButton)
        # Thêm nút vào layout
        buttonsLayout.addWidget(self.calculateProductButton)
        buttonsLayout.addWidget(self.calculateValueButton)

        # Thêm các layout và widget vào dialog
        layout.addLayout(formLayout)
        layout.addLayout(buttonsLayout)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def calculateFiniteSum(self):
        # Lấy giá trị từ các QLineEdit
        expression = self.expressionLineEdit.text()
        lower_limit = self.lowerLimitLineEdit.text()
        upper_limit = self.upperLimitLineEdit.text()
        variable = self.variableLineEdit.text()

        # Kiểm tra xem người dùng đã nhập đủ thông tin chưa
        if not expression or not lower_limit or not upper_limit or not variable:
            self.resultTextEdit.setHtml("<div style='color: red;'>Lỗi: Vui lòng nhập đầy đủ thông tin.</div>")
            return

        try:
            # Thực hiện tính tổng hữu hạn nếu đã nhập đủ thông tin
            sum_expression = Sum(sympify(expression),
                                 (symbols(variable), sympify(lower_limit), sympify(upper_limit))).doit()
            result_latex = latex(sum_expression)

            # Hiển thị kết quả
            formatted_result = f"<div style='color: red; font-size: 30px;'>Kết quả dạng Python:<br> {sum_expression}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

    def calculateValueAtX0(self):
        expression = self.expressionLineEdit.text()
        x0_value = self.x0LineEdit.text()
        variable = self.variableLineEdit.text()

        # Kiểm tra xem người dùng đã nhập đủ thông tin chưa
        if not expression or not x0_value or not variable:
            self.resultTextEdit.setHtml("<div style='color: red;'>Lỗi: Vui lòng nhập đầy đủ thông tin.</div>")
            return

        try:
            # Thực hiện tính giá trị tại x_0 nếu đã nhập đủ thông tin
            evaluated_expression = sympify(expression).subs(symbols(variable), sympify(x0_value))
            result_latex = latex(evaluated_expression)

            # Hiển thị kết quả
            formatted_result = f"<div style='color: green; font-size: 30px;'>Giá trị tại x_0:<br> {evaluated_expression}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

    def calculateFiniteProduct(self):
        expression = self.expressionLineEdit.text()
        lower_limit = self.lowerLimitLineEdit.text()
        upper_limit = self.upperLimitLineEdit.text()
        variable = self.variableLineEdit.text()

        if not expression or not lower_limit or not upper_limit or not variable:
            self.resultTextEdit.setHtml("<div style='color: red;'>Lỗi: Vui lòng nhập đầy đủ thông tin.</div>")
            return

        try:
            product_expression = Product(sympify(expression),
                                         (symbols(variable), sympify(lower_limit), sympify(upper_limit))).doit()
            result_latex = latex(product_expression)

            formatted_result = f"<div style='color: red; font-size: 30px;'>Kết quả dạng Python:<br> {product_expression}</div>\n<div style='color: blue; font-size: 30px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = FiniteSumCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
