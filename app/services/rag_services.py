from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from ..data.embedding import embedding
from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import os
model=OllamaLLM(model="llama3.2")
os.environ["HUGGINGFACEHUB_API_TOKEN"]=os.getenv("HUGGINGFACEHUB_API_TOKEN")

def retriever_docs(query):
    new_db = FAISS.load_local("/Users/bootlabs/testingforproject/FastAPI_GENAI_project/FastAPI_GENAI_project/app/Model_index", embedding, allow_dangerous_deserialization=True)

    db= new_db.as_retriever(search_type="similarity",search_kwargs={"k":3})
    return db.invoke(query)
    

def generate_role_based_response(query, role):
    
    retrieved_docs = retriever_docs(query) 
    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

    role_prompt = {
        "Lawyer": f"Extract the legal clauses and summarize the contract terms based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Banker": f"Answer queries related to bank policies, loans, and credits based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Student": f"Summarize the research paper and generate citations based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Doctor": f"Extract the patient history and suggest treatments based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Enterprise": f"Transcribe the meeting and extract action items based on the reference:\n\n{retrieved_text} \n\nQuery: {query}"
    }

    if role not in role_prompt:
        return "Role not specified correctly. Please choose from: 'Lawyer', 'Banker', 'Student', 'Doctor', 'Enterprise'."

    prompt = role_prompt[role]

    return model.invoke(prompt)



response=generate_role_based_response("what is Finance management? ","Finance Assistant")

   






