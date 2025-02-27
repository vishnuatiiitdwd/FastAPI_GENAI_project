from ..genai.processes import prompting
from ..genai.processes import indexing
from ..genai.processes.models import llm
from app.genai.processes.indexing import get_retriever
from langchain_core.runnables import RunnablePassthrough
from langchain.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate


def generate_response(extracted_text, query, current_user_role):
    retriever = get_retriever(extracted_text)
    current_user = current_user_role.value 

    template="""
        Me: I am the {user_role} and you are the AI assistant that follows instructions extremely well. 
        Please be truthful and give direct answers if and only if  my role relates with the provided CONTEXT. 
        Please tell 'I don't know' if my query is not in CONTEXT and my role does not relate with the CONTEXT.
        Remember, you will lose the job if you answer out of CONTEXT questions.
        CONTEXT: {context}
        Query: {question}
        Remember, only return the AI answer if the my role relates with the context. Otherwise, say 'I don't know.'
        Assistant:
        """.format(user_role=current_user, context="{context}", question="{question}")
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {
            "context": retriever.with_config(run_name="docs"),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )
    
    response = chain.invoke(query, max_length=300)
    return response
