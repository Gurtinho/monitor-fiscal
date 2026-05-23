from PyPDF2 import PdfReader

def pdf_tem_paginas(path: str) -> bool:
    try:
        reader = PdfReader(path)
        return len(reader.pages) > 0
    except:
        return False