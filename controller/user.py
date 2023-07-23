from flask import Blueprint
from model.user import User

user = Blueprint('user', __name__)


@user.route('/user')
def get_one():
    user = User()
    result = user.get_one()
    print(result)
    print(result.username)

    return 'ok'