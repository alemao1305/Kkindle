# src/Kkindle/app.py

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import fitz  # PyMuPDF para PDFs
from ebooklib import epub
import mobi  # Importar a biblioteca mobi
from database import BookDatabase  # Importando a classe do banco de dados

class BookReaderApp(toga.App):

    def startup(self):
        # Inicializar o banco de dados
        self.db = BookDatabase()

        # Criar a janela principal
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Adicionar um botão para abrir um livro
        open_button = toga.Button(
            'Abrir Livro',
            on_press=self.open_book,
            style=Pack(padding=10)
        )
        main_box.add(open_button)

        # Adicionar uma área de texto para mostrar o conteúdo do livro
        self.text_area = toga.MultilineTextInput(style=Pack(flex=1))
        main_box.add(self.text_area)

        # Configurar a janela principal
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def open_book(self, widget):
        # Diálogo para selecionar um arquivo
        file_path = self.main_window.open_file_dialog(
            title='Selecione um livro para abrir',
            file_types=['pdf', 'epub', 'mobi']
        )

        if file_path:
            if file_path.endswith('.pdf'):
                self.read_pdf(file_path)
            elif file_path.endswith('.epub'):
                self.read_epub(file_path)
            elif file_path.endswith('.mobi'):
                self.read_mobi(file_path)
            else:
                self.main_window.info_dialog('Erro', 'Formato de arquivo não suportado.')

    def read_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ''
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text()
            self.text_area.value = text
            self.db.add_book('Título PDF', 'Autor PDF', file_path)
        except Exception as e:
            self.main_window.info_dialog('Erro', f'Não foi possível ler o PDF: {str(e)}')

    def read_epub(self, file_path):
        try:
            book = epub.read_epub(file_path)
            text = ''
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    text += item.get_content().decode('utf-8')
            self.text_area.value = text
            self.db.add_book('Título EPUB', 'Autor EPUB', file_path)
        except Exception as e:
            self.main_window.info_dialog('Erro', f'Não foi possível ler o EPUB: {str(e)}')

    def read_mobi(self, file_path):
        try:
            mobi.extract(file_path, "temp_mobi_output")
            with open("temp_mobi_output/mobi7/book.html", "r", encoding='utf-8') as f:
                text = f.read()
            self.text_area.value = text
            self.db.add_book('Título MOBI', 'Autor MOBI', file_path)
        except Exception as e:
            self.main_window.info_dialog('Erro', f'Não foi possível ler o MOBI: {str(e)}')

def main():
    return BookReaderApp('Book Reader', 'org.example.bookreader')
