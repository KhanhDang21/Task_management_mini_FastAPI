from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException
from config.authentication import get_current_user
from config.database import task_collection
from models.task_model import Task
from schemas.task_shema import task_serializer, tasks_serializer

router = APIRouter(
    prefix="/api/task",
    tags=["Task"],
)


@router.get('')
def get_all_task():
    tasks = tasks_serializer(task_collection.find())
    return {
        'status': 200,
        'data': tasks,
    }


@router.get('/get_task/{task_id}')
def get_task(task_id: str, user=Depends(get_current_user)):
    if user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!',
        }

    this_task = task_serializer(task_collection.find_one({'_id': ObjectId(task_id)}))

    if this_task is None:
        return {
            'status': 404,
            'data': 'Task not found!',
        }

    return {
        'status': 200,
        'data': this_task,
    }


@router.post('/add_task')
def add_task(task: Task, user=Depends(get_current_user)):
    if user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!',
        }

    try:
        new_task = {
            'title': task.title,
            'description': task.description,
        }

        task_collection.insert_one(new_task)

        return {
            'status': 200,
            'data': 'Task added successfully',
        }
    except Exception as e:
        return {
            'status': 500,
            'error': str(e),
        }


@router.put('/update_task/{task_id}')
def update_task(task_id: str, task: Task, user=Depends(get_current_user)):
    if user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!',
        }

    this_task = task_collection.find_one({'_id': ObjectId(task_id)})

    if this_task is None:
        return {
            'status': 404,
            'data': 'Task not found',
        }

    try:
        task_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set':
                {
                    'title': task.title,
                    'description': task.description,
                }
            }
        )
        return {
            'status': 200,
            'data': 'Task updated successfully',
        }
    except Exception as e:
        return {
            'status': 500,
            'error': str(e),
        }


@router.delete('/delete_task/{task_id}')
def delete_task(task_id: str, user=Depends(get_current_user)):
    if user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!',
        }

    this_task = task_collection.find_one({'_id': ObjectId(task_id)})

    if this_task is None:
        return {
            'status': 404,
            'data': 'Task not found',
        }

    task_collection.delete_one({'_id': ObjectId(task_id)})

    return {
        'status': 200,
        'data': 'Task deleted successfully',
    }
