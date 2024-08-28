# src/Kkindle/__main__.py

from app import BookReaderApp

def main():
    app = BookReaderApp('Book Reader', 'org.example.bookreader')
    app.main_loop()

if __name__ == '__main__':
    main()