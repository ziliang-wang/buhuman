import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config.config import config
from app.settings import env


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
