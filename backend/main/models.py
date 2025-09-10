
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os 
load_dotenv()


## loading hugging face eapi key
os.getenv('HF_TOKEN')

os.getenv('LANGSMITH_TRACING')
## loading preplexity api key
os.getenv('PPLX_API_KEY')
# Loading the chat model
llm = init_chat_model(model='gemini-2.5-flash',model_provider='google_genai')

# Loading the embedding model from the Hugging face
embeddings = HuggingFaceEmbeddings(model='BAAI/bge-base-en-v1.5')