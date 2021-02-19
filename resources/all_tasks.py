from flask_restful import Resource, fields, marshal_with, abort, reqparse
from models.all_models import TaskModel, db, OwnerModel
from flask_jwt import jwt_required
import datetime


resource_fields = {
    "id": fields.Integer,
    "owner_id": fields.Integer,
    "task_name": fields.String,
    "task_priority": fields.String,
    "task_status": fields.String,
    "date_created": fields.DateTime(dt_format='iso8601'),
    "due_date": fields.DateTime(dt_format='iso8601') #dt_format='rfc822'
}


task_args = reqparse.RequestParser()
updated_args = reqparse.RequestParser()

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


def get_task_by_id(task_id):
    task_by_id = TaskModel.query.get(task_id)
    if task_by_id:
        return task_by_id
    else:
        return abort(404, message="Task not available")


def user_updating_id(user_id):
    user_up_id = OwnerModel.query.get(user_id)
    return user_up_id

#
# class AllTasksAutoMail(Resource):
#     def get(self):
#         ts = TaskModel.query.all()
#         email_tasks = {}
#         for t in ts:
#             # print(t.owner.username)
#             # print(t.task_name)
#             # with open(f"{t.task_name}.txt", 'w', encoding='utf-8') as f:
#             #     f.write(f"{t.owner.username}\n")
#             #     f.write(f"{t.task_name}\n")
#         print(email_tasks)

        # users = [t.owner_id for t in tasks]
        # owners_emails = [OwnerModel.query.get(u).username for u in users]


class AllTasks(Resource):
    @marshal_with(resource_fields)
    def get(self):
        tasks = TaskModel.query.all()
        return tasks, 200

    @jwt_required()
    @marshal_with(resource_fields)
    def post(self):
        args = task_args.parse_args()
        owner_exists = OwnerModel.query.get(args['owner_id'])
        if owner_exists is None:
            return abort(404, message="User does not exists")

        task_exists = TaskModel.query.all()

        for task in task_exists:
            if task.task_name == args['task_name'] and task.owner_id == args['owner_id']:
                return abort(404, message=f"{task.task_name} already exists")

        if (args["task_status"] != "completed" and args["task_status"] != "in_progress"
                and args["task_status"] != "not_started"):
            return abort(404, message="Incorrect Status")

        if (args["task_priority"] != "high" and args["task_priority"] != "medium"
                and args["task_priority"] != "low"):
            return abort(404, message="Incorrect Priority")

        updated_date = args["due_date"].split("-")
        new_task = TaskModel(owner_id = args["owner_id"],task_name=args["task_name"],
                        task_status=args["task_status"], task_priority=args["task_priority"],
                        due_date = datetime.date(int(updated_date[0]),int(updated_date[1]),int(updated_date[2])))
        new_task.save_to_db()
        return new_task, 201


class AllTasksByStatus(Resource):
    @marshal_with(resource_fields)
    def get(self, task_status):
        tasks = TaskModel.query.filter_by(task_status=task_status).all()

        if len(tasks) < 1:
            return abort(404, message=f'Tasks with {task_status} status not available')
        else:
            return tasks, 200


class AllTasksByPriority(Resource):
    @marshal_with(resource_fields)
    def get(self,task_priority):
        tasks = TaskModel.query.filter_by(task_priority=task_priority).all()

        if len(tasks) < 1:
            return abort(404, message=f'Tasks with {task_priority} priority not available')
        else:
            return tasks, 200


class AllTasksDue(Resource):
    @marshal_with(resource_fields)
    def get(self):
        current = datetime.date.today()
        current = int(str(current).split("-")[2])
        tasks = TaskModel.query.all()
        due_tasks = []
        for over_due in tasks:
            due_date = (int(str(over_due.due_date).split("-")[2].split(" ")[0]))
            if current < due_date:
                due_tasks.append(over_due)
        return due_tasks, 200


class SingleTask(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        single_task = get_task_by_id(task_id)
        if single_task:
            return single_task, 200

    @jwt_required()
    def delete(self,task_id):
        task_to_delete = get_task_by_id(task_id)
        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()
            return {'message': 'Task deleted'}, 200

    @jwt_required()
    @marshal_with(resource_fields)
    def put(self, task_id):
        task_to_update = get_task_by_id(task_id)
        if task_to_update:
            args = updated_args.parse_args()
            updated_date = args["due_date"].split("-")
            task_to_update.owner_id = args['owner_id']
            task_to_update.task_name = args['task_name']
            task_to_update.task_status = args['task_status']
            task_to_update.task_priority = args['task_priority']
            task_to_update.due_date = datetime.date(int(updated_date[0]),
                                                        int(updated_date[1]), int(updated_date[2]))
            db.session.commit()
            return task_to_update, 200









