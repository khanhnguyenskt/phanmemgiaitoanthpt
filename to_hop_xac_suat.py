import sys
from PyQt5.QtWidgets import QPushButton, QLineEdit, QDialog, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout, QApplication
from sympy import symbols, factorial, binomial, sympify

class CombinatoricsCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Toán Hoán Vị, Chỉnh Hợp, Tổ Hợp")

        # Cấu hình các widget
        self.nLineEdit = QLineEdit()
        self.rLineEdit = QLineEdit()
        self.resultTextEdit = QTextEdit()
        self.permutationButton = QPushButton("Hoán Vị")
        self.combinationButton = QPushButton("Tổ Hợp")
        self.arrangementButton = QPushButton("Chỉnh Hợp")

        # Đặt màu nền và phong cách cho các nút
        self.permutationButton.setStyleSheet("background-color: lightgreen; font-size: 25px;")
        self.combinationButton.setStyleSheet("background-color: lightblue; font-size: 25px;")
        self.arrangementButton.setStyleSheet("background-color: lightcoral; font-size: 25px;")

        # Đặt phong cách cho kết quả
        self.resultTextEdit.setStyleSheet("color: blue; font-size: 20px;")

        # Cấu hình sự kiện click cho mỗi nút
        self.permutationButton.clicked.connect(self.calculatePermutation)
        self.combinationButton.clicked.connect(self.calculateCombination)
        self.arrangementButton.clicked.connect(self.calculateArrangement)

        # Tạo layout
        layout = QVBoxLayout()
        inputLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        # Thêm widget vào layout
        inputLayout.addWidget(QLabel("Số phần tử n:"))
        inputLayout.addWidget(self.nLineEdit)
        inputLayout.addWidget(QLabel("Chập k:"))
        inputLayout.addWidget(self.rLineEdit)
        buttonLayout.addWidget(self.permutationButton)
        buttonLayout.addWidget(self.combinationButton)
        buttonLayout.addWidget(self.arrangementButton)

        # Thêm các layout và widget vào dialog
        layout.addLayout(inputLayout)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def calculatePermutation(self):
        # Thêm phần xử lý lỗi để thông báo khi nhập sai
        try:
            n = sympify(self.nLineEdit.text())
            result = factorial(n)
            self.displayResult(result)
        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {e}")

    def calculateCombination(self):
        try:
            n = sympify(self.nLineEdit.text())
            r = sympify(self.rLineEdit.text())
            result = binomial(n, r)
            self.displayResult(result)
        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {e}")

    def calculateArrangement(self):
        try:
            n = sympify(self.nLineEdit.text())
            r = sympify(self.rLineEdit.text())
            result = binomial(n, r) * factorial(r)
            self.displayResult(result)
        except Exception as e:
            self.resultTextEdit.setText(f"Lỗi: {e}")

    def displayResult(self, result):
        self.resultTextEdit.setHtml(f"<div style='color: blue; font-size: 30px;'>Kết quả: {result}</div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CombinatoricsCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
