import io
from PyPDF2 import PdfReader


def pdf_reader(file_content):
  pdf_reader_obj=PdfReader(io.BytesIO(file_content))
  text=""
  for page in pdf_reader_obj.pages:
    text+= page.extract_text()+"\n"

  return text