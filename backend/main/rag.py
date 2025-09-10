from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from prompt_template import system_prompt
from vectorDB import retriever


#Intializing the Output Parser
output_parser = StrOutputParser()

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





