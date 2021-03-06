import os
from datetime import timedelta
from configparser import ConfigParser
from flask_restful import Api
from flask_jwt import JWT
from resources.all_tasks import (AllTasks, SingleTask, AllTasksByStatus,
                                 AllTasksByPriority, AllTasksDue, AllSingleUserTasks)
from resources.users import Users, User
from models.all_models import app
from flask import jsonify
from security import authenticate, identity as identity_function

config = ConfigParser()
config.read('config.ini')
app.secret_key = os.environ.get('SECRETE_KEY')
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id,
        'name': identity.owner_name
    })


api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/user/<int:user_id>')
api.add_resource(AllTasks, '/api/tasks')
api.add_resource(AllTasksDue, '/api/tasks/overdue')
api.add_resource(AllTasksByStatus, '/api/status/<string:task_status>')
api.add_resource(AllTasksByPriority, '/api/priority/<string:task_priority>')
api.add_resource(SingleTask, '/api/task/<int:task_id>')
api.add_resource(AllSingleUserTasks, '/api/tasks/user/<int:owner_id>')


if __name__ == '__main__':
    app.run()