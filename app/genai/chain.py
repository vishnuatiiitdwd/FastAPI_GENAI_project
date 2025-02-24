from ..genai.processes import prompting
from ..genai.processes import indexing
from ..genai.processes.models import llm
from app.genai.processes.indexing import get_retriever
from langchain_core.runnables import RunnablePassthrough
from langchain.llms import Ollama

# llm = Ollama(model="llama3.2")

def generate_response(extracted_text, query, current_user_role):
    retriever = get_retriever(extracted_text)
    current_user_role = current_user_role.value 

    chain = (
        {
            "context": retriever.with_config(run_name="docs"),
            "question": RunnablePassthrough(),
            "user_role": RunnablePassthrough()  # Now it's a string
        }
        | prompting.prompt
        | llm
    )

    response = chain.invoke(query, max_length=300)
    return response
