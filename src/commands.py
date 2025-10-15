from datetime import datetime
from rich.console import Console
from rich.table import Table

from .storage import create_task, get_tasks, save_database

console = Console()


def add_task():
    name = input("Task nomi: ").strip().capitalize()
    description = input("Tavsif: ").strip().capitalize()
    category = input("Kategoriya: ").strip().title()
    due_date = input("Tugash sanasi (yyyy-mm-dd): ")

    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    if due_date < datetime.now():
        print("Xato: Sana hozirgi kundan kichik bo‘lmasligi kerak.")
        return

    create_task(name, description, category, due_date)
    print("Task muvaffaqiyatli qo‘shildi.")


def show_tasks():
    tasks = get_tasks()

    if not tasks:
        print("Hozircha tasklar mavjud emas.")
        return

    table = Table(title="Barcha tasklar")
    table.add_column("ID", justify="center")
    table.add_column("Nomi")
    table.add_column("Kategoriya")
    table.add_column("Tugash sanasi")

    for task in tasks:
        due_date = task["due_date"].strftime("%d/%m/%Y")
        table.add_row(str(task["id"]), task["name"], task["category"], due_date)
    
    console.print(table)

    num = int(input("Batafsil ko‘rish uchun ID kiriting: "))
    task = next((t for t in tasks if t["id"] == num), None)

    if not task:
        print("Bunday ID topilmadi.")
        return

    status = "Bajarilgan" if task["status"] else "Bajarilmagan"
    due_date = task["due_date"].strftime("%d/%m/%Y")
    created_date = task["created_date"].strftime("%d/%m/%Y, %H:%M:%S")

    print(f"\nTask nomi: {task['name']}")
    print(f"Tavsif: {task['description']}")
    print(f"Kategoriya: {task['category']}")
    print(f"Holati: {status}")
    print(f"Tugash sanasi: {due_date}")
    print(f"Yaratilgan sana: {created_date}\n")


def update_task():
    tasks = get_tasks()
    show_tasks()

    if not tasks:
        return

    task_id = int(input("Yangilash uchun ID kiriting: "))
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print("Bunday ID topilmadi.")
        return

    task["name"] = input(f"Yangi nomi ({task['name']}): ") or task["name"]
    task["description"] = input(f"Yangi tavsif ({task['description']}): ") or task["description"]
    task["category"] = input(f"Yangi kategoriya ({task['category']}): ") or task["category"]

    save_database(tasks)
    print("Task muvaffaqiyatli yangilandi.")


def delete_task():
    tasks = get_tasks()
    show_tasks()

    if not tasks:
        return

    task_id = int(input("O‘chirish uchun ID kiriting: "))
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        print("Bunday ID topilmadi.")
    else:
        save_database(new_tasks)
        print("Task muvaffaqiyatli o‘chirildi.")


def change_status():
    tasks = get_tasks()
    show_tasks()

    if not tasks:
        return

    task_id = int(input("Holatini o‘zgartirish uchun ID kiriting: "))
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        print("Bunday ID topilmadi.")
        return

    task["status"] = not task["status"]
    save_database(tasks)

    if task["status"]:
        print("Task bajarilgan holatga o‘tkazildi.")
    else:
        print("Task bajarilmagan holatga qaytarildi.")
