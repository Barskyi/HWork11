from collections import UserDict
from datetime import datetime

# Клас Field, який є базовим для Name, Phone та Birthday
class Field:
    def __init__(self, value):
        """
        Конструктор класу Field.

        :param value: Значення поля
        """
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас Name, успадкований від Field, для представлення імені контакту
class Name(Field):
    def __init__(self, value):
        """
        Конструктор класу Name.

        :param value: Значення імені контакту
        :raises ValueError: Якщо значення імені порожнє, видається виняток
        """
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


# Клас Phone, успадкований від Field, для представлення номера телефону
class Phone(Field):
    def __init__(self, value):
        """
        Конструктор класу Phone.

        :param value: Значення номера телефону
        :raises ValueError: Якщо значення не є 10-значним числом, видається виняток
        """
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)


# Клас Birthday для представлення дня народження
class Birthday(Field):
    def __init__(self, value):
        """
        Конструктор класу Birthday.

        :param value: Значення дня народження у форматі '%Y-%m-%d'
        :raises ValueError: Якщо значення не відповідає формату
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format for Birthday")
        super().__init__(value)


# Клас Record для зберігання інформації про контакт
class Record:
    def __init__(self, name, birthday=None):
        """
        Конструктор класу Record.

        :param name: Значення імені контакту
        :param birthday: Значення дня народження (опціонально)
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        """
        Додає номер телефону до запису.

        :param phone: Значення номера телефону
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Видаляє номер телефону з запису.

        :param phone: Значення номера телефону
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """
        Редагує номер телефону в записі.

        :param old_phone: Попереднє значення номера телефону
        :param new_phone: Нове значення номера телефону
        :raises ValueError: Якщо попередній номер телефону не знайдено
        """
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number '{old_phone}' not found")

    def find_phone(self, phone):
        """
        Пошук номера телефону в записі.

        :param phone: Значення номера телефону
        :return: Знайдені номери телефону або None, якщо не знайдено
        """
        phones_found = [p for p in self.phones if p.value == phone]
        return phones_found[0] if phones_found else None

    def days_to_birthday(self):
        """
        Кількість днів до наступного дня народження.

        :return: Кількість днів до наступного дня народження або -1, якщо день народження не задано
        """
        if not self.birthday:
            return -1

        today = datetime.now().date()
        next_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)

        days_until_birthday = (next_birthday - today).days
        return days_until_birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


# Клас AddressBook для зберігання контактів
class AddressBook(UserDict):
    def add_record(self, record):
        """
        Додає запис до адресної книги.

        :param record: Запис для додавання
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Пошук запису за ім'ям в адресній книзі.

        :param name: Ім'я для пошуку
        :return: Знайдений запис або None, якщо не знайдено
        """
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        """
        Видаляє запис за ім'ям з адресної книги.

        :param name: Ім'я для видалення
        """
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        self.current_record = 0
        self.records = list(self.data.values())
        return self

    def __next__(self):
        if self.current_record < len(self.records):
            record = self.records[self.current_record]
            self.current_record += 1
            return record
        else:
            raise StopIteration


if __name__ == "__main__":
    address_book = AddressBook()

