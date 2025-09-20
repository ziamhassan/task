import json
import os

FILE_NAME = "tasks.json"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump([], f)  # just an empty list of tasks

def load_tasks():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "description": description, "status": "todo"}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    for task in tasks:
        print(f"{task['id']}. {task['description']} [{task['status']}]")

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            print(f"Task {task_id} marked as done")
            return
    print("Task not found.")

def main():
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Done")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            add_task(description)

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            mark_done(task_id)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
