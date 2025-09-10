
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os , getpass
load_dotenv()


## loading hugging face eapi key
os.getenv('HF_TOKEN')

os.getenv('LANGSMITH_TRACING')
## loading preplexity api key
if not os.getenv('PPLX_API_KEY'):
    getpass.getpass("Enter the preplexity API: ")

## loading pincone api key
pincone_api_key = os.getenv('PINCONE_API_KEY')
if not pincone_api_key:
    getpass.getpass("Enter the pincone API: ")

# Loading the chat model
print("Loading Chat Model...")
llm = init_chat_model(model='sonar',model_provider='perplexity')

# Loading the embedding model from the Hugging face
print("Loading Embedding Model....")
embeddings = HuggingFaceEmbeddings(model='BAAI/bge-base-en-v1.5')