import sys
sys.path.append("..")
import networks
from flask import Flask, abort, render_template
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()    # ModuleNotFoundError: No module named 'MySQLdb'

app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)
# 使用集成方式处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/photoeraser?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True: 跟踪数据库的修改，及时发送信号
# 实例化db对象
db = SQLAlchemy(app)

# 定义404错误页面
@app.errorhandler(404)
def server_error(e):
    return render_template('error-404.html')

# 定义500错误页面
@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')

@app.route('/error')
def error_500():
    try:
        x = 10 / 0
        return x
    except:
        return abort(500)

# 第二种方式：按照标准的函数调用的方式进行
def getmethod():
    method = {'1': '图片去水印', '2': '删除物体', '3': '图片编辑','4': '视频去水印'}
    return method
app.jinja_env.globals.update(mymethod=getmethod)

# 自定义模板页面的过滤器
def mylen(str):
    return len(str)
app.jinja_env.filters.update(mylen=mylen)


if __name__ == "__main__":
    from app.controller.index import *
    app.register_blueprint(index)

    from app.controller.user import *
    app.register_blueprint(user)


    from app.controller.photoDewatering import *
    app.register_blueprint(photoDewatering)

    from app.controller.deleteObjects import *
    app.register_blueprint(deleteObjects)

    from app.controller.photoEditor import *
    app.register_blueprint(photoEditor)

    from app.controller.videoDewatering import *
    app.register_blueprint(videoDewatering)

    app.run(host='127.0.0.1', debug=True)#, port=443, threaded=True)

