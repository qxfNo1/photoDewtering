import hashlib
import math
import os
from flask import Blueprint, session, make_response, request, redirect, url_for, render_template,current_app
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import base64
import io
import torch
import numpy as np
import random
import sys
from app.module.comment import Comment
sys.path.append("..")

import networks
deleteObjects = Blueprint('deleteObjects',__name__)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=2335, help='web service port')
parser.add_argument('--maxsize', type=int, default=2048)
parser.add_argument('--nogpu', action='store_true')
parser.add_argument('--opt', default='', type=str)
parser.add_argument('--load', default='', type=str)
parser.add_argument('--load1', default='../files/directory/model_256.pth', type=str)
parser.add_argument('--load2', default='../files/directory/model_near512.pth', type=str)
args = parser.parse_args()


UPLOAD_FOLDER = 'resource/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'jpeg', 'bmp'])

imgPath = UPLOAD_FOLDER
max_size = args.maxsize
use_gpu = not args.nogpu
device = torch.device("cuda:0") if use_gpu else torch.device("cpu")

if len(args.opt)>0 and len(args.load)>0:
    net = getattr(networks, args.opt).InpaintGenerator()
    net.load_state_dict(torch.load(args.load))
    net = net.to(device)
    net1 = net
    net2 = net
else:
    net = None
    net1 = networks.convnet.InpaintGenerator()
    net1.load_state_dict(torch.load(args.load1))
    # net1 = net1.to(device)
    net2 = networks.nearestx2.InpaintGenerator()
    net2.load_state_dict(torch.load(args.load2))
    # net2 = net2.to(device)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_image(img, msk, name, save_to_input=True):
    img =img.convert("RGB")
    img_raw = np.array(img)
    w_raw, h_raw = img.size
    if min(w_raw, h_raw)>=512:
        net = net2
    else:
        net = net1

    h_t, w_t = h_raw//8*8, w_raw//8*8

    img = img.resize((w_t, h_t))
    img = np.array(img)
    img = torch.Tensor(img.transpose((2,0,1)))[None,...]/255.0
    img = (img-0.5)/0.5
    msk_raw = np.array(msk)[...,None]>0
    msk = msk.resize((w_t, h_t))

    msk = np.array(msk)
    msk = (msk>0)[...,None]
    msk = torch.Tensor(msk.transpose((2,0,1)))[None,...]

    # img = img.to(device)
    # msk = msk.to(device)

    with torch.no_grad():
        _, result = net(img*(1-msk), msk)
        result = result*msk+img*(1-msk)
        result = result*0.5+0.5
    result = result.detach().cpu()[0].numpy()*255
    result = result.transpose((1,2,0)).astype(np.uint8)
    result = Image.fromarray(result).resize((w_raw, h_raw))
    result = np.array(result)
    result = result*msk_raw + img_raw*(1-msk_raw)
    result = Image.fromarray(result.astype(np.uint8))
    result.save(f"resource/results/{name}")
    if save_to_input:
        result.save(f"resource/images/{name}")

@deleteObjects.route('/deleteObjects', methods=['GET', 'POST'])
def deleteObject(name=None):

    method = 1

    #返回当前方法的评论列表
    comment_list = Comment().get_comment_user_list(1, 0, 5)
    #统计评论的总数
    count = Comment().get_count_by_method(1)
    total = math.ceil(count / 1)

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image = Image.open(file)
                W, H = image.size
                if max(W, H) > max_size:
                    ratio = float(max_size) / max(W, H)
                    W = int(W*ratio)
                    H = int(H*ratio)
                    image = image.resize((W, H))
                    filename = "resize_"+filename
                image.save(os.path.join(imgPath, filename))
                return render_template('deleteObjects.html', name=name, image_name=filename, image_width=W, image_height=H,comment_list=comment_list,total=total,method=method)
            else:
                filename='example.jpg'
                image = Image.open(os.path.join(imgPath, filename))
                W, H = image.size
                return render_template('deleteObjects.html', name=name, image_name=filename, image_width=W, image_height=H, is_alert=True,comment_list=comment_list,total=total,method=method)
        if 'mask' in request.form:
            filename = request.form['imgname']
            mask_data = request.form['mask']
            mask_data = mask_data.replace('data:image/png;base64,', '')
            mask_data = mask_data.replace(' ', '+')
            mask = base64.b64decode(mask_data)
            maskname = '.'.join(filename.split('.')[:-1]) + '.png'
            maskname = "{}_{}".format(random.randint(0, 1000), maskname)
            with open(os.path.join('resource/masks', maskname), "wb") as fh:
                fh.write(mask)
            mask = io.BytesIO(mask)
            mask = Image.open(mask).convert("L")
            image = Image.open(os.path.join(imgPath, filename))
            W, H = image.size
            process_image(image, mask, "result_"+maskname, save_to_input=True)
            return render_template('deleteObjects.html', name=name, image_name0=filename, image_name="result_" + maskname, mask_name=maskname, image_width=W, image_height=H,comment_list=comment_list,total=total,method=method)
    else:
        filename='example01.png'
        image = Image.open(os.path.join(os.path.join(imgPath, filename)))
        W, H = image.size
        return render_template('deleteObjects.html', name=name, image_name=filename, image_width=W, image_height=H,comment_list=comment_list,total=total,method=method)
