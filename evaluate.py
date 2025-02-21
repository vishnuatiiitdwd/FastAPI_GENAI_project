
# pip install streamlit langchain google-generativeai PyPDF2 faiss-cpu python-dotenv ragas


import app
from ragas import EvaluationDataset
from langchain_google_genai import ChatGoogleGenerativeAI
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from langchain.schema import Document
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness

# Sample questions and ground truth answers
sample_questions = ['What is Variables?']
ground_truth = [
    "Variables are defined with the assignment operator, '='. Python is dynamically "
    "typed, meaning that variables can be assigned without declaring their type, and "
    "that their type can change. Values can come from constants, from computation "
    "involving values of other variables, or from the output of a function. Python"
]


dataset = []


for query, reference in zip(sample_questions, ground_truth):
    
    relevant_docs = app.get_relevant_document(query)
    
    if isinstance(relevant_docs[0], Document):
        relevant_docs_text = [doc.page_content for doc in relevant_docs]
    else:
        relevant_docs_text = relevant_docs  

   
    response = app.get_response(query, relevant_docs)

    dataset.append(
        {
            "user_input": query,
            "retrieved_contexts": relevant_docs_text,  
            "response": response,
            "reference": reference
        }
    )

print(dataset)

evaluation_dataset = EvaluationDataset.from_list(dataset)
model = ChatGoogleGenerativeAI(model="gemini-pro")
# embeddings = ollama.Embeddings("llama3.2")
evaluator_llm = LangchainLLMWrapper(model)

result = evaluate(
    dataset=evaluation_dataset,
    metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
    llm=evaluator_llm
)

print(result)
