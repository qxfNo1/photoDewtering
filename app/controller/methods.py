
import math
import os
from flask import Blueprint, session, make_response, request, redirect, url_for, render_template,current_app
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io
import torch
import numpy as np
import random
from app.module.comment import Comment

methods = Blueprint('method',__name__)

@methods.route('/photoEditor')
def editor():
    return render_template('photoEditor.html')


@methods.route('/deleteObjects')
def delete_objects():
    render_template('deleteObjects.html')

@methods.route('/videoDewatering')
def delete_object():
    render_template('videoDewatering.html')

@methods.route('/')
def read():
    pass



@methods.route('/readall',methods=['POST','GET'])
def read_all():
   pass

