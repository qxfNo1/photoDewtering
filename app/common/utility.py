import random,string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class ImageCode:
    #用于绘制字符串的随机颜色
    def rand_color(self):
        red = random.randint(32,200)
        green = random.randint(22,255)
        blue = random.randint(0,200)
        return red,green,blue

    #生成4位随机字符串
    def gen_text(self):
        list = random.sample(string.ascii_letters,4)
        return ''.join(list)

    def draw_verify_code(self):
        code=self.gen_text()
        width,height = 120,50 #设定图片大小，可根据实际需求调整
        #创建图片对象，并设定背景色为白色
        im = Image.new('RGB',(width,height),'white')

        #选择使用何种字体及字体大小
        font = ImageFont.truetype(font='arial.ttf',size=40)
        draw = ImageDraw.Draw(im)
        #绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3,3)+23*i,5+random.randint(-3,3)),
                      text=code[i],fill=self.rand_color(),font=font)
        self.draw_lines(draw,2,width,height)
        # im.show()
        return im,code

    #随机画干扰线
    def draw_lines(self,draw,num,width,height):
        for num in range(num):
            x1 = random.randint(0,width/2)
            y1 = random.randint(0,height/2)
            x2 = random.randint(0,width)
            y2 = random.randint(height/2,height)
            draw.line(((x1,y1),(x2,y2)),fill='black',width=2)


# ImageCode().draw_verify_code()

    #生成图片验证码并返回给控制器
    def get_code(self):
        image,code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf,'jpeg')
        bstring = buf.getvalue()
        return code,bstring

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def send_email(receiver,ecode):
    sender = '1812463693@qq.com'
    content = f"<br/>欢迎注册照片橡皮擦系统账号，您的邮箱验证码为："\
              f"<span style='color:red;font-size:20px;'>{ecode}</span>," \
              f"请复制到注册窗口中完成注册，感谢您的支持。<br/>"
    message = MIMEText(content,'html','utf-8')
    message['Subject'] = Header('照片橡皮擦的注册验证码','utf-8')
    message['From'] = sender
    message['To'] = receiver


    smtpObj = SMTP_SSL('smtp.qq.com')

    smtpObj.login(user = '1812463693@qq.com',password = 'lpkbesyypgvnecgf')
    smtpObj.sendmail(sender,receiver,str(message))
    smtpObj.quit()

#生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str= random.sample(string.ascii_letters + string.digits,6)
    return ''.join(str)

# code = gen_email_code()
# print(code)
# send_email('xiaofengQ@shu.edu.cn',code)
#


#单个模型类转换为标准的python list数据
def model_list(result):
    list = []
    for row in result:
        dict = {}
        for k, v in row.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                if not k in dict:
                    dict[k] = v

        list.append(dict)
    return list


def model_join_list(result):
    list = []

    for obj1,obj2 in result:
        dict = {}
        for k1,v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                if not k1 in dict:
                    dict[k1] = v1
        for k2,v2 in obj2.__dict__.items():
            if not k2.startswith('_sa_instance_state'):
                if not k2 in dict:
                    dict[k2] = v2

        list.append(dict)
    return list
