from langchain.text_splitter import RecursiveCharacterTextSplitter
from .models import embeddings
import pickle
from langchain.vectorstores import FAISS
filepath = "file_store.pkl"


def get_retriever(docs):

    text_splitter = RecursiveCharacterTextSplitter(separators=['\n\n','\n','.',','],chunk_size=300)
    splits = text_splitter.split_documents([docs])
    if splits:
        vector_store = FAISS.from_documents(splits,embeddings)
    else:
        raise Exception()
    with open(filepath,"wb") as f:
        pickle.dump(vector_store,f)
    with open(filepath,"rb") as f:
        vector_store_retriver = pickle.load(f)
        retriever = vector_store_retriver.as_retriever()
    return retriever