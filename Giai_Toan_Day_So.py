from PyQt5.QtWidgets import QApplication, QMessageBox,QPlainTextEdit
import sys
import sympy as sp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QGroupBox, QPlainTextEdit
class Toan_Day_So(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nguyễn Văn Sang - GV THPT Nguyễn Hữu Cảnh - TP HCM")
        self.setGeometry(50, 100, 1200, 1000)
        self.layout = QVBoxLayout(self)

        self.group_box1 = QGroupBox("Truy Hồi Cấp 1 Với Dãy u(n)=a.u(n-1)+b.n^2+c.n+d+e.f^n", self)
        self.group_box1.setStyleSheet("QGroupBox:title { color: blue; }")
        self.layout.addWidget(self.group_box1)
        input_layout = QHBoxLayout()
        self.label1a = QLabel(self)
        self.label1a.setText("Nhập a của a.u(n-1)")
        input_layout.addWidget(self.label1a)
        self.num1a = QLineEdit(self)
        input_layout.addWidget(self.num1a)

        self.label1b = QLabel(self)
        self.label1b.setText("Nhập b của b.n^2")
        input_layout.addWidget(self.label1b)
        self.num1b = QLineEdit(self)
        input_layout.addWidget(self.num1b)

        self.label1c = QLabel(self)
        self.label1c.setText("Nhập c của c.n")
        input_layout.addWidget(self.label1c)
        self.num1c = QLineEdit(self)
        input_layout.addWidget(self.num1c)

        self.label1d = QLabel(self)
        self.label1d.setText("Nhập d")
        input_layout.addWidget(self.label1d)
        self.num1d = QLineEdit(self)
        input_layout.addWidget(self.num1d)

        self.label1e = QLabel(self)
        self.label1e.setText("Giá trị u(1)")
        input_layout.addWidget(self.label1e)
        self.initial_term_num = QLineEdit(self)
        input_layout.addWidget(self.initial_term_num)

        self.label1f = QLabel(self)
        self.label1f.setText("Nhập e của e.f^n")
        input_layout.addWidget(self.label1f)
        self.e_num = QLineEdit(self)
        input_layout.addWidget(self.e_num)

        self.label1g = QLabel(self)
        self.label1g.setText("Nhập f của e.f^n")
        input_layout.addWidget(self.label1g)
        self.f_num = QLineEdit(self)
        input_layout.addWidget(self.f_num)

        self.button_generate = QPushButton("Giải", self)
        self.button_generate.clicked.connect(self.find_general_term)
        self.button_hd = QPushButton("Hướng Dẫn", self)
        self.button_hd.clicked.connect(self.hd)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_generate)
        # button_layout.addWidget(self.button_clear)
        button_layout.addWidget(self.button_hd)
        input_layout.addLayout(button_layout)
        self.group_box1.setLayout(input_layout)
        self.group_box2 = QGroupBox("Truy Hồi Cấp 2 Với Dãy u(n)=a_1.u(n-1)+a_2.u(n-2)+b.n^2+c.n+d+e.f^n", self)
        self.group_box2.setStyleSheet("QGroupBox:title { color: red; }")
        self.layout.addWidget(self.group_box2)
        input_layout = QHBoxLayout()
        self.label2a = QLabel(self)
        self.label2a.setText("a_1 của a_1.u(n-1)")
        input_layout.addWidget(self.label2a)
        self.num2a = QLineEdit(self)
        input_layout.addWidget(self.num2a)

        self.label2a2 = QLabel(self)
        self.label2a2.setText("a_2 của a_2.u(n-2)")
        input_layout.addWidget(self.label2a2)
        self.num2a2 = QLineEdit(self)
        input_layout.addWidget(self.num2a2)

        self.label2b = QLabel(self)
        self.label2b.setText("b của b.n^2")
        input_layout.addWidget(self.label2b)
        self.num2b = QLineEdit(self)
        input_layout.addWidget(self.num2b)

        self.label2c = QLabel(self)
        self.label2c.setText("c của c.n")
        input_layout.addWidget(self.label2c)
        self.num2c = QLineEdit(self)
        input_layout.addWidget(self.num2c)

        self.label2d = QLabel(self)
        self.label2d.setText("Nhập d")
        input_layout.addWidget(self.label2d)
        self.num2d = QLineEdit(self)
        input_layout.addWidget(self.num2d)

        self.label2e = QLabel(self)
        self.label2e.setText("Giá trị u(1)")
        input_layout.addWidget(self.label2e)
        self.initial_term_num2a = QLineEdit(self)
        input_layout.addWidget(self.initial_term_num2a)
        self.label2e2 = QLabel(self)
        self.label2e2.setText("Giá trị u(2)")
        input_layout.addWidget(self.label2e2)
        self.initial_term_num2b = QLineEdit(self)
        input_layout.addWidget(self.initial_term_num2b)

        self.label2f = QLabel(self)
        self.label2f.setText("e của e.f^n")
        input_layout.addWidget(self.label2f)
        self.e_num2 = QLineEdit(self)
        input_layout.addWidget(self.e_num2)

        self.label2g = QLabel(self)
        self.label2g.setText("f của e.f^n")
        input_layout.addWidget(self.label2g)
        self.f_num2 = QLineEdit(self)
        input_layout.addWidget(self.f_num2)

        self.button_generate = QPushButton("Giải", self)
        self.button_generate.clicked.connect(self.find2_general_term)
        self.button_hd = QPushButton("Hướng Dẫn", self)
        self.button_hd.clicked.connect(self.hd)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_generate)
        # button_layout.addWidget(self.button_clear)
        button_layout.addWidget(self.button_hd)
        input_layout.addLayout(button_layout)
        self.group_box2.setLayout(input_layout)


        self.result_text = QPlainTextEdit(self)
        self.layout.addWidget(self.result_text)
        self.setLayout(self.layout)
    def find_general_term(self):
        try:
            a = int(self.num1a.text() or 0)
            b = int(self.num1b.text() or 0)
            c = int(self.num1c.text() or 0)
            d = int(self.num1d.text() or 0)
            e = int(self.e_num.text() or 0)
            f = int(self.f_num.text() or 1)
            initial_term = int(self.initial_term_num.text() or 0)
        except ValueError:
            # Xử lý lỗi khi giá trị nhập vào không phải là số hợp lệ
            # Ví dụ: Hiển thị thông báo lỗi cho người dùng
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập giá trị số hợp lệ.')
            return

        n = sp.symbols('n')

        general_term = self.calculate_general_term(a, b, c, d,e,f, n, initial_term)
        self.result_text.setPlainText(f"Số hạng tổng quát của dãy là $u_n={sp.latex(general_term)}$")
    def calculate_general_term(self, a, b, c, d, e, f, n, initial_term):
        u = sp.Function('u')
        equation = sp.Eq(u(n), a * u(n-1) + b * n**2 + c * n + d+e*f**n)
        solution = sp.rsolve(equation, u(n), [initial_term])
        return solution

    def find2_general_term(self):
        try:
            a = int(self.num2a.text() or 0)
            m = int(self.num2a2.text() or 0)
            b = int(self.num2b.text() or 0)
            c = int(self.num2c.text() or 0)
            d = int(self.num2d.text() or 0)
            e = int(self.e_num2.text() or 0)
            f = int(self.f_num2.text() or 1)
            initial_term1 = int(self.initial_term_num2a.text() or 0)
            initial_term2 = int(self.initial_term_num2b.text() or 0)
        except ValueError:
            # Xử lý lỗi khi giá trị nhập vào không phải là số hợp lệ
            # Ví dụ: Hiển thị thông báo lỗi cho người dùng
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập giá trị số hợp lệ.')
            return

        n = sp.symbols('n')

        general_term = self.calculate2_general_term(a, m, b, c, d, e, f, n, initial_term1, initial_term2)
        self.result_text.setPlainText(f"Số hạng tổng quát của dãy là $u_n={sp.latex(general_term)}$")

    def calculate2_general_term(self, a, m, b, c, d, e, f, n, initial_term1, initial_term2):
        u = sp.Function('u')
        equation = sp.Eq(u(n), a * u(n - 1) + m * u(n - 2) + b * n ** 2 + c * n + d + e * f ** n)

        # Sử dụng hàm rsolve để giải phương trình đệ quy
        solution = sp.rsolve(equation, u(n), {u(0): initial_term1, u(1): initial_term2})
        return solution

    def hd(self):
        QMessageBox.information(self, 'Hướng Dẫn Sử Dụng',
                                '1. Các hệ số là số nguyên \n'
                                '2. Hệ số nào ko có thì để trống\n' )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Toan_Day_So()
    window.show()
    sys.exit(app.exec_())
