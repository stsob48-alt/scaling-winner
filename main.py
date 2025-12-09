from isbnlib import meta
from imdbinfo import get_movie
from library import Library, Movie, Book


def split_list(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def add_book(library):
    """
    Legger til book
    """
    while True:
        print("Legg til bok")
        print("1. By ISBN")
        print("2. Manual")
        print("#. Back")
        print("0. Avslutt")
        choice = input("Velg en valgmulighet: ")

        def get_book_from_isbn(isbn: str) -> dict:
            return meta(isbn)

        if choice == "1":
            isbn = input("ISBN: ").strip()
            try:
                (isbn, title, authors, publisher, year, lang) = get_book_from_isbn(
                    isbn
                ).values()
            except ():
                print("Online søk feilet, prøv manuelt")
                continue
            book = Book(title, authors, isbn, int(year), lang, publisher)
            library.add_item(book)
            print("Bok lagt til")
            print("Legg til ny bok (y/n)")
            choice = input("Valg: ")
            if choice.lower() == "n":
                break
            elif not choice.lower() == "y" or not choice.lower() == "n":
                print("Ugyldig valg")

        elif choice == "2":
            title = input("Bok tittel: ").strip()
            isbn = input("ISBN: ").strip()
            authors = input("Forfatter: ").strip().split(",")
            publisher = input("Forlag: ").strip()
            year = input("Utgivelsesår: ").strip()
            lang = input("Språk: ").strip()
            book = Book(title, authors, isbn, int(year), lang, publisher)
            library.add_item(book)
            print("Bok lagt til")
            print("Legg til ny bok (y/n)")
            choice = input("Valg: ")
            if choice.lower() == "n":
                break
            elif not choice.lower() == "y" and not choice.lower() == "n":
                print("Ugyldig valg")
        elif choice == "#":
            return
        elif choice == "0":
            exit()
        else:
            print("Ugyldig valg")


def add_movie(library: Library):
    """
    Legger til film
    """
    while True:
        print("Legg til film")
        # sellection for tittle or imdb id
        print("1. By IMDB id ")
        print("2. Manual")
        choice = input("Velg en valgmulighet: ")
        if choice == "1":
            imdb_id = input("IMDB id: ").strip()
            try:
                movie = get_movie(imdb_id)
            except ():
                print("Online søk feilet, prøv manuelt")
                continue
            movie = Movie(movie.title, movie.directors, movie.year, imdb_id)
            library.add_item(movie)
            print("Film lagt til")
            print("Legg til ny film (y/n)")
            choice = input("Valg: ")
            if choice.lower() == "n":
                break
            elif not choice.lower() == "y" and not choice.lower() == "n":
                print("Ugyldig valg")
        elif choice == "2":
            imdb_id = input("IMDB id: ").strip()
            title = input("Film tittel: ").strip()
            year = input("Film år: ").strip()
            directors = input("Film regissør/er: ").strip().split(",")
            movie = Movie(title, directors, int(year), imdb_id)
            library.add_item(movie)
            print("Film lagt til")
            print("Legg til ny bok (y/n)")
            choice = input("Valg: ")
            if choice.lower() == "n":
                break
            elif not choice.lower() == "y" and not choice.lower() == "n":
                print("Ugyldig valg")
        elif choice == "#":
            return
        elif choice == "0":
            exit()
        else:
            print("Ugyldig valg")


def borrow_item(library):
    max_items = 5
    while True:
        print("1. Film")
        print("2. Bok")
        print("?. Søk")
        print("#. Tilbake")
        print("0. Avslutt")
        choice = input("Velg: ").strip()
        if choice == "1":
            movie_list = library.get_available_movies()
            page_content = split_list(movie_list, max_items)
            page = 1
            start_index = (page - 1) * max_items + 1
            print("Amount of movies:", len(movie_list))
            while True:
                print(f"Side {page}:")
                for i, item in enumerate(page_content[page - 1]):
                    print(f"{i + start_index}. {item}")
                print("?. Søk")
                if page > 1:
                    print("<. Forrige")
                if page < len(page_content):
                    print(">. Neste")
                print("#. Tilbake")
                print("0. Avslutt")
                choice = input("Velg: ").strip()
                if choice in range(len(movie_list)):
                    movie = movie_list[int(choice)]
                    library.borrow_item(movie)
                elif choice == "?":
                    while True:
                        search_term = input("Søk etter: ").strip()
                        results = library.search_items(search_term)
                        if results:
                            print("Søk: ", search_term)
                            print("Søk resultat:")
                            for i, result in enumerate(results):
                                print(f"{i}. {result.title}, {result.year}")
                            print("#. Tilbake")
                            print("0. Avslutt")
                            choice = input("Velg film: ").strip()
                            if choice == "#":
                                break
                            elif choice == "0":
                                exit()
                            elif choice in range(len(results)):
                                movie = results[int(choice)]
                                if movie.is_available():
                                    library.borrow_item(movie)
                                    print(f"{movie.title} er nå utlånt.")
                                else:
                                    print(f"{movie.title} er allerede utlånt.")
                            else:
                                print("Ugyldig valg")
                        else:
                            print("Ingen treff")
                        choice = input("Fortsett søk? (y/n): ").strip()
                        if choice == "n":
                            break
                    break
                elif choice == "#":
                    break
                elif choice == "0":
                    exit()
            break
        elif choice == "2":
            book_list = library.get_available_books()
            page_content = split_list(book_list, max_items)
            page = 1
            start_index = (page - 1) * max_items + 1
            while True:
                print(f"Side {page}:")
                for i, item in enumerate(page_content[page - 1]):
                    print(f"{i + start_index}. {item}")
                print("?. Søk")
                if page > 1:
                    print("<. Forrige")
                if page < len(page_content):
                    print(">. Neste")
                print("#. Tilbake")
                print("0. Avslutt")
                choice = input("Velg en handling: ").strip()
                if choice == "?":
                    while True:
                        print("Søk etter book")
                        search_term = input("Søk etter: ").strip()
                        results = library.search_items(search_term)
                        if results:
                            print("Søk: ", search_term)
                            print("Søk resultat:")
                            for result in results:
                                print(result)
                            print("#. Tilbake")
                            print("0. Avslutt")
                            choice = input("Velg bok: ").strip()
                            if choice in range(len(results)):
                                book = results[int(choice)]
                                if book.is_available():
                                    library.borrow_item(book)
                                    print(f"Boken '{book.title}' er lånt.")
                                else:
                                    print(f"Boken '{book.title}' er ikke tilgjengelig.")
                            if choice == "#":
                                break
                            elif choice == "0":
                                exit()
                        else:
                            print("Ingen treff")
                        choice = input("Fortsett søk? (y/n): ").strip()
                        if choice == "n":
                            break
                elif choice == "#":
                    break
                elif choice == "0":
                    exit()
            break
        elif choice == "?":
            print("Søk etter gjenstand")
            search_term = input("Søk etter: ").strip()
            results = library.search_items(search_term)
            if results:  # TODO: Søk etter gjenstand og velg en
                print("Søk resultat:")
                for item in results:
                    print(f"{item.title} ({item.type})")
            else:
                print("Ingen treff")
        elif choice == "#":
            return
        elif choice == "0":
            exit()
        else:
            print("Ugyldig valg")
    print("Gjenstand lånt")


def return_item(library: Library):
    # TODO: Gjør det mulig å gå tilbake til hovedmenyen, exit eller forsette å prøve finne LibraryItem ved id for returnere
    while True:
        item_id = input("Skriv inn ID på gjenstanden du vil returnere: ")
        try:
            library_item = library.items[item_id]
            if library_item:
                library_item.return_item()
                print(f"{library_item.title} er nå returnert.")
                break
            else:
                print("Ugyldig ID")
        except ValueError:
            print("Ugyldig ID")
        except KeyError:
            print("Ugyldig ID")


def find_item(library):  # TODO fix implementation to fit with rest of application,
    print("Søk etter gjenstand")
    title = input("Skriv inn tittel: ")
    items = library.search_items(title)
    if items:
        print("Finner:")
        for item in items:
            print(f"{item.title} ({item.year})")
    else:
        print("Ingen treff")


def list_available_books(library: Library):
    max_items = 5
    page = 1
    while True:
        book_list = library.get_available_books()
        page_content = split_list(book_list, max_items)
        start_index = (page - 1) * max_items + 1
        if len(book_list) == 0:
            print("Ingen bøker tilgjengelig")
            break
        for i, item in enumerate(
            page_content[page - 1],
        ):
            print(f"{i + start_index}. {item.title} ({item.year})")
        if len(page_content) > 1:
            print("> Neste")
        if page > 1:
            print("< Forrige")
        print("#. Tilbake")
        print("0. Avslutt")
        choice = input("Velg: ")
        if choice.isdigit() and int(choice) - 1 in range(len(book_list)):
            item = book_list[int(choice) - 1]
            print(
                f"Tittel:{item.title}",
                f"\nISBN:{item.isbn}",
                f"\nForfattere:[{', '.join(item.authors)}]",
                f"\nÅr:{item.year}",
                f"\nUtgiver:{item.publisher}",
                f"\nSpråk:{item.lang}",
            )
            print("#. Tilbake")
            print("#. Avslutt")
            choice = input("Velg: ")
            if choice == "#":
                pass
            elif choice == "0":
                exit()
            print("\n")
        elif choice == ">":
            page += 1
        elif choice == "<":
            page -= 1
        elif choice == "#":
            return
        elif choice == "0":
            exit()
        else:
            print("Ugyldig valg")


def list_available_movies(library: Library):
    max_items = 5
    page = 1
    while True:
        movie_list = library.get_available_movies()
        page_content = split_list(movie_list, max_items)
        start_index = (page - 1) * max_items + 1
        if len(movie_list) == 0:
            print("Ingen filmer tilgjengelig")
            break
        for i, item in enumerate(page_content[page - 1]):
            print(f"{i + start_index}. {item.title} ({item.year})")
        if page < len(page_content):
            print("> Neste")
        if page > 1:
            print("< Forrige")
        print("#. Tilbake")
        print("0. Avslutt")
        choice = input("Velg: ")
        if choice.isdigit() and int(choice) - 1 in range(len(movie_list)):
            item = movie_list[int(choice) - 1]
            print(
                f"Title: {item.title}",
                f"\nIMDB_ID:{item.imdb_id}",
                f"\nÅr:{item.year}",
                f"\nRegissører: {', '.join(item.directors)}\n",
            )
            print("#. Tilbake")
            print("#. Avslutt")
            choice = input("Velg: ")
            if choice == "#":
                pass
            elif choice == "0":
                exit()
            print("\n")
        elif choice == ">":
            page += 1
        elif choice == "<":
            page -= 1
        elif choice == "#":
            return
        elif choice == "0":
            exit()
        else:
            print("Ugyldig valg")


def _item(item_type, title="Title"):
    return (
        item_type(title=title, directors=["Director"], year=2008, imdb_id="21414")
        if item_type is Movie
        else item_type(title=title, authors=["Author"], isbn="23456", year=2010)
    )


def main():
    library = Library()

    exit_requested = False

    while not exit_requested:
        try:
            print("Meny:")
            print("1. Legg til bok")
            print("2. Legg til film")
            print("3. List tilgjengelige bøker")
            print("4. List tilgjengelige filmer")
            print("5. Lån gjenstand")
            print("6. Returner gjenstand")
            print("7. Finn gjenstand")
            print("0. Avslutt")

            choice = input("Velg et alternativ: ").strip()

            if choice == "1":
                print("\n")
                add_book(library)
                print("\n")
            elif choice == "2":
                print("\n")
                add_movie(library)
                print("\n")
            elif choice == "3":
                print("\n")
                list_available_books(library)
                print("\n")
            elif choice == "4":
                print("\n")
                list_available_movies(library)
                print("\n")
            elif choice == "5":
                print("\n")
                borrow_item(library)
                print("\n")
            elif choice == "6":
                print("\n")
                return_item(library)
                print("\n")
            elif choice == "7":
                print("\n")
                find_item(library)
                print("\n")
            elif choice == "0":
                print("Avslutter…")
                exit_requested = True
            else:
                print("Ugyldig valg.")
        except ValueError as e:
            print(f"[Inputfeil] {e}")


if __name__ == "__main__":
    main()
