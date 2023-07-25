import json
import re
from flask import Blueprint, make_response, session, request
from common.email_utils import gen_email_code, send_email
from common.response_message import UserMessage
from common.utils import ImageCode

user = Blueprint('user', __name__)


@user.route('/vcode')
def vcode():
    code, imbstring = ImageCode().get_code()
    response = make_response(imbstring)
    response.headers['Content-Type'] = 'image/jpeg'
    # 存起來，暫存到session里
    session['vcode'] = code.lower()
    print(code.lower())
    return response


@user.route('/ecode', methods=['POST'])
def email_code():
    # email = request.form.get('email')
    email = json.loads(request.data).get('email')
    if not re.match('.+@.+\..+', email):
        return UserMessage.other('無效的Email')
    email_code = gen_email_code()
    print(email_code)
    # 發送郵件
    try:
        send_email(email, email_code)
        session['ecode'] = email_code.lower()
        return UserMessage.success('Email驗證碼發送成功')
    except:
        return UserMessage.fail('Email驗證碼發送失敗')


