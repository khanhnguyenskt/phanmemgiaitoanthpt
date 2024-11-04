from sympy import N
from sympy import Point3D, sympify
from sympy import latex
from sympy.matrices import Matrix
from flask import request, Blueprint

blueprint_tinh_the_tich_tu_dien = Blueprint('tinh_the_tich_tu_dien', __name__)


def getPointFromEdit(edits):
    return Point3D(sympify(edits[0] or '0'), sympify(edits[1] or '0'), sympify(edits[2] or '0'))


@blueprint_tinh_the_tich_tu_dien.route('/', methods=['POST'])
def calculateTetrahedronVolume():
    if request.method == "POST":
        Ax = request.form.get('Ax', None)
        Ay = request.form.get('Ay', None)
        Az = request.form.get('Az', None)
        Bx = request.form.get('Bx', None)
        By = request.form.get('By', None)
        Bz = request.form.get('Bz', None)
        Cx = request.form.get('Cx', None)
        Cy = request.form.get('Cy', None)
        Cz = request.form.get('Cz', None)
        Dx = request.form.get('Dx', None)
        Dy = request.form.get('Dy', None)
        Dz = request.form.get('Dz', None)

        try:
            # Lấy điểm từ QLineEdit
            A = getPointFromEdit([Ax, Ay, Az])
            B = getPointFromEdit([Bx, By, Bz])
            C = getPointFromEdit([Cx, Cy, Cz])
            D = getPointFromEdit([Dx, Dy, Dz])

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
            formatted_result = f"Kết quả dạng Python: {volume_evaluated} \nKết quả dạng LaTeX: {volume_latex}"
            return formatted_result
        except Exception as e:
            return f"Lỗi: {e}"
