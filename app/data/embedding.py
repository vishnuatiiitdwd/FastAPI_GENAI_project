from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
# from langchain_huggingface import HuggingFaceEndpointEmbeddings
import numpy as np
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"]=os.getenv("HUGGINGFACEHUB_API_TOKEN")


embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embedding_vectorstore(data):
    ##chunking the data 
    data=[data]
    chunk=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    split_text=chunk.create_documents(data)
    ##vector databasec
    print("________")
    print(data)
    print("-----")
    print(split_text)
    database=FAISS.from_documents(split_text,embedding)
    database.save_local('Model_index')
    print('sucessfully')
    return {"data is successfully append"}



    



    

