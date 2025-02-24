import re
from services import ocr_services
from services import transction
from services import summarization
from .embedding import embedding_vectorstore
def identification_file(path):
    image_matching=re.match(r'[a-zA-Z0-9\-/_@]+\.(img|png|jpg|jpeg)$',path)
    audio_matching=re.match(r'[a-zA-Z0-9\-/_@]+\.(mp3|wav)$',path)
    pdf_matching=re.match(r'[a-zA-Z0-9\-/_@]+\.pdf$',path)
    print("---")
    if image_matching:
        print("------")
        data=ocr_services.ocr_function(path)
        print(data)
        embedding_vectorstore(data)        
    elif audio_matching:
        print("----")
        data=transction.audio_(path)
        embedding_vectorstore(data)
    elif  pdf_matching:
        print("------")
        data=summarization.pdf_(path)
        print("--")
        print(data)
        embedding_vectorstore(data)
        
identification_file("data/audio.mp3")        

 




