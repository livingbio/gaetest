# based on http://stackoverflow.com/questions/6632809/gae-unit-testing-taskqueue-with-testbed/6635947#6635947

import pickle, base64

def execute_tasks(testapp, taskq, queue_name):
    """
    Executes all currently queued tasks, and also removes them from the
    queue.
    The tasks are execute against the provided web application.
    """

    tasks = taskq.GetTasks(queue_name)
    # Get all of the tasks, and then clear them.
    taskq.FlushQueue(queue_name)

    # Run each of the tasks, checking that they succeeded.
    for task in tasks:
        if 'params' in task:
            response = testapp.post(task['url'], task['params'])
        else:
            # defer
            func, args, opts = pickle.loads(base64.b64decode(task['body']))
            func(*args)


