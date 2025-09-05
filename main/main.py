from langchain_community.document_loaders import PyPDFLoader , UnstructuredPowerPointLoader , Docx2txtLoader , TextLoader , WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec , Pinecone
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain.output_parsers import StructuredOutputParser
from huggingface_hub import login
from getpass import getpass
import os , json 
import bs4