import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QComboBox, QMessageBox
from sympy import symbols, Eq, solve, sympify, latex, solveset, S

class AdvancedEquationSolverDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Giải Phương Trình/Bất Phương Trình Nâng Cao")

        # Cấu hình các widget
        self.leftSideLineEdit = QLineEdit()
        self.comparisonComboBox = QComboBox()
        self.comparisonComboBox.addItems(["=", ">=", "<=", "<", ">"])
        self.rightSideLineEdit = QLineEdit("0")  # Giá trị mặc định cho vế phải
        self.variableLineEdit = QLineEdit("x")  # Giá trị mặc định cho biến
        self.resultTextEdit = QTextEdit()
        self.solveButton = QPushButton("Giải")
        self.solveButton.clicked.connect(self.solveEquation)

        # Tạo layout
        layout = QVBoxLayout()
        equationLayout = QHBoxLayout()

        # Thêm widget vào layout
        equationLayout.addWidget(QLabel("Vế trái:"))
        equationLayout.addWidget(self.leftSideLineEdit)
        equationLayout.addWidget(self.comparisonComboBox)
        equationLayout.addWidget(self.rightSideLineEdit)
        equationLayout.addWidget(QLabel("Giải theo biến:"))
        equationLayout.addWidget(self.variableLineEdit)

        # Thêm các layout và widget vào dialog
        layout.addLayout(equationLayout)
        layout.addWidget(self.solveButton)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def solveEquation(self):
        solution = None  # Khởi tạo solution với giá trị mặc định là None
        try:
            # Chuyển đổi chuỗi nhập vào thành biểu thức sympy
            left_side = sympify(self.leftSideLineEdit.text())
            right_side = sympify(self.rightSideLineEdit.text())
            variable = symbols(self.variableLineEdit.text())

            # Lấy loại so sánh từ combobox
            comparison = self.comparisonComboBox.currentText()

            # Giải phương trình hoặc bất phương trình
            if comparison == "=":
                equation = Eq(left_side, right_side)
                solution = solve(equation, variable)
            else:
                # Sử dụng solveset cho bất phương trình
                equation = left_side - right_side
                if comparison == ">=":
                    solution = solveset(equation >= 0, variable, domain=S.Reals)
                elif comparison == "<=":
                    solution = solveset(equation <= 0, variable, domain=S.Reals)
                elif comparison == "<":
                    solution = solveset(equation < 0, variable, domain=S.Reals)
                elif comparison == ">":
                    solution = solveset(equation > 0, variable, domain=S.Reals)

            # Định dạng kết quả để hiển thị
            result_latex = latex(solution)
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {solution}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)

        except Exception as e:
            # Hiển thị cửa sổ thông báo lỗi
            QMessageBox.warning(self, "Lỗi cú pháp", f"Có lỗi xảy ra: {e}\nVui lòng kiểm tra lại cú pháp và thử lại.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AdvancedEquationSolverDialog()
    dialog.show()
    sys.exit(app.exec_())
