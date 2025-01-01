def task_serializer(task) -> dict:
    return {
        'task_id': str(task['_id']),
        'title': task['title'],
        'description': task['description'],
    }


def tasks_serializer(tasks) -> list:
    return [task_serializer(task) for task in tasks]