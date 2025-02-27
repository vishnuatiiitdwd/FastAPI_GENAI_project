from langchain_core.prompts import ChatPromptTemplate

template="""
        Me: I am the {user_role} and you are the AI assistant that follows instructions extremely well. 
        Please be truthful and give direct answers if and only if  my role matches with the provided CONTEXT. 
        Please tell 'I don't know' if my query is not in CONTEXT and my role does not match with the CONTEXT.
        Remember, you will lose the job if you answer out of CONTEXT questions.
        CONTEXT: {context}
        Query: {question}
        Remember, only return the AI answer if the my role matches with the context. Otherwise, say 'I don't know.'
        Assistant:
        """.format(user_role="{user_role}", context="{context}", question="{question}")
prompt = ChatPromptTemplate.from_template(template)
