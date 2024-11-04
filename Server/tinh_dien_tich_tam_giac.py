from sympy import N
from sympy import latex
from sympy import Point3D, sympify
from sympy.matrices import Matrix
from flask import request, Blueprint

blueprint_tinh_dien_tich_tam_giac = Blueprint('tinh_dien_tich_tam_giac', __name__)


def getPointFromEdit(edits):
    return Point3D(sympify(edits[0] or '0'), sympify(edits[1] or '0'), sympify(edits[2] or '0'))


@blueprint_tinh_dien_tich_tam_giac.route('/', methods=['POST'])
def calculateTriangleArea():
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

        try:
            # Lấy điểm từ QLineEdit và chuyển thành vectơ
            A = Matrix(getPointFromEdit([Ax, Ay, Az]))
            B = Matrix(getPointFromEdit([Bx, By, Bz]))
            C = Matrix(getPointFromEdit([Cx, Cy, Cz]))

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
            return f"Kết quả dạng Python: {area_evaluated} \nKết quả dạng LaTeX: {area_latex}"
        except Exception as e:
            return f"Lỗi: {e}"

