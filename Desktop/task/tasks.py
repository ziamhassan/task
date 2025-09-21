
import sys
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

def init_file():

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump({"last_id": 0, "tasks": []}, f)

def load_data():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_task(description):
    data = load_data()
    data["last_id"] += 1
    task = {
        "id": data["last_id"],
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now()
    }
    data["tasks"].append(task)
    save_data(data)
    print(f"Task added successfully (ID: {task['id']})")

def update_task(task_id, new_description):
    data = load_data()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = now()
            save_data(data)
            print(f"Task {task_id} updated")
            return
    print("Task not found")

def delete_task(task_id):
    data = load_data()
    new_tasks = [t for t in data["tasks"] if t["id"] != task_id]
    if len(new_tasks) == len(data["tasks"]):
        print("Task not found")
    else:
        data["tasks"] = new_tasks
        save_data(data)
        print(f"Task {task_id} deleted")

def change_status(task_id, status):
    data = load_data()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = now()
            save_data(data)
            print(f"Task {task_id} marked as {status}")
            return
    print("Task not found")

def list_tasks(filter_status=None):
    data = load_data()
    tasks = data["tasks"]

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"{task['id']}. {task['description']} "
              f"[{task['status']}] "
              f"(created: {task['createdAt']}, updated: {task['updatedAt']})")

def main():
    init_file()

    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        description = " ".join(sys.argv[2:])
        add_task(description)

    elif command == "update":
        task_id = int(sys.argv[2])
        new_description = " ".join(sys.argv[3:])
        update_task(task_id, new_description)

    elif command == "delete":
        task_id = int(sys.argv[2])
        delete_task(task_id)

    elif command == "mark-in-progress":
        task_id = int(sys.argv[2])
        change_status(task_id, "in-progress")

    elif command == "mark-done":
        task_id = int(sys.argv[2])
        change_status(task_id, "done")

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        else:
            status = sys.argv[2]
            if status in ["done", "todo", "in-progress"]:
                list_tasks(status)
            else:
                print("Invalid filter. Use: done, todo, in-progress")

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
