from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from data.embedding import embedding
from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import os
model=OllamaLLM(model="llama2")
os.environ["HUGGINGFACEHUB_API_TOKEN"]=os.getenv("HUGGINGFACEHUB_API_TOKEN")

def retriever_docs(query):
    new_db = FAISS.load_local("/Users/bootlabs/Genai-project-folder/FastAPI_GENAI_project/Model_index", embedding, allow_dangerous_deserialization=True)

    db= new_db.as_retriever(search_type="similarity",search_kwargs={"k":3})
    return db.invoke(query)
    

def generate_role_based_response(query, role):
    
    retrieved_docs = retriever_docs(query) 
    retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

    role_prompt = {
        "Legal Assistant": f"Extract the legal clauses and summarize the contract terms based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Finance Assistant": f"Answer queries related to bank policies, loans, and credits based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Academic Assistant": f"Summarize the research paper and generate citations based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Healthcare Assistant": f"Extract the patient history and suggest treatments based on the reference:\n\n{retrieved_text} \n\nQuery: {query}",
        "Business Assistant": f"Transcribe the meeting and extract action items based on the reference:\n\n{retrieved_text} \n\nQuery: {query}"
    }

    if role not in role_prompt:
        return "Role not specified correctly. Please choose from: 'Legal Assistant', 'Finance Assistant', 'Academic Assistant', 'Healthcare Assistant', 'Business Assistant'."

    prompt = role_prompt[role]

    return model.invoke(prompt)



response=generate_role_based_response("what is Finance management? ","Finance Assistant")
print(response)
#return {"response":respone}
   






