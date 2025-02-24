from langchain_huggingface import HuggingFaceEmbeddings
from langchain.llms import Ollama

model = "llama3.2"

model_name = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=model_name)

llm = Ollama(model=model)