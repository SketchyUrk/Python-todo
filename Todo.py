from sys import argv
from json import dump, load, JSONDecodeError
from os import path

TASKS_FILE = "tasks.json"


def load_tasks():
    if not path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r") as file:
            return load(file)
    except (JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        dump(tasks, file, indent=4)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title):
    tasks = load_tasks()

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added: {title}")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Complete" if task["completed"] else "Incomplete"
        print(f"[{task['id']}] {status} {task['title']}")


def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed.")
            return

    print(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted.")
            return None

    print(f"Task with ID {task_id} not found.")


def print_help():
    print("""
Todo App Commands:

python todo.py add "Task title"
python todo.py list
python todo.py done <id>
python todo.py delete <id>
""")


def main():
    if len(argv) < 2:
        print_help()
        return

    command = argv[1]

    if command == "add":
        if len(argv) < 3:
            print("Error: Missing task title.")
            return

        title = " ".join(argv[2:])
        add_task(title)

    elif command == "list":
        list_tasks()

    elif command == "done":
        if len(argv) < 3:
            print("Error: Missing task ID.")
            return

        try:
            task_id = int(argv[2])
            complete_task(task_id)
        except ValueError:
            print("Task ID must be a number.")

    elif command == "delete":
        if len(argv) < 3:
            print("Error: Missing task ID.")
            return

        try:
            task_id = int(argv[2])
            delete_task(task_id)
        except ValueError:
            print("Task ID must be a number.")

    else:
        print("Unknown command.")
        print_help()


if __name__ == "__main__":
    main()