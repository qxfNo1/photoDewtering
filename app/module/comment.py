from flask import session,request
from sqlalchemy import Table
from app.common.database import dbconnect
import time

from app.common.utility import model_join_list
from app.module.users import Users
# from common.utility import model_join_list

dbsession,md,DBase = dbconnect()

class Comment(DBase):
    __table__ = Table("comment",md,autoload=True)

    #新增一条评论
    def insert_comment(self,method,content,ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid = session.get('userid'),method = method,
                          content=content,ipaddr=ipaddr,createtime =now,updatetime=now)
        dbsession.add(comment)
        dbsession.commit()

    # #新增一条回复
    # def insert_reply(self,articleid,commentid,content,ipaddr):
    #     now = time.strftime('%Y-%m-%d %H:%M:%S')
    #     comment = Comment(userid=session.get('userid'), articleid=articleid,
    #                       content=content, ipaddr=ipaddr,replyid=commentid,
    #                       createtime=now, updatetime=now)
    #     dbsession.add(comment)
    #     dbsession.commit()

    def find_by_method(self,method):
        result = dbsession.query(Comment).filter_by(method=method,hidden=0,replyid = 0).all()
        return result


    def check_limit_per_5(self):

        start = time.strftime('%Y-%m-%d 00:00:00')

        end = time.strftime('%Y-%m-%d 23:59:59')

        result = dbsession.query(Comment).filter(Comment.userid == session.get('userid'),
                                                 Comment.createtime.between(start,end)).all()
        if len(result) >= 10:
            return True
        else:
            return False


    def find_limit_with_user(self,method,start,count):
        result = dbsession.query(Comment,Users).join(Users,Users.userid == Comment.userid)\
            .filter(Comment.method == method)\
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()

        return result


    def insert_reply(self,method,commentid,content,ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'),method=method,
                  content=content,ipaddr=ipaddr,replyid=commentid,createtime=now,updatetime=now)
        dbsession.add(comment)
        dbsession.commit()

    #查原始评论
    def find_comment_with_user(self,method,start,count):
        result = dbsession.query(Comment,Users).join(Users,Users.userid == Comment.userid).filter(Comment.method == method,Comment.replyid == 0,Comment.hidden == 0)\
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result

    #查回复评论
    def find_reply_with_user(self,replyid):
        result = dbsession.query(Comment,Users).join(Users,Users.userid == Comment.userid).filter(Comment.replyid == replyid,Comment.replyid != 0,Comment.hidden == 0).all()
        return result



     #获取
    def get_comment_user_list(self,method,start,count):
        result = self.find_comment_with_user(method,start,count)
        print('result',result)
        comment_list = model_join_list(result)
        for comment in comment_list:
            result = self.find_reply_with_user(comment['commentid'])

            comment['reply_list'] = model_join_list(result)

        return comment_list

    def get_count_by_method(self,method):
        count = dbsession.query(Comment).filter_by(method=method,hidden=0,replyid=0).count()
        return count

    def update_agree_oppose(self, commentid, type):
        row = dbsession.query(Comment).filter_by(commentid=commentid).first()
        if type == 1:
            row.agreecount += 1

        elif type == 0:
            row.opposecount += 1
        dbsession.commit()





