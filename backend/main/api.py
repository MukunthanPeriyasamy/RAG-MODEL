from fastapi import FastAPI , UploadFile , File , HTTPException , status
from rag import Rag_Chain
from vectorDB import upload_document_vectorize
from models import llm 
import shutil
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for dev, more secure to use exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str

@app.get('/')
def root():
    return 'Welcome to RAG chat'

@app.post('/upload/')
async def upload(files: list[UploadFile] = File()):
    for file in files:
        temp_file_path = f"temp_{file.filename}"
        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            upload_document_vectorize(temp_file_path, file.filename)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing the file {file.filename}: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

@app.post('/chat/')    
def chat(res : QuestionRequest):
    result = Rag_Chain(res.question,llm)
    return {
        "answer": result
    }

