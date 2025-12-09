import pytest
from library import Book, Movie, User, Library
import random


@pytest.fixture
def library_instance():
    return Library()


def _item(item_type, title="Title"):
    imdb_id_randome = str(random.randint(1, 9999999999))
    isbn_random = str(random.randint(1, 9999999999))
    return (
        item_type(
            title=title, directors=["Director"], year=2008, imdb_id=imdb_id_randome
        )
        if item_type is Movie
        else item_type(title=title, authors=["Author"], year=2008, isbn=isbn_random)
    )


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_borrow_item(item_type):
    item = _item(item_type)
    item.borrow_item()
    assert item.due_date is not None


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_return_item(item_type):
    item = _item(item_type)
    item.borrow_item()
    item.return_item()
    assert item.due_date is None


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_is_borrowed(item_type):
    item = _item(item_type)
    item.borrow_item()
    assert item.is_borrowed()


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_is_not_borrowed(item_type):
    item = _item(item_type)
    assert not item.is_borrowed()


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_add_item(library_instance, item_type):
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(Movie, "Podado"))
    library_instance.add_item(_item(Book, "Folado"))
    assert len(library_instance.get_list_of_items()) == 4


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_get_available_items(library_instance, item_type):
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(Movie, "Podado"))
    library_instance.add_item(_item(Book, "Folado"))
    assert len(library_instance.get_available_items()) == 4


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_get_available_books(library_instance, item_type):
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(Movie, "Podado"))
    library_instance.add_item(_item(Book, "Folado"))
    assert len(library_instance.get_available_books()) == 3 if item_type == Book else 1


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_get_available_movies(library_instance, item_type):
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(Movie, "Podado"))
    library_instance.add_item(_item(Book, "Folado"))
    assert (
        len(library_instance.get_available_movies()) == 3 if item_type == Movie else 1
    )


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_list_of_items(library_instance, item_type):
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(Movie, "Podado"))
    library_instance.add_item(_item(Book, "Folado"))
    assert len(library_instance.get_list_of_items()) == 4


def test_add_user(library_instance):
    library_instance.add_user("1337@solo.com", "John Doe")
    assert len(library_instance.get_users()) == 1


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_borrow_user(library_instance, item_type):
    library_instance.add_user("1337@solo.com", "John Doe")
    library_instance.add_item(_item(item_type, "Folado"))
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(item_type, "Podado"))
    user = library_instance.get_users()[0]
    items = library_instance.get_available_items()
    for item in items:
        id_item = library_instance._id_items(item)
        library_instance.user_borrow(user.id, id_item)
    assert len(library_instance.get_available_books()) == 0


@pytest.mark.parametrize("item_type", [Book, Movie])
def test_return_user(library_instance, item_type):
    library_instance.add_user("1337@solo.com", "John Doe")
    library_instance.add_item(_item(item_type, "Folado"))
    library_instance.add_item(_item(item_type, "Solado"))
    library_instance.add_item(_item(item_type, "Bonado"))
    library_instance.add_item(_item(item_type, "Podado"))
    user = library_instance.get_users()[0]
    items = library_instance.get_available_items()
    for item in items:
        id_item = library_instance._id_items(item)
        library_instance.user_borrow(user.id, id_item)
    assert len(library_instance.get_available_items()) == 0
    for item in items:
        id_item = library_instance._id_items(item)
        library_instance.user_return(user.id, id_item)
    assert len(library_instance.get_available_items()) == 4
