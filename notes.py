import json
from datetime import datetime

class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NoteMenu:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(**note_data) for note_data in notes_data]
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        notes_data = [{'note_id': note.note_id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp}
                      for note in self.notes]
        with open(self.filename, 'w') as file:
            json.dump(notes_data, file, indent=2)

    def display_notes(self):
        if not self.notes:
            print("Список заметок пуст")
        else:
            for note in self.notes:
                print(f"{note.note_id}. {note.title} - {note.timestamp}")

    def add_note(self):
        note_id = len(self.notes) + 1
        title = input("Введите название заметки: ")
        body = input("Введите содержимое заметки: ")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_note = Note(note_id, title, body, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка добавлена успешно!")

    def edit_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = input("Введите новое название заметки: ")
                note.body = input("Введите новое содержимое заметки: ")
                note.timestamp = datetime.now().strftime("%Y-%m-%d")
                self.save_notes()
                print("Заметка отредактирована успешно!")
                return
        print("Заметка с указанным идентификатором не найдена")

    def delete_note(self, note_id):
        existing_notes = [note for note in self.notes if note.note_id == note_id]
        if not existing_notes:
            print("Заметка с указанным идентификатором не найдена")
            return
        self.notes = [note for note in self.notes if note.note_id != note_id]
        for index, note in enumerate(self.notes, start=1):
            note.note_id = index
        self.save_notes()
        print("Заметка удалена успешно!")

    def view_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                print(f"\nЗаметка #{note.note_id} - {note.title} ({note.timestamp})\n")
                print(note.body)
                return
        print("Заметка с указанным идентификатором не найдена")

    def filter_notes_by_date(self, date):
        filtered_notes = [note for note in self.notes if date == note.timestamp]
        if not filtered_notes:
            print(f"За выбранную дату ({date}) заметок нет")
        else:
            for note in filtered_notes:
                print(f"{note.note_id}. {note.title} - {note.timestamp}")


def main():
    note_menu = NoteMenu()

    while True:
        print("\nМеню:")
        print("1. Показать все заметки")
        print("2. Показать содержимое заметки")
        print("3. Добавить новую заметку")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Фильтр по дате")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            note_menu.display_notes()
        elif choice == "2":
            note_id = int(input("Введите идентификатор заметки для просмотра: "))
            note_menu.view_note(note_id)
        elif choice == "3":
            note_menu.add_note()
        elif choice == "4":
            note_id = int(input("Введите идентификатор заметки для редактирования: "))
            note_menu.edit_note(note_id)
        elif choice == "5":
            note_id = int(input("Введите идентификатор заметки для удаления: "))
            note_menu.delete_note(note_id)
        elif choice == "6":
            date = input("Введите дату для фильтрации (формат: YYYY-MM-DD): ")
            note_menu.filter_notes_by_date(date)
        elif choice == "0":
            break
        else:
            print("Некорректный ввод, выберите действие из меню")


if __name__ == "__main__":
    main()
