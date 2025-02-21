import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv





# Loading API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
groq_api_key=os.getenv('GROQ_API_KEY')

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    texts = ""
    if not pdf_docs:
        return texts
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            texts += page.extract_text() or ""
    return texts

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

# Function to create and save vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


#  function to call chatgenarative llm:
def get_conversational_chain():
    prompt_template = PromptTemplate(
        template="""
        You are a code explanation assistant. Your task is to explain the code from the provided context as clearly and thoroughly as possible.  
        If the code or relevant explanation is not available in the context, respond with: "Explanation is not available."  

        Context (Code or Documentation):  
        {context}  

        Question:  
        {question}  

        Explanation:
        """,
        input_variables=["context", "question"],
    )
    
    model = ChatGoogleGenerativeAI(model="gemini-pro")
   

    return load_qa_chain(model, chain_type="stuff", prompt=prompt_template)


#ton get the relevant document
def get_relevant_document(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    docs = new_db.similarity_search(user_question,top_k=10)
    return docs
    
#getting the response from llm
def get_response(query, relevant_docs):
    chain = get_conversational_chain()
    
    response = chain.invoke({"input_documents": relevant_docs, "question": query}) 
    
    return response["output_text"] 



# Function to process user question
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    
    response = chain.invoke({"input_documents": docs, "question": user_question}) 
    
    return response["output_text"]  

# front end part
def main():
    st.set_page_config(page_title="Chat with PDFs", layout="wide")
    st.header("CODE Explanation Bot Using Gemini")
    
    user_question = st.text_input("Ask a Question from the PDF Files")
    
    # Added Submit Button
    if st.button("Submit"):
        if user_question.strip():
            with st.spinner("Loading your answer..."):
                #here i am calling user input function
                answer = user_input(user_question)
                st.write(answer)
        else:
            st.warning("Please enter a question before submitting!")

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDF Files", type=["pdf"], accept_multiple_files=True)
        
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                #calling the function for extract the text from pdf
                raw_text = get_pdf_text(pdf_docs)
                
                if not raw_text.strip():
                    st.error("No text found in uploaded PDFs. Please upload valid PDF files.")
                    return
                #calling the chunk function for text chunk
                text_chunks = get_text_chunks(raw_text)
                #calling vectore storing functions
                get_vector_store(text_chunks)
                st.success("PDFs processed successfully!")

if __name__ == "__main__":
    main()











