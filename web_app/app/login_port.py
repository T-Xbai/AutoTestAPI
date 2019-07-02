from flask import request, jsonify
from web_app.app import app,db
from datetime import datetime

from web_app.app.models import User, UserSchema

import json


@app.route('/getUserPassword', methods=["GET"])
def getUserPassword():
    users = User.query.all()
    schema = UserSchema(many=True)
    results = schema.dump(users)
    return jsonify(results.data)


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
        res_mes["sql"] = "jianchuang"
    return jsonify(res_mes)


@app.route('/upload/image', methods=['POST'])
def update_file():
    f = request.files['file']
    print(request.headers)
    file_path = 'upload/%s.png' % datetime.utcnow()
    f.save(file_path)
    return "is ok"


@app.route('/', methods=['GET'])
def index():
    return 'hello flask'



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)


