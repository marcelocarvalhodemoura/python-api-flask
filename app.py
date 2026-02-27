from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() #recebe os dados em json
    task_id = len(tasks) + 1 #gera um id para a tarefa
    task = Task(
        task_id, 
        data['title'], 
        data['description']
    ) #cria a tarefa
    tasks.append(task) #adiciona a tarefa na lista
    return jsonify(task.to_dict()) #retorna a tarefa em json

@app.route('/tasks', methods=['GET']) #rota para listar as tarefas
def get_tasks():
    tasks_list = [ task.to_dict() for task in tasks ] #cria uma lista de tarefas
    
    output = { #cria um dicionario com as tarefas e o total de tarefas
        "tasks": tasks_list,
        "total_tasks": len(tasks)
    }
    
    return jsonify(output) #retorna as tarefas em json

@app.route('/tasks/<int:id>', methods=['GET']) #rota para listar uma tarefa
def get_task(id): #recebe o id da tarefa
    task = next((task for task in tasks if task.id == id), None) #busca a tarefa na lista
    if task:
        return jsonify(task.to_dict()) #retorna a tarefa em json
    else:
        return jsonify({"message": "Task not found"}), 404 #retorna uma mensagem de erro

@app.route('/tasks/<int:id>', methods=['PUT']) #rota para atualizar uma tarefa
def update_task(id): #recebe o id da tarefa
    task = next((task for task in tasks if task.id == id), None) #busca a tarefa na lista
    if task:
        data = request.get_json() #recebe os dados em json
        task.title = data['title'] #atualiza o titulo da tarefa
        task.description = data['description'] #atualiza a descricao da tarefa
        task.completed = data['completed'] #atualiza o status da tarefa
        return jsonify(task.to_dict()) #retorna a tarefa em json
    else:
        return jsonify({"message": "Task not found"}), 404 #retorna uma mensagem de erro

@app.route('/tasks/<int:id>', methods=['DELETE']) #rota para deletar uma tarefa
def delete_task(id): #recebe o id da tarefa
    task = next((task for task in tasks if task.id == id), None) #busca a tarefa na lista
    if task:
        tasks.remove(task) #remove a tarefa da lista
        return jsonify({"message": "Task deleted successfully"}) #retorna uma mensagem de sucesso
    else:
        return jsonify({"message": "Task not found"}), 404 #retorna uma mensagem de erro

@app.route('/tasks/<int:id>', methods=['PATCH']) #rota para marcar uma tarefa como concluida
def update_task_status(id): #recebe o id da tarefa
    task = next((task for task in tasks if task.id == id), None) #busca a tarefa na lista
    if task:
        task.completed = True #marca a tarefa como concluida
        return jsonify(task.to_dict()) #retorna a tarefa em json
    else:
        return jsonify({"message": "Task not found"}), 404 #retorna uma mensagem de erro

if __name__ == '__main__':
    app.run(debug=True) #inicia o servidor