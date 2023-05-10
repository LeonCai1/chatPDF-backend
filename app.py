from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
import glob, os
import qdrant_client
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
    return {"OPEN_AI_KEY": OPEN_AI_KEY}

#TODO: fine-tune the parameters of loader and splitter
def load_pdf():
    pages = []
    for file in glob.glob("test_data/*.pdf"):
        loader = UnstructuredPDFLoader(file)
        pages+=loader.load_and_split()
    return pages
    
#TODO: implement the method
def generate_prompt():
    return None

#TODO: fine-tune the parameters of chain, embedding model, llm, and db
def load_chain():
    embeddings = OpenAIEmbeddings(openai_api_key=env["OPEN_AI_KEY"])
    if(not os.path.exists("../chatPDF/data/local_qdrant/collection/my_documents")):
        #load and split input files
        texts = load_pdf()

        #embed the input files and load it to DB
        qdrant = Qdrant.from_documents(
        texts, embeddings, 
        path="../chatPDF/data/local_qdrant",
        collection_name="my_documents",
         )
    else:
        client = qdrant_client.QdrantClient(
        path="../chatPDF/data/local_qdrant",
        )
        qdrant = Qdrant(
            client=client, collection_name="my_documents", 
            embeddings=embeddings
        )

    #construct a qa chain with customized llm and db
    chain = load_qa_chain(OpenAI(model_name="text-davinci-003", openai_api_key=env["OPEN_AI_KEY"], temperature=0), chain_type="map_reduce")
    qa = RetrievalQA(combine_documents_chain=chain, retriever=qdrant.as_retriever())

    return qa

def ask_and_answer():
    print("Type exit to quite")
    print("-"*30)
    while (True):
        question = input("You: ")
        if (question == "exit"):
            break
        
        answer = qa.run(question)
        print("Chatbot: " + answer + "\n")
    print("program terminated by user")

env = load_env()
qa = load_chain()
ask_and_answer()




