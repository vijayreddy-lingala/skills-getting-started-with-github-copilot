import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")
VALID_PRIORITIES = ["Low", "Medium", "High"]
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

class Todo:
    def __init__(self, title, description, due_date, priority, status="Not Started"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_completed(self):
        self.status = "Completed"

    def mark_as_in_progress(self):
        self.status = "In Progress"

    def mark_as_not_started(self):
        self.status = "Not Started"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            priority=data.get("priority", "Low"),
            status=data.get("status", "Not Started"),
        )

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Due Date: {self.due_date}\n"
            f"Priority: {self.priority}\n"
            f"Status: {self.status}"
        )


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Todo.from_dict(item) for item in data]
    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading saved tasks: {error}")
        return []


def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2)
    except OSError as error:
        print(f"Error saving tasks: {error}")


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def choose_task(tasks, prompt_text="Select a task by number: "):
    if not tasks:
        print("No tasks available.")
        return None

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task.title} (Due: {task.due_date}, Priority: {task.priority}, Status: {task.status})")

    choice = input(prompt_text).strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(tasks)):
        print("Invalid selection. Please enter a valid task number.")
        return None
    return tasks[int(choice) - 1]


def list_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
        return

    print("\nTask list:\n")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Due Date: {task.due_date}")
        print(f"   Priority: {task.priority}")
        print(f"   Status: {task.status}\n")


def add_task(tasks):
    print("\nAdd a new task")
    title = input("Title: ").strip()
    if not title:
        print("Title is required.")
        return

    description = input("Description: ").strip()
    due_date = input("Due date (YYYY-MM-DD): ").strip()
    if not validate_date(due_date):
        print("Please enter a valid due date in YYYY-MM-DD format.")
        return

    print("Priority options: Low, Medium, High")
    priority = input("Priority: ").strip().title()
    if priority not in VALID_PRIORITIES:
        print("Priority must be Low, Medium, or High.")
        return

    tasks.append(Todo(title, description, due_date, priority))
    print("Task added successfully.")


def modify_task(tasks):
    print("\nModify an existing task")
    task = choose_task(tasks)
    if not task:
        return

    new_title = input(f"Title [{task.title}]: ").strip() or task.title
    new_description = input(f"Description [{task.description}]: ").strip() or task.description
    new_due_date = input(f"Due date [{task.due_date}] (YYYY-MM-DD): ").strip() or task.due_date
    if not validate_date(new_due_date):
        print("Please enter a valid due date in YYYY-MM-DD format.")
        return

    print("Priority options: Low, Medium, High")
    new_priority = input(f"Priority [{task.priority}]: ").strip().title() or task.priority
    if new_priority not in VALID_PRIORITIES:
        print("Priority must be Low, Medium, or High.")
        return

    task.title = new_title
    task.description = new_description
    task.due_date = new_due_date
    task.priority = new_priority
    print("Task updated successfully.")


def update_status(tasks):
    print("\nChange task status")
    task = choose_task(tasks)
    if not task:
        return

    print("Status options:")
    for index, status in enumerate(VALID_STATUSES, start=1):
        print(f"{index}. {status}")

    choice = input("Choose a status number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(VALID_STATUSES)):
        print("Invalid status selection.")
        return

    task.status = VALID_STATUSES[int(choice) - 1]
    print(f"Task status updated to {task.status}.")


def remove_task(tasks):
    print("\nRemove a task")
    task = choose_task(tasks)
    if not task:
        return

    confirm = input(f"Are you sure you want to delete '{task.title}'? (y/n): ").strip().lower()
    if confirm == "y":
        tasks.remove(task)
        print("Task removed successfully.")
    else:
        print("Deletion canceled.")


def remove_tasks_bulk(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    print("\nBulk remove tasks")
    list_tasks(tasks)
    start = input("Enter the first task number to delete: ").strip()
    end = input("Enter the last task number to delete: ").strip()
    if not (start.isdigit() and end.isdigit()):
        print("Please enter valid numeric task positions.")
        return

    start_index = int(start) - 1
    end_index = int(end) - 1
    if start_index < 0 or end_index >= len(tasks) or start_index > end_index:
        print("Invalid range specified.")
        return

    confirm = input(f"Are you sure you want to remove tasks {start} through {end}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Bulk deletion canceled.")
        return

    del tasks[start_index:end_index + 1]
    print("Selected tasks deleted.")


def sort_tasks(tasks):
    if not tasks:
        print("No tasks to sort.")
        return

    print("\nSort tasks by:")
    print("1. Status")
    print("2. Priority")
    print("3. Due date")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        tasks.sort(key=lambda item: VALID_STATUSES.index(item.status) if item.status in VALID_STATUSES else len(VALID_STATUSES))
        print("Tasks sorted by status.")
    elif choice == "2":
        tasks.sort(key=lambda item: VALID_PRIORITIES.index(item.priority) if item.priority in VALID_PRIORITIES else len(VALID_PRIORITIES))
        print("Tasks sorted by priority.")
    elif choice == "3":
        tasks.sort(key=lambda item: item.due_date)
        print("Tasks sorted by due date.")
    else:
        print("Invalid sort option.")


def print_menu():
    print("\nTodo App Menu")
    print("1. View tasks")
    print("2. Add task")
    print("3. Modify task")
    print("4. Change task status")
    print("5. Remove task")
    print("6. Bulk remove tasks")
    print("7. Sort tasks")
    print("8. Save tasks")
    print("9. Exit")


def startup():
    tasks = load_tasks()
    print("Welcome to the Todo App.")
    print("Loaded {} saved task(s).".format(len(tasks)))

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            modify_task(tasks)
        elif choice == "4":
            update_status(tasks)
        elif choice == "5":
            remove_task(tasks)
        elif choice == "6":
            remove_tasks_bulk(tasks)
        elif choice == "7":
            sort_tasks(tasks)
        elif choice == "8":
            save_tasks(tasks)
            print("Tasks saved.")
        elif choice == "9":
            save_tasks(tasks)
            print("Saved tasks before exit. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid menu item.")


if __name__ == "__main__":
    startup() 
           