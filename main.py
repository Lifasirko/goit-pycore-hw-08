import pickle
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("New phone number must be 10 digits")

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return True
        raise ValueError("Old phone number not found")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        # Переконайтеся, що record є екземпляром класу Record
        if isinstance(record, Record):
            self.data[record.name.value] = record
        else:
            raise TypeError("record має бути екземпляром класу Record")

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)
            days_until_birthday = (birthday_this_year - today).days
            if 0 <= days_until_birthday <= 7:
                # Adjust for weekends
                if birthday_this_year.weekday() >= 5:  # Saturday or Sunday
                    days_to_add = 7 - birthday_this_year.weekday()
                    birthday_this_year += timedelta(days=days_to_add)
                upcoming_birthdays.append(record)
        return upcoming_birthdays


def __str__(self):
    return "\n".join(str(record) for record in self.data.values())


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me the correct arguments please."
        except IndexError:
            return "Provide enough arguments."

    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        record.add_phone(phone)
        return "Phone number added to the existing contact."


@input_error
def change_contact(args, book):
    name, phone = args
    if name not in book:
        raise KeyError
    record = Record(name)

    book[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]
    return book[name]


@input_error
def show_all(book, *args):
    return "\n".join([f"{name}: {number}" for name, number in book.items()])


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    else:
        return "Birthday not found."


@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(
            [f"{record.name.value}'s birthday is coming up on {record.birthday.value.strftime('%d.%m.%Y')}" for record
             in upcoming_birthdays])
    else:
        return "No upcoming birthdays."


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("FileNotFoundError")
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def main():
    book = load_data()
    print("Welcome to the assistant bot! Type 'exit' or 'close' to quit.")

    while True:

        # try:
        user_input = input("Enter a command: ")
        try:
            command, *args = user_input.split()
        except ValueError:
            print("Give me the correct command please.")
            command = None
            pass

        if command is None:
            pass
        elif command.lower() in ["exit", "close"]:
            save_data(book)
            print("Good bye!")
            break
        elif command.lower() == "hello":
            print("How can I help you?")
        elif command.lower() == "add":
            print(add_contact(args, book))
        elif command.lower() == "change":
            print(change_contact(args, book))
        elif command.lower() == "phone":
            print(show_phone(args, book))
        elif command.lower() == "all":
            print(show_all(book, *args))
        elif command.lower() == "add-birthday":
            print(add_birthday(args, book))  # Передайте book як аргумент
        elif command.lower() == "show-birthday":
            print(show_birthday(args, book))
        elif command.lower() == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()

# add mike 0502222222
# add-birthday mike 21.05.1995
# add alex 0503333333
# add-birthday alex 03.03.2020
# birthdays
