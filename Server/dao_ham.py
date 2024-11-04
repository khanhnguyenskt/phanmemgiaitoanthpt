from sympy import symbols, diff, latex, sympify
from flask import request, Response, Blueprint

blueprint_dao_ham = Blueprint('dao_ham', __name__)


@blueprint_dao_ham.route('/', methods=['POST'])
def calculate_derivative():
    if request.method == "POST":
        function = request.form.get('function', None)
        variable = request.form.get('variable', None)

        try:
            x = symbols(variable)
            expr = sympify(function)
            result = diff(expr, x)
            result_latex = latex(result) # Tính đạo hàm
            return Response(result_latex)
        except Exception as e:
            error_message = f"Lỗi: {e}"
            return Response(error_message)
