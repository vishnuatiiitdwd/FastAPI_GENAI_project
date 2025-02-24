from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
def pdf_(path):
    extract_text=PyPDFLoader(path)
    extraction=extract_text.load()
    extracted_text = "\n".join([page.page_content for page in extraction])

    # return Document(page_content=extracted_text, metadata={"source": path}) 
    return extracted_text