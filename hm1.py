from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digits")
        self.value = value

class Name(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already set")

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def get_upcoming_birthdays(self, days=7):
        upcoming = []
        for record in self.records.values():
            days_left = record.days_to_birthday()
            if days_left is not None and 0 <= days_left <= days:
                upcoming.append(record.name.value)
        return upcoming
