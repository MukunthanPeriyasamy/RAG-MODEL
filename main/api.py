from fastapi import FastAPI
from rag import Rag_Chain

app = FastAPI()

@app.get('/')
def root():
    return 'Welcome to RAG chat'

@app.get('/chat/{question}')
def chat(question):
    result = Rag_Chain(question)

    return result