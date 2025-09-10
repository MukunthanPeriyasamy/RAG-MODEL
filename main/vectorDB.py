import os
from langchain_chroma import Chroma
import os
from langchain_community.document_loaders import WebBaseLoader , PyPDFLoader , Docx2txtLoader , TextLoader , UnstructuredPowerPointLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import bs4
from models import embeddings


persist_directory = "./chroma_langchain_db"

# if not os.path.exists(persist_directory):
#     folder_path  = 'D:\\CUBE AI\\rag\\dataset'
#     print("LOADING DOCUMENT..")
#     splitted_docuement = load_and_vectorize(folder_path) # the 'document' is the list that is defined earlier
## this function is for user's to upload and query their own document
document = []

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
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

