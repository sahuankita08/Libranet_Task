import json, os
from abc import ABC, abstractmethod
from datetime import datetime

class LibraryItem(ABC):
    def __init__(self, item_id: int, title: str, author: str):
        self.item_id = item_id
        self.title = title
        self.author = author
        self.is_available = True
        self.borrow_date = None
        self.due_date = None
        self.fine_rate = 10 

    def borrow(self, duration_str: str):
        if not self.is_available:
            print(f"{self.title} is currently not available.")
            return
        try:
            days = int(duration_str.replace("days", "").strip())
            self.borrow_date = datetime.now()
            self.due_date = self.borrow_date.replace(day=self.borrow_date.day + days)
            self.is_available = False
            print(f"{self.title} borrowed for {days} days.")
        except Exception as e:
            print(f"Error parsing duration: {e}")

    def return_item(self):
        if self.is_available:
            print(f"{self.title} was not borrowed.")
            return
        self.is_available = True
        today = datetime.now()
        overdue_days = (today - self.due_date).days if self.due_date else 0
        fine = self.fine_rate * overdue_days if overdue_days > 0 else 0
        print(
            f"{self.title} returned. Fine: Rs {fine}"
            if fine > 0
            else f"{self.title} returned on time."
        )

    def check_availability(self):
        return self.is_available

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

class Book(LibraryItem):
    def __init__(self, item_id, title, author, page_count):
        super().__init__(item_id, title, author)
        self.page_count = page_count

    def get_page_count(self):
        return self.page_count

    def display_info(self):
        print(
            f"Book[{self.item_id}]: {self.title} by {self.author}, Pages: {self.page_count}, Available: {self.is_available}"
        )

    def to_dict(self):
        return {
            "type": "Book",
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "page_count": self.page_count,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["item_id"], data["title"], data["author"], data["page_count"])
        book.is_available = data["is_available"]
        return book


class Playable(ABC):
    @abstractmethod
    def play(self):
        pass

class Audiobook(LibraryItem, Playable):
    def __init__(self, item_id, title, author, duration):
        super().__init__(item_id, title, author)
        self.duration = duration  

    def play(self):
        print(f"Playing audiobook: {self.title} ({self.duration} hrs)")

    def display_info(self):
        print(
            f"Audiobook[{self.item_id}]: {self.title} by {self.author}, Duration: {self.duration} hours, Available: {self.is_available}"
        )

    def to_dict(self):
        return {
            "type": "Audiobook",
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "duration": self.duration,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data):
        audio = cls(data["item_id"], data["title"], data["author"], data["duration"])
        audio.is_available = data["is_available"]
        return audio


class EMagazine(LibraryItem):
    def __init__(self, item_id, title, author, issue_number):
        super().__init__(item_id, title, author)
        self.issue_number = issue_number

    def archive_issue(self):
        print(f"Archiving issue #{self.issue_number} of {self.title}")

    def display_info(self):
        print(
            f"EMagazine[{self.item_id}]: {self.title} by {self.author}, Issue: {self.issue_number}, Available: {self.is_available}"
        )

    def to_dict(self):
        return {
            "type": "EMagazine",
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "issue_number": self.issue_number,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data):
        mag = cls(data["item_id"], data["title"], data["author"], data["issue_number"])
        mag.is_available = data["is_available"]
        return mag

class LibrarySearch:
    @staticmethod
    def search_by_title(items, keyword: str):
        return [item for item in items if keyword.lower() in item.title.lower()]

    @staticmethod
    def search_by_type(items, item_type):
        return [item for item in items if isinstance(item, item_type)]

    @staticmethod
    def search_by_title_and_type(items, keyword: str, item_type):
        return [
            item
            for item in items
            if isinstance(item, item_type) and keyword.lower() in item.title.lower()
        ]

def save_library(items, filename="library.json"):
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=4)


def load_library(filename="library.json"):
    if not os.path.exists(filename):
        return [
            Book(1, "Clean Code", "Robert C. Martin", 450),
            Book(2, "The Pragmatic Programmer", "Andy Hunt", 320),
            EMagazine(3, "Tech Monthly", "Editorial Team", 42),
            Audiobook(4, "Atomic Habits", "James Clear", 6.5),
            Audiobook(5, "The Power of Habit", "Charles Duhigg", 10),
        ]

    with open(filename, "r") as f:
        data = json.load(f)

    items = []
    for entry in data:
        if entry["type"] == "Book":
            items.append(Book.from_dict(entry))
        elif entry["type"] == "Audiobook":
            items.append(Audiobook.from_dict(entry))
        elif entry["type"] == "EMagazine":
            items.append(EMagazine.from_dict(entry))
    return items

def run_app():
    library_items = load_library()

    while True:
        print("\n--- LibraNet Menu ---")
        print("1. List all items")
        print("2. Borrow item")
        print("3. Return item")
        print("4. Play audiobook")
        print("5. Search by title")
        print("6. Search by type (Book/Audiobook/EMagazine)")
        print("7. Search by title + type")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            for item in library_items:
                item.display_info()

        elif choice == "2":
            item_id = int(input("Enter item ID to borrow: "))
            duration = input("Enter duration (e.g., '7 days'): ")
            for item in library_items:
                if item.item_id == item_id:
                    item.borrow(duration)

        elif choice == "3":
            item_id = int(input("Enter item ID to return: "))
            for item in library_items:
                if item.item_id == item_id:
                    item.return_item()

        elif choice == "4":
            item_id = int(input("Enter audiobook ID to play: "))
            for item in library_items:
                if item.item_id == item_id and isinstance(item, Audiobook):
                    item.play()

        elif choice == "5":
            keyword = input("Enter keyword to search by title: ")
            results = LibrarySearch.search_by_title(library_items, keyword)
            for item in results:
                item.display_info()

        elif choice == "6":
            type_input = input("Enter type (Book/Audiobook/EMagazine): ").lower()
            type_map = {"book": Book, "audiobook": Audiobook, "emagazine": EMagazine}
            if type_input in type_map:
                results = LibrarySearch.search_by_type(
                    library_items, type_map[type_input]
                )
                for item in results:
                    item.display_info()
            else:
                print("Invalid type entered.")

        elif choice == "7":
            keyword = input("Enter keyword: ")
            type_input = input("Enter type (Book/Audiobook/EMagazine): ").lower()
            type_map = {"book": Book, "audiobook": Audiobook, "emagazine": EMagazine}
            if type_input in type_map:
                results = LibrarySearch.search_by_title_and_type(
                    library_items, keyword, type_map[type_input]
                )
                if results:
                    print(
                        f"\nFound {len(results)} {type_input}(s) with keyword '{keyword}':"
                    )
                    for item in results:
                        item.display_info()
                else:
                    print(f"No {type_input}s found with keyword '{keyword}'.")
            else:
                print("Invalid type entered.")

        elif choice == "0":
            save_library(library_items)
            print("Library saved. Exiting LibraNet. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    run_app()
