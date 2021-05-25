from flask import Blueprint, session, make_response, request, redirect, url_for, render_template,current_app

videoDewatering = Blueprint('videoDewatering',__name__)

@videoDewatering.route('/videoDewatering')
def editor():
    return render_template('videoDewatering.html')

