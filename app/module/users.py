import random
import time

from flask import session
from sqlalchemy import Table
from app.common.database import dbconnect

dbsession,md,DBase = dbconnect()


class Users(DBase):
    __table__ = Table('users',md,autoload = True)


    #查询用户名，可用于注册是判断新用户名是否已注册，也可用于登陆校验
    def find_by_username(self,username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result

    #实现注册

    def do_register(self,username,password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]
        avatar = str(random.randint(1,15))
        user = Users(username=username,password=password,role = 'user',credit=50,
                    nickname=nickname,avatar=avatar + '.png',createtime = now,updatetime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    def update_credit(self,credit):
        user = dbsession.query(Users).filter_by(userid = session.get('userid')).one()
        user.credit = int(user.credit) +credit
        dbsession.commit()





