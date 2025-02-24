from langchain_core.prompts import ChatPromptTemplate

template = """
                User: You are an {user_role} that follows instructions extremely well.
                Please be truthful and give direct answers. Please tell 'I don't know' if user query is not in CONTEXT
                Keep in mind, you will lose the job, if you answer out of CONTEXT questions
                CONTEXT: {context}
                Query: {question}
                Remember only return AI answer
                Assistant:
                """
prompt = ChatPromptTemplate.from_template(template)
