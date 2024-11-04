import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from sympy import symbols, Eq, solve, sympify, latex

class SystemOfEquationsSolverDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Giải Hệ Phương Trình")
        self.setMinimumWidth(800)
        self.equationsLayouts = []
        self.variablesLineEdit = QLineEdit("x, y, z, t")
        self.numberOfEquationsComboBox = QComboBox()
        self.numberOfEquationsComboBox.addItems(["2", "3", "4"])
        self.solveButton = QPushButton("Giải Hệ Phương Trình")
        self.resultTextEdit = QTextEdit()

        self.solveButton.clicked.connect(self.solveSystemOfEquations)
        self.numberOfEquationsComboBox.currentIndexChanged.connect(self.updateEquationInputs)

        layout = QVBoxLayout()
        optionsLayout = QHBoxLayout()  # Layout mới để chứa combobox và lineedit trên cùng một dòng
        optionsLayout.addWidget(QLabel("Số phương trình:"))
        optionsLayout.addWidget(self.numberOfEquationsComboBox)
        optionsLayout.addWidget(QLabel("Các ẩn (ngăn cách bằng dấu phẩy):"))
        optionsLayout.addWidget(self.variablesLineEdit)
        layout.addLayout(optionsLayout)

        self.equationsWidgetLayout = QVBoxLayout()
        layout.addLayout(self.equationsWidgetLayout)

        layout.addWidget(self.solveButton)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)
        self.updateEquationInputs(0)
    def updateEquationInputs(self, index):
        # Xóa các layout cũ
        while self.equationsWidgetLayout.count():
            child = self.equationsWidgetLayout.takeAt(0)
            if child.layout():
                while child.layout().count():
                    grand_child = child.layout().takeAt(0)
                    if grand_child.widget():
                        grand_child.widget().deleteLater()
                child.layout().deleteLater()

        # Tạo mới layout cho từng phương trình
        num_equations = int(self.numberOfEquationsComboBox.currentText())
        self.equationsLayouts = []
        for i in range(num_equations):
            equationLayout = QHBoxLayout()
            equationLabel = QLabel(f"Phương trình {i+1}: ")
            equationLineEdit = QLineEdit()
            equationLayout.addWidget(equationLabel)
            equationLayout.addWidget(equationLineEdit)
            self.equationsWidgetLayout.addLayout(equationLayout)
            self.equationsLayouts.append((equationLineEdit, equationLabel))

    def solveSystemOfEquations(self):
        equations = []
        for equationLineEdit, _ in self.equationsLayouts:
            try:
                equation = sympify(equationLineEdit.text())
                equations.append(equation)
            except Exception as e:
                self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi ở phương trình nhập: {equationLineEdit.text()} - {e}</div>")
                return

        variables = symbols(self.variablesLineEdit.text().replace(' ', ''))
        try:
            solution = solve(equations, variables)
            result_latex = latex(solution)
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {solution}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SystemOfEquationsSolverDialog()
    dialog.show()
    sys.exit(app.exec_())
