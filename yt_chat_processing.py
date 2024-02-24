from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# create vector db
def create_chunk_and_vector_db():
    loader = TextLoader("transcript.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    docs = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_document")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, 
    if the answer is not in the provided context, just say "answer is not available in the context", don't provide wrong answer.
    Context:\n {context}?\n
    Question:\n {question}\n

    Answer:

    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3,
                                   convert_system_message_to_human=True)
    PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model=model, chain_type="studd", prompt=prompt_template)
    return chain

def use_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_document")

    print("Embedding loaded")
    new_db = FAISS.load_local("faiss_index", embeddings)
    print('Database retrieved')
    print("Now searching DB")
    docs = new_db.search(user_question)
    print('Passing to chain')
    chain =  get_conversational_chain()
    print('Getting answer')
    response = chain(
        {"input_documents": docs, "question": user_question}, 
        return_only_outputs=True
    )
    print(response)
    st.write("Reply: ", response["output_text"])
