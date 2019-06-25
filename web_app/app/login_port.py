from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/getUserPassword', methods=["GET"])
def getUserPassword():
    return jsonify({"mobile": "SDGKA72", "password": "sdf123"})


@app.route('/member/butler_login.do', methods=['POST'])
def butler_login():
    re_body = request.json
    username = re_body.get('mobile') == 'SDGKA72'
    password = re_body.get('password') == 'sdg123'

    res_mes = {}
    if not username:
        res_mes["code"] = 200
        res_mes["mess"] = "账号不匹配"
    elif username and not password:
        res_mes["code"] = 200
        res_mes["mess"] = "密码错误"
    else:
        res_mes["code"] = 200
        res_mes["mess"] = "login successfully"
    return jsonify(res_mes)


@app.route('/upload/image', methods=['POST'])
def update_file():
    f = request.files['file']
    print(request.headers)
    f.save('upload/image.png')
    return "is ok"


@app.route('/', methods=['GET'])
def index():
    return 'hello flask'


if __name__ == '__main__':
    app.run()
