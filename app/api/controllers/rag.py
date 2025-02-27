from app.genai.services.transcribing import model_audio
from app.genai.services.ocr import reader
from app.genai.services.summarizing import PyPDFLoader
from app.genai.chain import generate_response
from langchain.schema import Document

def rag_response(filepath,query,file_extension,current_user_role):
    if file_extension == ".wav":
        res = model_audio.transcribe(filepath)
        if isinstance(res, dict) and "text" in res:
            res = res["text"]
        answerfromthellm = generate_response(Document(page_content=res),query,current_user_role)
        return answerfromthellm
    elif file_extension == "jpg":
        response = reader.readtext(filepath)
        text = [textscarping[1] for textscarping in response]
        text2 = ' '.join(text)
        answerfromthellm = generate_response(Document(page_content=text2),query,current_user_role)
        return answerfromthellm
    else:
        response = PyPDFLoader(file_path=filepath)
        extraction = response.load()
        text = []
        for word in extraction:
            text.append(word.page_content)
        final_text = ' '.join(text)
        answerfromthellm = generate_response(Document(page_content=final_text),query,current_user_role)
        return answerfromthellm




    