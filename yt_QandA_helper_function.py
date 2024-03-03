from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
# from prefect import task, flow

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# create vector db
# @task(log_prints=True, cache_result_in_memory=True, task_run_name="Create Chunk and Vector DB", retry_delay_seconds=5, tags=["youtube", "transcript"])
def create_chunk_and_vector_db():
    loader = TextLoader("transcript.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    docs = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", task_type="retrieval_document")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")

# @task(log_prints=True, cache_result_in_memory=True, task_run_name="Get Conversational Chain", retry_delay_seconds=5, tags=["youtube", "conversational"])
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details and explain it better that it is in the context, 
    if the answer is not in provided context or even out of the scope of the context just say,
    "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3, convert_system_message_to_human=True)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

# @flow(name="User Input", cache_result_in_memory=True)
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", task_type="retrieval_document")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents":docs, "question": user_question},
        return_only_outputs=True
    )

    return response["output_text"]

