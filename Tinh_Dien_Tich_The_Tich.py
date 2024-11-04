from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QTextEdit, QApplication
from sympy import N
from sympy import latex, sqrt
from sympy import Point3D, sympify
from sympy.matrices import Matrix
class GeometryCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Toán Hình Học")

        layout = QVBoxLayout()

        # Tạo QGroupBox cho tính diện tích tam giác
        triangleGroupBox = QGroupBox("Tính Diện Tích Tam Giác")
        triangleLayout = QVBoxLayout()
        self.trianglePointsEdits = [[QLineEdit() for _ in range(3)] for _ in range(3)]  # Tạo một list cho 3 điểm A, B, C
        for i, pointName in enumerate(['A', 'B', 'C']):
            pointLayout = QHBoxLayout()
            pointLayout.addWidget(QLabel(f"Điểm {pointName} (x, y, z):"))
            for edit in self.trianglePointsEdits[i]:
                pointLayout.addWidget(edit)
            triangleLayout.addLayout(pointLayout)
        self.calcTriangleAreaButton = QPushButton("Tính Diện Tích")
        self.calcTriangleAreaButton.clicked.connect(self.calculateTriangleArea)
        triangleLayout.addWidget(self.calcTriangleAreaButton)
        triangleGroupBox.setLayout(triangleLayout)
        layout.addWidget(triangleGroupBox)

        # Tạo QGroupBox cho tính thể tích tứ diện
        tetrahedronGroupBox = QGroupBox("Tính Thể Tích Tứ Diện")
        tetrahedronLayout = QVBoxLayout()
        self.tetrahedronPointsEdits = [[QLineEdit() for _ in range(3)] for _ in range(4)]  # Tạo một list cho 4 điểm A, B, C, D
        for i, pointName in enumerate(['A', 'B', 'C', 'D']):
            pointLayout = QHBoxLayout()
            pointLayout.addWidget(QLabel(f"Điểm {pointName} (x, y, z):"))
            for edit in self.tetrahedronPointsEdits[i]:
                pointLayout.addWidget(edit)
            tetrahedronLayout.addLayout(pointLayout)
        self.calcTetrahedronVolumeButton = QPushButton("Tính Thể Tích")
        self.calcTetrahedronVolumeButton.clicked.connect(self.calculateTetrahedronVolume)
        tetrahedronLayout.addWidget(self.calcTetrahedronVolumeButton)
        tetrahedronGroupBox.setLayout(tetrahedronLayout)
        layout.addWidget(tetrahedronGroupBox)

        # Thêm QTextEdit để hiển thị kết quả
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)  # Đặt thành chỉ đọc để người dùng không thể chỉnh sửa kết quả
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def getPointFromEdit(self, edits):
        return Point3D(sympify(edits[0].text() or '0'), sympify(edits[1].text() or '0'), sympify(edits[2].text() or '0'))



    def calculateTriangleArea(self):
        try:
            # Lấy điểm từ QLineEdit và chuyển thành vectơ
            A = Matrix(self.getPointFromEdit(self.trianglePointsEdits[0]))
            B = Matrix(self.getPointFromEdit(self.trianglePointsEdits[1]))
            C = Matrix(self.getPointFromEdit(self.trianglePointsEdits[2]))

            # Tạo vectơ AB và AC từ các điểm
            AB = B - A
            AC = C - A

            # Tính tích có hướng của AB và AC để tìm vectơ vuông góc
            cross_product = AB.cross(AC)

            area = cross_product.norm() / 2

            # Định dạng kết quả dạng số thực
            area_evaluated = N(area)

            # Định dạng kết quả dạng LaTeX
            area_latex = latex(area)

            # Định dạng kết quả và hiển thị
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {area_evaluated}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{area_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red; font-size: 25px;'>Lỗi: {e}</div>")


    def calculateTetrahedronVolume(self):
        try:
            # Lấy điểm từ QLineEdit
            A = self.getPointFromEdit(self.tetrahedronPointsEdits[0])
            B = self.getPointFromEdit(self.tetrahedronPointsEdits[1])
            C = self.getPointFromEdit(self.tetrahedronPointsEdits[2])
            D = self.getPointFromEdit(self.tetrahedronPointsEdits[3])

            # Tạo vectơ AB, AC, và AD
            AB = B - A
            AC = C - A
            AD = D - A

            # Tạo ma trận từ các vectơ AB, AC, và AD
            M = Matrix([
                [AB.x, AB.y, AB.z],
                [AC.x, AC.y, AC.z],
                [AD.x, AD.y, AD.z]
            ])

            # Tính thể tích bằng 1/6 giá trị tuyệt đối của định thức của M
            volume = abs(M.det()) / 6

            # Định dạng kết quả dạng số thực
            volume_evaluated = N(volume)

            # Định dạng kết quả dạng LaTeX
            volume_latex = latex(volume)

            # Định dạng kết quả và hiển thị
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {volume_evaluated}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{volume_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red; font-size: 25px;'>Lỗi: {e}</div>")

if __name__ == "__main__":
    app = QApplication([])
    dialog = GeometryCalculatorDialog()
    dialog.show()
    app.exec_()
