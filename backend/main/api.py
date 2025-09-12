from fastapi import FastAPI , UploadFile , File , HTTPException , status
from rag import Rag_Chain
from vectorDB import upload_document_vectorize
from models import llm 
import shutil
import os

app = FastAPI()

@app.get('/')
def root():
    return 'Welcome to RAG chat'

@app.post('/upload/')
def upload(files: list[UploadFile] = File()):
    for file in files:
        temp_file_path = f"temp_{file.filename}"
        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            if upload_document_vectorize(temp_file_path, file.filename):
                return {"message": "Files uploaded and processed successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing files")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

@app.get('/chat/{question}')    
def chat(question):
    result = Rag_Chain(question,llm)
    return result

