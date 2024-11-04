from sympy import sympify, pi, E, sin, cos, tan, asin, acos, atan, log, exp, sqrt, symbols, N
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox, \
    QDialog


class Calculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)  # Thêm tham số parent
        self.initUI()
        self.isDecimal = False  # Ban đầu không ở chế độ số thập phân

    def initUI(self):
        self.setWindowTitle('Máy Tính Mở Rộng')
        self.expressionTextEdit = QTextEdit()
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.expressionTextEdit)
        mainLayout.addWidget(self.resultTextEdit)

        buttonsLayout = QVBoxLayout()
        rows = [
            ('7', '8', '9', '+', 'sin', 'cos', 'tan', 'pi'),
            ('4', '5', '6', '-', 'asin', 'acos', 'atan', 'e'),
            ('1', '2', '3', '*', 'log', 'exp', '^', 'sqrt'),
            ('0', '.', '=', '/', '(', ')', 'clear', ',', 'S<=>D')
        ]

        for row in rows:
            rowLayout = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text)
                button.clicked.connect(self.onButtonClick)
                rowLayout.addWidget(button)
            buttonsLayout.addLayout(rowLayout)

        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)

    def onButtonClick(self):
        sender = self.sender()
        text = sender.text()

        if text == '=':
            expression = self.expressionTextEdit.toPlainText()
            try:
                result = sympify(expression, locals={'pi': pi, 'e': E})
                if self.isDecimal:
                    result = N(result)  # Chuyển kết quả thành số thập phân
                self.resultTextEdit.append(f"{expression} = {result}\n")
            except Exception as e:
                self.resultTextEdit.append("Error: Biểu thức không hợp lệ!\n")
        elif text == 'clear':
            self.expressionTextEdit.clear()
            self.resultTextEdit.clear()
        elif text == 'S<=>D':
            self.isDecimal = not self.isDecimal  # Đảo trạng thái
            self.resultTextEdit.append("Chế độ: Số thập phân" if self.isDecimal else "Chế độ: Biểu diễn chính xác")
        else:
            current_text = self.expressionTextEdit.toPlainText()
            new_text = current_text + text
            self.expressionTextEdit.setText(new_text)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = Calculator()
    dialog.show()
    sys.exit(app.exec_())
