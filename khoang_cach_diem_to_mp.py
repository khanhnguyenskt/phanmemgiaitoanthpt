import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QGroupBox
from sympy import symbols, Point, Plane, sympify, latex, sqrt, Point3D


class PlaneDistanceCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Khoảng Cách Từ Điểm Đến Mặt Phẳng")

        # Cấu hình các widget
        self.pointXLineEdit = QLineEdit()
        self.pointYLineEdit = QLineEdit()
        self.pointZLineEdit = QLineEdit()
        self.planeALineEdit = QLineEdit()
        self.planeBLineEdit = QLineEdit()
        self.planeCLineEdit = QLineEdit()
        self.planeDLineEdit = QLineEdit()
        self.resultTextEdit = QTextEdit()
        # Tạo QHBoxLayout để đặt cả hai nút
        buttonsLayout = QHBoxLayout()
        self.calculateButton = QPushButton("Tính Khoảng Cách")
        self.calculateButton.clicked.connect(self.calculateDistance)
        self.calculatePlaneButton = QPushButton("Tính Khoảng Cách Đến Mặt Phẳng")
        self.calculatePlaneButton.clicked.connect(self.calculateDistanceToPlane)
        # Thêm các nút vào layout
        buttonsLayout.addWidget(self.calculateButton)
        buttonsLayout.addWidget(self.calculatePlaneButton)

        # Tô màu nền cho các nút
        self.calculateButton.setStyleSheet("QPushButton { background-color: #33D1FF; border-radius: 5px; min-height: 60px; max-height: 60px; }")
        self.calculatePlaneButton.setStyleSheet("QPushButton { background-color: #FF5733; border-radius: 5px; min-height: 60px; max-height: 60px; }")

        # Khởi tạo QLineEdit cho các điểm M, N, P
        self.pointMXLineEdit = QLineEdit()
        self.pointMYLineEdit = QLineEdit()
        self.pointMZLineEdit = QLineEdit()

        self.pointNXLineEdit = QLineEdit()
        self.pointNYLineEdit = QLineEdit()
        self.pointNZLineEdit = QLineEdit()

        self.pointPXLineEdit = QLineEdit()
        self.pointPYLineEdit = QLineEdit()
        self.pointPZLineEdit = QLineEdit()

        # Tạo layout
        layout = QVBoxLayout()
        pointLayout = QHBoxLayout()
        planeLayout = QHBoxLayout()

        # Canh label và các trường nhập liệu
        pointLabel = QLabel("Điểm (x0, y0, z0):")
        pointLabel.setFixedWidth(200)
        planeLabel = QLabel("Mặt phẳng (A,B,C,D):")
        planeLabel.setFixedWidth(200)

        # Thêm widget vào layout
        pointLayout.addWidget(pointLabel)
        pointLayout.addWidget(self.pointXLineEdit)
        pointLayout.addWidget(self.pointYLineEdit)
        pointLayout.addWidget(self.pointZLineEdit)

        planeLayout.addWidget(planeLabel)
        planeLayout.addWidget(self.planeALineEdit)
        planeLayout.addWidget(self.planeBLineEdit)
        planeLayout.addWidget(self.planeCLineEdit)
        planeLayout.addWidget(self.planeDLineEdit)

        pointsGroupBox = QGroupBox("Mặt phẳng qua 3 điểm")
        pointsGroupBoxLayout = QVBoxLayout()

        # Layout cho điểm M
        pointMLayout = QHBoxLayout()
        pointMLayout.addWidget(QLabel("Điểm M (x, y, z):"))
        pointMLayout.addWidget(self.pointMXLineEdit)
        pointMLayout.addWidget(self.pointMYLineEdit)
        pointMLayout.addWidget(self.pointMZLineEdit)

        # Layout cho điểm N
        pointNLayout = QHBoxLayout()
        pointNLayout.addWidget(QLabel("Điểm N (x, y, z):"))
        pointNLayout.addWidget(self.pointNXLineEdit)
        pointNLayout.addWidget(self.pointNYLineEdit)
        pointNLayout.addWidget(self.pointNZLineEdit)

        # Layout cho điểm P
        pointPLayout = QHBoxLayout()
        pointPLayout.addWidget(QLabel("Điểm P (x, y, z):"))
        pointPLayout.addWidget(self.pointPXLineEdit)
        pointPLayout.addWidget(self.pointPYLineEdit)
        pointPLayout.addWidget(self.pointPZLineEdit)

        # Thêm các layout con vào layout của QGroupBox
        pointsGroupBoxLayout.addLayout(pointMLayout)
        pointsGroupBoxLayout.addLayout(pointNLayout)
        pointsGroupBoxLayout.addLayout(pointPLayout)
        pointsGroupBox.setLayout(pointsGroupBoxLayout)

        # Thêm các layout và widget vào layout chính của dialog
        layout.addLayout(pointLayout)
        layout.addLayout(planeLayout)
        layout.addWidget(pointsGroupBox)
        # layout.addWidget(self.calculateButton)
        # layout.addWidget(self.calculatePlaneButton)
        # Thêm buttonsLayout vào layout chính
        layout.addLayout(buttonsLayout)
        layout.addWidget(self.resultTextEdit)

        self.setLayout(layout)

    def calculateDistanceToPlane(self):
        # Lấy tọa độ của 3 điểm M, N, P từ QLineEdit, coi trống là 0
        m = Point3D(sympify(self.pointMXLineEdit.text() or '0'), sympify(self.pointMYLineEdit.text() or '0'),
                    sympify(self.pointMZLineEdit.text() or '0'))
        n = Point3D(sympify(self.pointNXLineEdit.text() or '0'), sympify(self.pointNYLineEdit.text() or '0'),
                    sympify(self.pointNZLineEdit.text() or '0'))
        p = Point3D(sympify(self.pointPXLineEdit.text() or '0'), sympify(self.pointPYLineEdit.text() or '0'),
                    sympify(self.pointPZLineEdit.text() or '0'))
        # Kiểm tra xem tất cả các điểm có phải là điểm gốc không hoặc có ít nhất 2 điểm trùng nhau không
        if m == n == p == Point3D(0, 0, 0) or m == n or n == p or m == p:
            self.resultTextEdit.setHtml(
                "<div style='color: red;'>Lỗi: Tất cả các điểm không thể đều là điểm gốc hoặc có ít nhất 2 điểm trùng nhau. Vui lòng nhập lại.</div>")
            return

        # Tạo mặt phẳng từ 3 điểm M, N, P
        plane = Plane(m, n, p)

        # Lấy tọa độ của điểm cần tính khoảng cách đến mặt phẳng, coi trống là 0
        q = Point3D(sympify(self.pointXLineEdit.text() or '0'), sympify(self.pointYLineEdit.text() or '0'),
                    sympify(self.pointZLineEdit.text() or '0'))

        # Tính khoảng cách từ điểm Q đến mặt phẳng
        distance = q.distance(plane)
        result_latex = latex(distance)

        # Hiển thị kết quả
        self.resultTextEdit.setHtml(f"<div style='color: blue; font-size: 25px;'>Khoảng cách: <br>{result_latex}</div>")

    def calculateDistance(self):
        # Đọc giá trị từ người dùng và kiểm tra giá trị 0
        x, y, z = sympify(self.pointXLineEdit.text() or '0'), sympify(self.pointYLineEdit.text() or '0'), sympify(
            self.pointZLineEdit.text() or '0')
        a, b, c, d = sympify(self.planeALineEdit.text() or '0'), sympify(self.planeBLineEdit.text() or '0'), sympify(
            self.planeCLineEdit.text() or '0'), sympify(self.planeDLineEdit.text() or '0')

        # Kiểm tra xem tất cả các giá trị có phải là 0
        if all(value == 0 for value in [a, b, c, d]):
            self.resultTextEdit.setHtml(
                "<div style='color: red;'>Lỗi: Tất cả các giá trị không thể đều là 0. Vui lòng nhập lại.</div>")
            return

        try:
            # Tạo điểm
            point = Point(x, y, z)

            # Xác định điểm trên mặt phẳng dựa vào a, b, và c
            if c != 0:
                reference_point = Point3D(0, 0, -d / c)
            elif b != 0:
                reference_point = Point3D(0, -d / b, 0)
            elif a != 0:
                reference_point = Point3D(-d / a, 0, 0)
            else:
                self.resultTextEdit.setHtml("<div style='color: red;'>Lỗi: a, b và c không thể đồng thời bằng 0.</div>")
                return

            # Tạo mặt phẳng
            plane = Plane(reference_point, normal_vector=(a, b, c))

            # Tính khoảng cách
            distance = point.distance(plane)
            result_latex = latex(distance)

            # Định dạng kết quả và hiển thị
            formatted_result = f"<div style='color: red; font-size: 25px;'>Kết quả dạng Python:<br> {distance}</div>\n<div style='color: blue; font-size: 25px;'>Kết quả dạng LaTeX: <br>{result_latex}</div>"
            self.resultTextEdit.setHtml(formatted_result)
        except Exception as e:
            self.resultTextEdit.setHtml(f"<div style='color: red;'>Lỗi: {e}</div>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PlaneDistanceCalculatorDialog()
    dialog.show()
    sys.exit(app.exec_())
