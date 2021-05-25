from flask import Blueprint, request, session, jsonify
from app.module.comment import Comment
from app.module.opinion import Opinion
from app.module.users import Users
from app.module.credit import Credit

comment = Blueprint('comment',__name__)


@comment.before_request
def before_comment():
    if session.get('islogin') is None or session.get('islogin') != 'True':
        return "not-login"

@comment.route('/comment',methods=['POST'])
def add():
    method = request.form.get('method')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr


    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment = Comment()

    if not comment.check_limit_per_5():
        try:
            comment.insert_comment(method,content,ipaddr)
            Credit().insert_detail(type='添加评论',target=method,credit=2)
            Users().update_credit(2)

            return 'add-pass'
        except:
            return 'add-fail'

    else:
        return 'add-limit'



@comment.route('/reply',methods=['POST'])
def reply():
    method = request.form.get('method')
    commentid = request.form.get('commentid')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr

    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment = Comment()
    if not comment.check_limit_per_5():
        try:
            comment.insert_reply(method=method,commentid=commentid,content=content,ipaddr=ipaddr)
            Credit().insert_detail(type='回复评论',target=method,credit=2)
            Users().update_credit(2)

            return 'reply-pass'
        except:
            return 'reply-fail'

    else:
        return 'reply-limit'

@comment.route('/comment/<int:method>-<int:page>')
def comment_page(method,page):
    start = (page-1)
    comment = Comment()
    list = comment.get_comment_user_list(method,start,5)
    return jsonify(list)


@comment.route('/opinion',methods=['POST'])
def do_opinion():
    commentid = request.form.get('commentid')
    type = int(request.form.get('type'))
    ipaddr = request.remote_addr


    opinion = Opinion()
    is_checked = opinion.check_opinion(commentid,ipaddr)
    if is_checked:
        return 'already-opinion'

    else:
        opinion.insert_opinion(commentid,type,ipaddr)
        Comment().update_agree_oppose(commentid,type)
        return 'opinion-pass'
