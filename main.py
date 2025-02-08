import json
from datetime import datetime
import os


file_name = "tasks.json"
def add_task(task_name):
    tasks = []
    tasks_count = 0
    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        with open(file_name, "r") as file:
            try:
                content = json.load(file)
                if content:
                    tasks = content['tasks']
                    tasks_count = len(content['tasks'])
            except json.JSONDecodeError:
                print("Invalid JSON format.")            
    else:
        print("file doesn't extsits")
        
    with open(file_name,"w") as file:
        task = {
            "id": tasks_count+1,
            "description" : task_name,
            "status":"todo",
            "created_at":f"{datetime.now()}",
            "updated_at":f"{datetime.now()}"
        }
        tasks.append(task)
        data = {}
        data ['tasks_count'] = len(tasks)
        data['tasks'] = tasks
        json.dump(data,file,indent=4)
        print("Task added succefully\n")
    
def update_task(task_id,task_name):
    with open(file_name,"r") as file:
        data = json.load(file)
        tasks = data['tasks']
        try:
            tasks[int(task_id)-1]['description'] = task_name
            with open(file_name,"w") as file:
                data['tasks'] = tasks
                data ['tasks_count'] = len(tasks)
                json.dump(data,file,indent=4)
                print("Task updated succefully\n")
        except IndexError:
            print("There is no task with the given ID\n")
    
def delete_task(task_id):
    with open(file_name,"r") as file:
        data = json.load(file)
        tasks = data['tasks']
        try:
            tasks.pop(int(task_id))
            with open(file_name,"w") as file:
                data['tasks'] = tasks
                data ['tasks_count'] = len(tasks)
                json.dump(data,file,indent=4)
                print("Task removed succefully\n")
        except IndexError:
            print("There is no task with the given ID\n")


def list_task():
    with open(file_name,"r") as file:
        data = json.load(file)
        tasks = data['tasks']
        print("\n")
        for task in tasks:
            print(f"{task['description']}    \tstatus : {task['status']}\n")

def list_by_status(status):
    with open(file_name,"r") as file:
        data = json.load(file)
        tasks = data['tasks']
        print("\n")
        for task in tasks:
            if task['status'] == status:
                print(f"{task['description']}    \tstatus : {task['status']}\n")

def mark_status(status,task_id):
    with open(file_name,"r") as file:
        data = json.load(file)
        tasks = data['tasks']
        try:
            tasks[int(task_id)-1]['status'] = status
            with open(file_name,"w") as file:
                data['tasks'] = tasks
                data ['tasks_count'] = len(tasks)
                json.dump(data,file,indent=4)
                print("Task updated succefully\n")
        except IndexError:
            print("There is no task with the given ID\n")



while True:
    print("######################################## Task Tracker ########################################\n\n")
    print("To Interact with the program use these commands:\n")
    print("1- To create a new task use add task_name\n")
    print("1- To update an existing  task use update task_id task_name\n")
    print("1- To delete an existing  task use delete task_id \n")
    print("2- To list all tasks use list\n")
    print("3- To list  tasks that are done use list done\n")
    print("4- To list tasks that are not done use list todo\n")
    print("5- To list  tasks that are in progress use list in-progress\n")
    print("6- To mark a task as done use mark status task_id\n")
    print("7- To quit the program use quit\n")

    command = input("")
    if command:
        args = command.split(" ")

        if args[0] == 'add':
            description = ' '.join(args[1:]).strip(' \" ')
            if description:
                add_task(description)
            else:
                print("Task name not found")
        elif args[0] == 'update':
            description = ' '.join(args[2:]).strip(' \" ')
            if description:
                update_task(args[1],description)
            else:
                print("Task name not found")
        elif args[0] == 'delete':
            delete_task(args[1])
        elif args[0] == 'list':
            try:
                list_by_status(args[1])
            except IndexError:
                list_task()
        elif args[0] == 'mark':
            try:
                mark_status(args[1],args[2])
            except IndexError:
                print("Wrong command\n")
        elif args[0] == 'quit':
            break
        else:
            print("Wrong command\n")