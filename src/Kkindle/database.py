# src/Kkindle/database.py

from tinydb import TinyDB, Query

class BookDatabase:
    def __init__(self, db_path='books.json'):
        self.db = TinyDB(db_path)
        self.books_table = self.db.table('books')

    def add_book(self, title, author, file_path):
        """Adiciona um livro ao banco de dados."""
        self.books_table.insert({
            'title': title,
            'author': author,
            'file_path': file_path
        })

    def get_all_books(self):
        """Retorna todos os livros no banco de dados."""
        return self.books_table.all()

    def find_book_by_title(self, title):
        """Procura um livro pelo título."""
        Book = Query()
        return self.books_table.search(Book.title == title)

    def remove_book(self, title):
        """Remove um livro pelo título."""
        Book = Query()
        self.books_table.remove(Book.title == title)
