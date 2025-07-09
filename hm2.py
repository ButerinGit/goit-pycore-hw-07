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
