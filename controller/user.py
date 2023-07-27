import hashlib
import json
import re
from flask import Blueprint, make_response, session, request
from common.email_utils import gen_email_code, send_email, send_registed_email
from common.response_message import UserMessage
from common.utils import ImageCode
from model.user import User

user = Blueprint('user', __name__)


@user.route('/vcode')
def vcode():
    code, imbstring = ImageCode().get_code()
    response = make_response(imbstring)
    response.headers['Content-Type'] = 'image/jpeg'
    # 存起來，暫存到session里
    session['vcode'] = code.lower()
    # print('圖片驗證碼', code.lower())
    return response


@user.route('/ecode', methods=['POST'])
def email_code():
    # email = request.form.get('email')
    email = json.loads(request.data).get('email')
    emailReg = '^\w{2,}\@\w{2,}\.[a-z]{2,4}(\.[a-z]{2,4})?$'
    if not re.match(emailReg, email):
        return UserMessage.other('無效的Email')
    email_code = gen_email_code()
    print('ecode:', email_code)
    # 發送郵件
    try:
        send_email(email, email_code)
        session['ecode'] = email_code.lower()
        return UserMessage.success('sentcode')
    except:
        return UserMessage.fail('ecodefail')


@user.route('/reg', methods=['POST'])
def register():
    request_data = json.loads(request.data)
    username = request_data.get('username')
    password = request_data.get('password')
    ecode = request_data.get('ecode')

    # username是否已存在
    user = User()
    user_find_result = user.find_by_username(username)
    # print('user:', user_result)
    if user_find_result:
        return UserMessage.fail('exist')


    # 數據驗證
    if ecode != session.get('ecode'):
        print(ecode, session.get('ecode'))
        return UserMessage.fail('ecodefail')

    # username / password
    emailReg = '^\w{2,}\@\w{2,}\.[a-z]{2,4}(\.[a-z]{2,4})?$'
    if not re.match(emailReg, username):
        return UserMessage.other('無效的Email')

    pwdReg = '^\w{6,}'
    if not re.match(pwdReg, password):
        return UserMessage.fail('密碼不合法')

    # 註冊功能
    password = hashlib.md5(password.encode()).hexdigest()
    try:
        new_user = user.do_register(username, password)
        if new_user:
            registed_username = new_user.username
            # 發註冊成功信給registed_user
            send_registed_email(registed_username)
        return UserMessage.success('added')
    except:
        return UserMessage.fail('fail')


@user.route('/chkuser', methods=['POST'])
def chkuser():
    request_data = json.loads(request.data)
    username = request_data.get('username')
    # username
    emailReg = '^\w{2,}\@\w{2,}\.[a-z]{2,4}(\.[a-z]{2,4})?$'
    if not re.match(emailReg, username):
        return UserMessage.other('無效的Email')

    # username是否已存在
    user = User()
    user_find_result = user.find_by_username(username)
    # print('user:', user_result)
    if user_find_result:
        return UserMessage.fail('exist')
    return UserMessage.success('ok')





