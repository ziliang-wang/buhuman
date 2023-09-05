import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config.config import config
from app.settings import env
import base64


def gen_email_code():
    list = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(list)


def send_email(email, email_code):
    sender = config[env].sender
    auth_code = config[env].auth_code
    msg_to = email
    content = f'''
        Your validation code is <strong style="color: red;">{ email_code }</strong>
    '''
    msg = MIMEMultipart()
    msg['Subject'] = '[Jomunn Service] Validation Code'
    # 昵称+空格+<邮箱地址>形式
    msg['From'] = f'Jomunn Service {sender}'
    msg['To'] = msg_to
    # 正文掛載
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(sender, auth_code)
    s.sendmail(sender, msg_to, msg.as_string())


def reset_send_email(email, email_code):
    sender = config[env].sender
    auth_code = config[env].auth_code
    msg_to = email
    username = base64.encodebytes(email.encode('utf-8')).decode('utf-8')
    print(username)
    # username = email.split('@')[0]
    content = f'''
        Your Reset Password-validation code is <strong style="color: red;">{ email_code }</strong>
        <br>
        Please visit http://localhost:5000/reset/password?u={username} to change your password
    '''
    msg = MIMEMultipart()
    msg['Subject'] = '[Jomunn Service] Reset Password-Email Validation Code'
    # 昵称+空格+<邮箱地址>形式
    msg['From'] = f'Jomunn Service {sender}'
    msg['To'] = msg_to
    # 正文掛載
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(sender, auth_code)
    s.sendmail(sender, msg_to, msg.as_string())


def send_registed_email(email):
    sender = config[env].sender
    auth_code = config[env].auth_code
    msg_to = email
    content = f'''
            註冊成功
        '''
    msg = MIMEMultipart()
    msg['Subject'] = '[Jomunn Service] 註冊成功通知'
    # 昵称+空格+<邮箱地址>形式
    msg['From'] = f'Jomunn Service {sender}'
    msg['To'] = msg_to
    # 正文掛載
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(sender, auth_code)
    s.sendmail(sender, msg_to, msg.as_string())
