import os
import json
from datetime import datetime, date

DATABASE_URL = "database.json"

if not os.path.exists(DATABASE_URL):
    with open(DATABASE_URL, "w") as f:
        json.dump([], f, indent=4)


def read_database() -> list[dict]:
    """Barcha tasklarni fayldan o‘qish"""
    with open(DATABASE_URL, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_database(tasks: list[dict]):
    """Tasklarni faylga saqlash (datetime obyektlarini stringga aylantiradi)"""
    serializable_tasks = []
    for task in tasks:
        new_task = task.copy()

        if isinstance(new_task.get("due_date"), datetime):
            new_task["due_date"] = new_task["due_date"].strftime("%d/%m/%Y")

        if isinstance(new_task.get("created_date"), datetime):
            new_task["created_date"] = new_task["created_date"].strftime("%d/%m/%Y, %H:%M:%S")

        serializable_tasks.append(new_task)

    with open(DATABASE_URL, "w") as f:
        json.dump(serializable_tasks, f, indent=4)


def create_task(name: str, description: str, category: str, due_date: date) -> bool:
    """Yangi task yaratish"""
    tasks = read_database()
    last_id = max((task["id"] for task in tasks), default=0)

    new_task = {
        "id": last_id + 1,
        "name": name,
        "description": description,
        "category": category,
        "due_date": due_date.strftime("%d/%m/%Y"),
        "created_date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "status": False,
    }

    tasks.append(new_task)
    save_database(tasks)
    return True


def get_tasks() -> list[dict]:
    """Tasklarni datetime obyektlari bilan olish"""
    tasks = []
    for task in read_database():
        try:
            task["due_date"] = datetime.strptime(task["due_date"], "%d/%m/%Y")
            task["created_date"] = datetime.strptime(task["created_date"], "%d/%m/%Y, %H:%M:%S")
        except Exception:
            continue
        tasks.append(task)
    return tasks
