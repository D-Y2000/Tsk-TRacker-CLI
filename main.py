import json
from datetime import datetime
import os


file_name = "tasks.json"
status_list = ['done', 'to-do' , 'in-progress']

def display_menu():
    print("######################################## Task Tracker ########################################\n\n")
    print("To Interact with the program use these commands:\n")
    print("1- To create a new task use add task_name\n")
    print("1- To update an existing  task use update task_id task_name\n")
    print("1- To delete an existing  task use delete task_id \n")
    print("2- To list all tasks use list\n")
    print("3- To list  tasks that are done use list done\n")
    print("4- To list tasks that are not done use list todo\n")
    print("5- To list  tasks that are in progress use list in-progress\n")
    print(f"6- To mark a task as done use mark status = [done, to-do , in-progress] task_id\n")
    print("7- To quit the program use quit\n")



def load_data():
    tasks = []
    #  check if the file exists and is not empty.
    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        with open(file_name, "r") as file:
            try:
                content = json.load(file)
                if content:
                    tasks = content['tasks']
            except json.JSONDecodeError:
                print("Invalid JSON format.")            
    return tasks

def add_task(task_name):
    # Load the existing data
    tasks = load_data()
    # fetch tasks count in order to set the correct id for the new task
    tasks_count = len(tasks)
    task = {
        "id": tasks_count+1,
        "description" : task_name,
        "status":"to-do",
        "created_at":f"{datetime.now().strftime('%Y/%m/%d  %H:%M:%S')}",
        "updated_at":f"{datetime.now().strftime('%Y/%m/%d  %H:%M:%S')}"
    }
    tasks.append(task)
    save_edits(tasks)
    print("Task added succefully\n")
    
def update_task(task_id,task_name):
    tasks =  load_data()
    try:
        tasks[int(task_id)-1]['description'] = task_name
        tasks[int(task_id)-1]["updated_at"] = f"{datetime.now().strftime('%Y/%m/%d  %H:%M:%S')}"
        save_edits(tasks)
        print("Task updated succefully\n")
    except IndexError:
        print("There is no task with the given ID\n")

def delete_task(task_id):
    tasks = load_data()
    try:
        tasks.pop(int(task_id))
        save_edits(tasks)
        print("Task removed succefully\n")
    except IndexError:
        print("There is no task with the given ID\n")


def list_task():
    tasks = load_data()
    print("\n")
    if len(tasks) > 0  :
        print("Tasks List : \n")
        for task in tasks:
            print(f"{task['id']} \t{task['description']}    \tstatus : {task['status']}\n")
    else:
        print("There is no task")

def list_by_status(status):
    if status in status_list:
        tasks = load_data()
        print("\n")
        print("Tasks list :\n")
        for task in tasks:
            if task['status'] == status:
                 print(f"{task['id']} \t{task['description']}    \tstatus : {task['status']}\n")
    else:
        print("Wrong command\n")

def mark_status(status,task_id):
    print(f"status : {status}")
    tasks = load_data()
    print("\n")
    # check if the given status is correct
    if status in status_list:
        try:
            tasks[int(task_id)-1]['status'] = status
            tasks[int(task_id)-1]["updated_at"] = f"{datetime.now().strftime('%Y/%m/%d  %H:%M:%S')}"
            save_edits(tasks)
            print("Task updated succefully\n")
        except IndexError:
            print("There is no task with the given ID\n")
    else:
        print("Wrong command\n")


def save_edits(tasks):
    data = {}
    data['tasks'] =   tasks
    data['tasks_count'] = len(tasks)
    with open(file_name,"w") as file:
        json.dump(data,file,indent=4)

while True:

    display_menu()

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