from fastapi import FastAPI , UploadFile , File , HTTPException , status
from rag import Rag_Chain
from vectorDB import upload_document_vectorize
import shutil
import os

app = FastAPI()

@app.get('/')
def root():
    return 'Welcome to RAG chat'

@app.post('/upload/{file_name}')
def upload_docs_and_chat(file: UploadFile = File()):
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(file.filename)
        if upload_document_vectorize(temp_file_path,file.filename):
            return HTTPException(status_code=status.HTTP_202_ACCEPTED)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
@app.get('/chat/{question}')    
def chat_with_uploded_docs(question):
    result = Rag_Chain(question)
    return result

