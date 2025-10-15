from rich.console import Console
from .commands import add_task, show_tasks, update_task, delete_task, change_status

console = Console()

def main():
    while True:
        print("\n--- TODO APP ---")
        print("1. Vazifa qo‘shish")
        print("2. Vazifalarni ko‘rish")
        print("3. Vazifani yangilash")
        print("4. Vazifani o‘chirish")
        print("5. Holatini o‘zgartirish")
        print("0. Chiqish")

        choice = input("\nTanlovni kiriting: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            change_status()
        elif choice == "0":
            print("Dastur tugatildi.")
            break
        else:
            print("Noto‘g‘ri tanlov! Qayta urinib ko‘ring.")
