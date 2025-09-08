from langchain_community.document_loaders import PyPDFLoader , UnstructuredPowerPointLoader , Docx2txtLoader , TextLoader , WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec , Pinecone
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from huggingface_hub import login
from prompt_template import system_prompt
import getpass
import os , json 
import bs4

load_dotenv()

## loading hugging face eapi key
os.getenv('HF_TOKEN')

## loading preplexity api key
if not os.getenv('PPLX_API_KEY'):
    getpass.getpass("Enter the preplexity API: ")

## loading pincone api key
pincone_api_key = os.getenv('PINCONE_API_KEY')
if not pincone_api_key:
    getpass.getpass("Enter the pincone API: ")

## pincone index name
index_name = "rag-embedding-collections-2"
pc = Pinecone(api_key=pincone_api_key)
# Loading the chat model
print("Loading Chat Model...")
llm = init_chat_model(model='sonar',model_provider='perplexity')

# Loading the embedding model from the Hugging face
print("Loading Embedding Model....")
embeddings = HuggingFaceEmbeddings(model='BAAI/bge-base-en-v1.5')

print("WORKING...")
#Intializing the Output Parser
output_parser = StrOutputParser()

document = [] # list that stores all the loaded documents

# Scraping the content from the Erode Sengunthar Engineering College website.
if not pc.has_index(index_name): 
    web_page = [
        "https://erode-sengunthar.ac.in/about-us/",
        "https://erode-sengunthar.ac.in/tap-vision-and-mission/tap-training/",
        "https://erode-sengunthar.ac.in/admission/courses-offered/",
        "https://www.isro.gov.in/profile.html",
        "https://www.isro.gov.in/Gaganyaan.html",
        "https://www.datacamp.com/blog/the-top-5-vector-databases",
        "https://en.wikipedia.org/wiki/Tamil_Nadu",
        "https://en.wikipedia.org/wiki/Nadigar_Sangam",
        "https://en.wikipedia.org/wiki/Erode_Sengunthar_Engineering_College",
        ]

    web_page_id = [
        "column2",
        "tablepress-840",
        "column2",
        "main",
        "main",
        "main",
        "bodyContent",
        "bodyContent",
        "bodyContent",
        ]

    # loading web content
    for i in range(len(web_page)):
        web_path = web_page[i]
        id = web_page_id[i]
        web_loader = WebBaseLoader(
            web_paths=(web_path,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    id=(id)
                )
            ),
        )
        document.extend(
                web_loader.load()
            )

# loading the documents
def load_document(folder_path,document):

    for filename in os.listdir(folder_path):
        file_path  = os.path.join(folder_path,filename)
        
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif filename.endswith('.pptx'):
            loader = UnstructuredPowerPointLoader(file_path)
        elif filename.endswith('.txt'):
            loader = TextLoader(file_path)

        document.extend(loader.load())
    return document

if not pc.has_index(index_name):
    folder_path  = 'D:\\CUBE AI\\rag\\dataset'
    print("LOADING DOCUMENT..")
    document = load_document(folder_path,document) # the 'document' is the list that is defined earlier

    text_splitter =  RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 200,
    length_function = len
)

    split_document = text_splitter.split_documents(document)
    print(f"Document is splitted into {len(split_document)} chunks")


# Loading the Vector DB
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,  # Dimension depends on your embedding model
        metric="cosine",  # cosine, euclidean, or dotproduct
        spec=ServerlessSpec(
            cloud="azure",     # aws, gcp, or azure
            region="us-east-1"  # Choose closest region
        )
    )

index = pc.Index(name=index_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# vectorizing documents
if not pc.has_index(index_name):
    print("VECTORIZING..")
    vectorize = vector_store.add_documents(doacuments=split_document)

# Retriever for retrieving the relavant documnets from the vector DB
retriever = vector_store.as_retriever(kwargs=3)

# Building the RAG chain
def Rag_Chain(question):

    # memory = ""

    # memory_list = return_memory()
    # if memory_list:
    #     for qa in memory_list[-3:]:
    #         memory+= f"Previous Question: {qa['question']}\nPrevious Answer: {qa['answer']}\n"
    # retriever_context = []

    template = system_prompt()
    prompt = ChatPromptTemplate.from_template(template)

    def doc_to_str(docs):
        
        return '\n\n'.join(doc.page_content for doc in docs)

    chain = (
        {'context' : retriever | doc_to_str , 'question' : RunnablePassthrough()}
            | prompt | llm | output_parser
    )
    
    rag_response = chain.invoke(question)
    # add_output_file(retriever_context,question)
    # add_memory_to_rag(question,rag_response)

    return rag_response

# while True:
#     os.system('cls')
#     question = input("\nAsk anyting from the document: \n")

#     print("\nLoading.....")
#     rag_output = Rag_Chain(question)
#     print("\nRESPONSE\n")
#     print(rag_output)

#     print("Do you want to continue ?: ",end="")
#     if input().lower() == 'n':
#         break
