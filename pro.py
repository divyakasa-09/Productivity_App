from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory task storage (for simplicity; use a database for production)
tasks = []

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'due_date': data.get('due_date'),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Route to list all tasks
@app.route('/tasks', methods=['GET'])
def list_tasks():
    return jsonify(tasks), 200

# Route to update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update({
                'title': data.get('title', task['title']),
                'description': data.get('description', task['description']),
                'due_date': data.get('due_date', task['due_date']),
                'completed': data.get('completed', task['completed'])
            })
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

# Route to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
