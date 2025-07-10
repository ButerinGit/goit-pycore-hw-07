from datetime import datetime

def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except IndexError:
            return "Missing arguments."
        except ValueError as e:
            return str(e)
        except AttributeError:
            return "Contact not found."
    return wrapper

@input_error
def add_birthday(args, book):
    name, birthday_str = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    # Перевірка формату дати
    try:
        datetime.strptime(birthday_str, "%d.%m.%Y")
    except ValueError:
        return "Invalid date format. Use DD.MM.YYYY"
    record.add_birthday(birthday_str)
    return f"Birthday for {name} added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        return "Birthday not set for this contact."
    return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    return "Upcoming birthdays:\n" + "\n".join(upcoming)

# === Симуляція адресної книги ===
class Record:
    def __init__(self, name):
        self.name = name
        self.birthday = None
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

class Birthday:
    def __init__(self, date_str):
        self.value = datetime.strptime(date_str, "%d.%m.%Y")

class AddressBook:
    def __init__(self):
        self.contacts = {"Alice": Record("Alice")}
    def find(self, name):
        return self.contacts.get(name)
    def get_upcoming_birthdays(self):
        return ["Alice - 10.07.1995"]

book = AddressBook()

# === Головний цикл ===
commands = {
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}

while True:
    user_input = input(">>> ").strip()
    if user_input in ["exit", "close"]:
        print("Good bye!")
        break
    parts = user_input.split()
    cmd, args = parts[0], parts[1:]
    if cmd in commands:
        result = commands[cmd](args, book)
        print(result)
    else:
        print("Unknown command.")
