from flask import request, jsonify
from datetime import datetime, timedelta
from models.Task import Task


def create_task():
        print("Received request for creating task")
        try:
            user_id = request.user['id']
            user_role = request.user['role']

            if user_role != 'user':
                return jsonify({'message': 'Unauthorized, only user can create tasks'}), 403

            completion_date = datetime.strptime(request.json['date'], '%Y-%m-%d')
            del request.json['date']
            task = Task(userId=user_id, date=completion_date, **request.json)
            save_task = task.save()
            return jsonify({'task': save_task.to_dict()}), 201
        except Exception as e:
            print(f"Error creating task: {e}")
            return jsonify({'error': str(e)}), 500
    
def update_task(task_id):
    try:
        task_data = request.json
        task = Task.objects(id=task_id).first()

        if task:
            allowed_fields = ['userId', 'type', 'status', 'name', 'date', 'time']
            for field in allowed_fields:
                if field in task_data:
                    setattr(task, field, task_data[field])

            task.save()

            return jsonify({'task': task.reload().to_dict()}), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def get_task(task_id):
    try:
        task = Task.objects(id=task_id).first()

        if task:
            return jsonify({'task': task.to_dict()}), 201
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_tasks():
    try:
        type_param = request.args.get('type')
        day = request.args.get('day')
        user_id = request.user.id

        min_date, max_date = None, None

        if day == 'today':
            min_date = max_date = datetime.now().strftime('%Y-%m-%d')
        elif day == 'seven':
            min_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            max_date = datetime.now().strftime('%Y-%m-%d')
        elif day == 'thirty':
            min_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            max_date = datetime.now().strftime('%Y-%m-%d')

        query_params = {'userId': user_id}

        if type_param:
            query_params['type'] = type_param

        if day:
            query_params['date__lte'] = max_date
            query_params['date__gte'] = min_date

        tasks = Task.objects(**query_params)

        tasks_list = [task.to_dict() for task in tasks if isinstance(task, Task)]

        return jsonify({'tasks': tasks_list}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_task(task_id):
    try:
        deleted_task = Task.objects(id=task_id).first()

        if deleted_task:
            deleted_task.delete()
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500