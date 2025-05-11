import os

class UniversalLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        extension = os.path.splitext(self.file_path)[1].lower()
        if extension == ".pdf":
            from pdf_loader import PDFLoader
            loader = PDFLoader()
        elif extension == ".txt":
            from text_loader import TextLoader
            loader = TextLoader()
        elif extension == ".docx":
            from docx_loader import DocxLoader
            loader = DocxLoader()
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load_document(self.file_path)