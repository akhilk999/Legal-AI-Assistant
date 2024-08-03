from PyPDF2 import PdfReader
import os

text_folder = "text case files"
pdf_folder = "pdf case files"

file = input("Enter PDF file name (no .PDF): ")
reader = PdfReader(os.path.join(pdf_folder, file + '.pdf'))
file_path = os.path.join(text_folder, file + ".txt")

with open(file_path, 'w') as f:
    for page in reader.pages:
        f.write(page.extract_text())