from langchain_chroma import Chroma
import os
from langchain_community.document_loaders import PyPDFLoader , Docx2txtLoader , TextLoader , UnstructuredPowerPointLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from models import embeddings

document = []


embedding_dim = len(embeddings.embed_query("hello world"))
index = faiss.IndexFlatL2(embedding_dim)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

def upload_document_vectorize(file_path,filename):
        
    if filename.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif filename.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif filename.endswith('.pptx'):
        loader = UnstructuredPowerPointLoader(file_path)
    elif filename.endswith('.txt'):
        loader = TextLoader(file_path)

    document.extend(loader.load())
    text_splitter =  RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 200,
    length_function = len
)

    splitted_docuements = text_splitter.split_documents(document)

    vector_store.add_documents(documents=splitted_docuements)
    
# Retriever for retrieving the relavant documnets from the vector DB
retriever = vector_store.as_retriever(kwargs=3)

