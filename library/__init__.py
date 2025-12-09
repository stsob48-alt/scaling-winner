import hashlib
from datetime import datetime, timedelta


class LibraryItem:
    def __init__(self, title: str, type_id: str):
        self.type_id = type_id
        self.title = title
        self._due = timedelta(days=30)
        self.due_date = None

    def is_borrowed(self) -> bool:
        return True if self.due_date else False

    def borrow_item(self) -> datetime | None:
        self.due_date = datetime.now() + self._due

    def return_item(self) -> None | str:
        if self.due_date is None:
            return "Item is not borrowed"
        late = None
        if datetime.now() > self.due_date:
            late = "Item is late"
        self.due_date = None
        return late


class Book(LibraryItem):
    def __init__(
        self,
        title: str,
        authors: list[str],
        isbn: str,
        year: int,
        lang: str = "EN",
        publisher: str | None = None,
    ):
        super().__init__(title, isbn)
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.lang = lang
        self.isbn = isbn


class Movie(LibraryItem):
    def __init__(self, title: str, directors: list[str], year: int, imdb_id: str):
        super().__init__(title, imdb_id)
        self.directors = directors
        self.year = year
        self.imdb_id = imdb_id


class User:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.borrowed_items: list[LibraryItem] = []


class Library:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.items: dict[str, LibraryItem] = {}
        self.inventory: dict[str, int] = {}

    def _id_user(self, email, name) -> str:
        return hashlib.sha256((name + email).encode()).hexdigest()

    def _id_items(self, item: LibraryItem) -> str:
        return hashlib.sha256((str(item.title) + item.type_id).encode()).hexdigest()

    def user_borrow(self, user_id: str, item_id: str) -> None:
        """Borrow an item from the library
        Args:
            user_id: str Unique id of the user
            item_id: str Unique id of the item
        """
        try:
            user = self.users[user_id]
            item = self.items[item_id]
            if item in user.borrowed_items:
                raise ValueError(f"User {user_id} already has item {item_id}")
            item.borrow_item()
            user.borrowed_items.append(item)
            self.remove_inventory(item_id)
        except KeyError as _:
            raise ValueError("User or item not found")

    def user_return(self, user_id: str, item_id: str) -> None:
        """Return an item to the library
        Args:
            user_id: str Unique id of the user
            item_id: str Unique id of the item
        """
        try:
            user = self.users[user_id]
            item = self.items[item_id]
            if item not in user.borrowed_items:
                raise ValueError(f"User {user_id} does not have item {item_id}")
            item.return_item()
            user.borrowed_items.remove(item)
            self.add_inventory(item_id)
        except KeyError as _:
            raise ValueError("User or item not found")

    def add_user(self, email, name):
        """Add a user
        Args:
            email: str Email of the user
            name: str Name of the user
        """
        unique_id = self._id_user(email, name)
        user = User(unique_id, email, name)
        self._add_user(user)

    def _add_user(self, user: User) -> None:
        try:
            self.users[user.id]
            raise ValueError(f"User with ID {user.id} already exists")
        except KeyError as _:
            self.users[user.id] = user

    def add_inventory(self, item_id: str):
        try:
            if self.inventory[item_id] > 0:
                self.inventory[item_id] += 1
            else:
                raise ValueError(
                    "Somthing went wrong when item was added, please redo, remove_item and then add_item"
                )
        except KeyError as _:
            raise ValueError(f"Item with ID {item_id} does not exist")

    def add_item(self, item: LibraryItem) -> None:
        """Add an item to the library
        Args:
            item: LibraryItem Item to add
        """
        if item.type_id in [
            movie.imdb_id for movie in self.items.values() if isinstance(movie, Movie)
        ]:
            raise ValueError(f"Movie with IMDB ID {item.type_id} already exists")
        unique_id = self._id_items(item)
        try:
            _item = self.items[unique_id]
            if _item != item:
                raise ValueError(f"Item with ID {unique_id} already exists")
        except KeyError as _:
            self.items[unique_id] = item
            self.inventory[unique_id] = 1

    def remove_item(self, item: Movie | Book):
        """Remove an item from the library
        Args:
            item: Movie | Book Item to remove
        """
        self.inventory.pop(self._id_items(item))
        return self.items.pop(self._id_items(item))

    def remove_inventory(self, item_id):
        """Remove an item from the library
        Args:
            item: Movie | Book Item to remove
        """
        try:
            if self.inventory[item_id] > 0:
                self.inventory[item_id] -= 1
            elif self.inventory[item_id] == 1:
                self.remove_item(item_id)
            else:
                raise ValueError("Inventory is empty")
        except KeyError as _:
            raise ValueError(f"Item with ID {item_id} does not exist")

    def search_items(
        self, query: str
    ) -> list[LibraryItem]:  # Todo implement a broader search
        """Search for items in the library
        Args:
            query: String to search for
        """
        return [
            item for item in self.items.values() if query.lower() in item.title.lower()
        ]

    def search_users(self, query: str) -> list[User]:  # Todo implement a broader search
        """Search for users in the library
        Args:
            query: String to search for
        """
        return [
            user for user in self.users.values() if query.lower() in user.name.lower()
        ]

    def get_users(self) -> list[User]:
        """Get a list of all users in the library"""
        return list(self.users.values())

    def get_list_of_items(self) -> list[LibraryItem]:
        """Get a list of all items in the library"""
        return list(self.items.values())

    def get_available_items(self) -> list[LibraryItem]:
        """Get a list of all available items in the library"""
        return [item for item in self.items.values() if not item.is_borrowed()]

    def get_available_books(self) -> list[Book]:
        """Get a list of all available books in the library"""
        return self._get_available_items_by_type(Book)

    def get_available_movies(self) -> list[Movie]:
        """Get a list of all available movies in the library"""
        return self._get_available_items_by_type(Movie)

    def _get_available_items_by_type(self, item_type: type):
        """Get a list of all available items of a specific type in the library"""
        return [
            item
            for item in self.items.values()
            if isinstance(item, item_type) and not item.is_borrowed()
        ]
