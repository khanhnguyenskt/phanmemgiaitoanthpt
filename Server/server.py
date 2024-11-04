import flask
from flask_cors import CORS
from dao_ham import blueprint_dao_ham
from giai_pt import blueprint_giai_pt
from tinh_the_tich_tu_dien import blueprint_tinh_the_tich_tu_dien
from tinh_dien_tich_tam_giac import blueprint_tinh_dien_tich_tam_giac


app = flask.Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
app.register_blueprint(blueprint_dao_ham, url_prefix='/dao_ham')
app.register_blueprint(blueprint_giai_pt, url_prefix='/giai_pt')
app.register_blueprint(blueprint_tinh_the_tich_tu_dien, url_prefix='/tinh_the_tich_tu_dien')
app.register_blueprint(blueprint_tinh_dien_tich_tam_giac, url_prefix='/tinh_dien_tich_tam_giac')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

