from flask_restful import fields, reqparse

resource_fields_user = {
    "id": fields.Integer,
    "owner_name": fields.String,
    "username": fields.String,
    "password": fields.String
}

resource_fields = {
    "id": fields.Integer,
    "owner_id": fields.Integer,
    "task_name": fields.String,
    "task_priority": fields.String,
    "task_status": fields.String,
    "date_created": fields.DateTime(dt_format='iso8601'),
    "due_date": fields.DateTime(dt_format='iso8601') #dt_format='rfc822'
}


user_args = reqparse.RequestParser()

task_args = reqparse.RequestParser()
updated_args = reqparse.RequestParser()

user_args.add_argument("owner_name", type=str, help="Name cannot be blank", required=True)
user_args.add_argument("username", type=str, help="Name cannot be blank",required=True)
user_args.add_argument("password", type=str, help="Name cannot be blank", required=True)

task_args.add_argument("owner_id", type=int, help = "Owner id cannot be blank",required=True)
task_args.add_argument("task_name", type=str, help = "Task name cannot be blank",required=True)
task_args.add_argument("task_priority", type=str, help = "Task Priority cannot be blank",required=True)
task_args.add_argument("task_status", type=str, help = "Task Status cannot be blank",required=True)
task_args.add_argument("due_date", type=str, help = "Due Date cannot be blank",required=True)

updated_args.add_argument("owner_id", type=int, help = "Task name cannot be blank", required=True)
updated_args.add_argument("task_name", type=str, help = "Task name cannot be blank",required=True)
updated_args.add_argument("task_priority", type=str, help = "Task Priority cannot be blank",required=True)
updated_args.add_argument("task_status", type=str, help = "Task Status cannot be blank",required=True)
updated_args.add_argument("due_date", type=str, help = "Due Date cannot be blank",required=True)





