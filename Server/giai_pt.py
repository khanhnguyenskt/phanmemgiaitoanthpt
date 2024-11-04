from flask import request, Blueprint
from sympy import Eq, solve, latex, solveset, S, sympify

blueprint_giai_pt = Blueprint('giai_pt', __name__)


@blueprint_giai_pt.route('/', methods=['POST'])
def solveEquation():
    if request.method == "POST":
        solution = None  # Khởi tạo solution với giá trị mặc định là None
        try:
            # Chuyển đổi chuỗi nhập vào thành biểu thức sympy
            left_side = sympify(request.form.get('left_side', None))
            right_side = sympify(request.form.get('right_side', None))
            variable = sympify(request.form.get('variable', None))

            # Lấy loại so sánh từ combobox
            comparison = request.form.get('comparison', None)

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
            return result_latex

        except Exception as e:
            # Hiển thị cửa sổ thông báo lỗi
            return f"Lỗi cú pháp: {e}, Vui lòng kiểm tra lại cú pháp và thử lại."
