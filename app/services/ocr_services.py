import easyocr
from langchain.schema import Document
def ocr_function(path):
    a=easyocr.Reader(['en'])
    b=a.readtext(path) 
    text=[ textscarping[1] for textscarping in b]
    text2=" ".join(text)
    # document = Document(page_content=text2)
    return text2