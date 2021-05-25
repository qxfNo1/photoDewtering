from flask import Blueprint, session, make_response, request, redirect, url_for, render_template,current_app

photoEditor = Blueprint('photoEditor',__name__)



@photoEditor.route('/photoEditor')
def editor():
    return render_template('photoEditor.html')

