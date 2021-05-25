import math

from flask import Blueprint, session, request, render_template

from app.module.users import Users


index =Blueprint("index",__name__)

@index.route('/')
def home():

    return render_template('index.html')
