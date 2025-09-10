from langchain_community.document_loaders import PyPDFLoader , UnstructuredPowerPointLoader , Docx2txtLoader , TextLoader , WebBaseLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from prompt_template import system_prompt
import os 
from vectorDB import retriever


# pressit directory for chroma DB
load_dotenv()

#Intializing the Output Parser
output_parser = StrOutputParser()

print("WORKING...")

persist_directory = "./chroma_langchain_db"

document = []


# Building the RAG chain
def Rag_Chain(question,llm):

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

if __name__ == "__main__":
    while True:
        os.system('cls')
        question = input("\nAsk anyting from the document: \n")

        print("\nLoading.....")
        rag_output = Rag_Chain(question)
        print("\nRESPONSE\n")
        print(rag_output)

        print("Do you want to continue ?: ",end="")
        if input().lower() == 'n':
            break



