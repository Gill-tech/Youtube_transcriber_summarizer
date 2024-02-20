import urllib
import warnings
from pathlib import Path as p
from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Gemini pro model
model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=GOOGLE_API_KEY,
                             temperature=0.2,convert_system_message_to_human=True)

# setting the embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

def create_vector_index(context):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    texts = text_splitter.split_text(context)

    # creating vector index
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})
    return vector_index

# Setting the Retrieval System

def run_qa_chain(vector_index, context, question):
    # custom chain
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, 
    don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    response = qa_chain({"query": question})
    return response['result']
    # response_chunks = response.split(' ')

    # # Yield each chunk
    # for chunk in response_chunks:
    #     yield chunk
