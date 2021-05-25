import hashlib

from flask import Blueprint, session, make_response, request, redirect, url_for
from app.common.utility import ImageCode, send_email, gen_email_code
import re

from app.module.credit import Credit
from app.module.users import Users

user = Blueprint('user',__name__)

@user.route('/vcode')
def vcode():
    code,bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response

@user.route('/ecode',methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match('.+@.+\..+',email):
        return 'email-invalid'
    code = gen_email_code()
    session['ecode'] = code
    try:
        send_email(email,code)
        return 'send-pass'
    except:
        return 'send-fail'

#实现注册功能
@user.route('/user',methods=['POST'])
def register():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()
    print('ecode:',ecode)
    print('get:',session.get('ecode'))



    if ecode != session.get('ecode'):
        return 'ecode-error'


    elif not re.match('.+@.+\..+',username) or len(password) < 5:
        return 'up-invalid'

    elif len(user.find_by_username(username))>0:
        return 'user-repeated'

    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result  = user.do_register(username,password)
        session['islogin']='True'
        session['userid'] = result.userid
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role

        #更新积分明细表
        Credit().insert_detail(type='用户注册',target = '0',credit=50)
        return 'reg-pass'



#实现登陆功能
@user.route('/login',methods=['POST'])
def login():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').strip()



    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'


    else:
        password = hashlib.md5(password.encode()).hexdigest()
        result  = user.find_by_username(username)
        if len(result) == 1 and result[0].password==password:
            session['islogin']='True'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role

            #更新积分明细表
            Credit().insert_detail(type='用户注册',target = '0',credit=1)
            user.update_credit(1)
            response = make_response('login-pass')
            response.set_cookie('username',username,max_age=30*24*3600)
            response.set_cookie('password',password,max_age=30*24*3600)

            return response
        else:
            return 'login-fail'

#实现登陆功能
@user.route('/logout')
def logout():
    session.clear()
    response = make_response('注销并进行重定向',302)
    response.headers['Location'] = url_for('index.home')
    response.delete_cookie('username')
    response.set_cookie('password',max_age=0)

    return response
