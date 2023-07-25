from flask import Blueprint, make_response, session

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
    print(code.lower())
    return response

# @user.route('/user')
# def get_one():
#     user = User()
#     result = user.get_one()
#     print(result)
#     print(result.username)
#
#     return 'ok'