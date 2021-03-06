from flask_restful import Resource, marshal_with, abort
from helpers import helpers
from models.all_models import TaskModel, db, OwnerModel
from flask_jwt import jwt_required
import datetime


def get_task_by_id(task_id):
    task_by_id = TaskModel.query.get(task_id)
    if task_by_id:
        return task_by_id
    else:
        return abort(404, message="Task not available")


def user_updating_id(user_id):
    user_up_id = OwnerModel.query.get(user_id)
    if user_up_id:
        return user_up_id
    else:
        return False


class AllTasks(Resource):
    @marshal_with(helpers.resource_fields)
    def get(self):
        all_tasks = TaskModel.query.all()
        tasks = []
        for t in all_tasks:
            task = {"id": t.id, "owner_id": t.owner_id, "task_owner_name": t.owner.owner_name, "task_name": t.task_name,
                    "task_priority": t.task_priority, "task_status": t.task_status, "date_created": t.date_created,
                    "due_date": t.due_date}
            tasks.append(task)
        return tasks, 200

    @jwt_required()
    @marshal_with(helpers.resource_fields)
    def post(self):
        args = helpers.task_args.parse_args()
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
    @marshal_with(helpers.resource_fields)
    def get(self, task_status):
        tasks = TaskModel.query.filter_by(task_status=task_status).all()

        if len(tasks) < 1:
            return abort(404, message=f'Tasks with {task_status} status not available')
        else:
            return tasks, 200


class AllTasksByPriority(Resource):
    @marshal_with(helpers.resource_fields)
    def get(self,task_priority):
        tasks = TaskModel.query.filter_by(task_priority=task_priority).all()

        if len(tasks) < 1:
            return abort(404, message=f'Tasks with {task_priority} priority not available')
        else:
            return tasks, 200


class AllTasksDue(Resource):
    @marshal_with(helpers.resource_fields)
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
    @marshal_with(helpers.resource_fields)
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
    @marshal_with(helpers.resource_fields)
    def put(self, task_id):
        args = helpers.updated_args.parse_args()
        task_to_update = get_task_by_id(task_id)
        if task_to_update.owner_id != args['owner_id']:
            return abort(404, message="Not Authorized")
        print(args['owner_id'])
        print(task_to_update.owner_id)

        if task_to_update:
            updated_date = args["due_date"].split("-")
            task_to_update.owner_id = args['owner_id']
            task_to_update.task_name = args['task_name']
            task_to_update.task_status = args['task_status']
            task_to_update.task_priority = args['task_priority']
            task_to_update.due_date = datetime.date(int(updated_date[0]),
                                                        int(updated_date[1]), int(updated_date[2]))
            db.session.commit()
            return task_to_update, 200


class AllSingleUserTasks(Resource):
    @marshal_with(helpers.resource_fields)
    def get(self,owner_id):
        user_tasks = TaskModel.query.filter_by(owner_id=owner_id).all()
        if user_tasks:
            return user_tasks, 200
        else:
            return abort(404, message="That User has no tasks")









