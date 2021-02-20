from models.all_models import OwnerModel
from resources.users import bcrypt


def authenticate(username, password):
    user = OwnerModel.find_by_username(username)
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return OwnerModel.find_by_id(user_id)
