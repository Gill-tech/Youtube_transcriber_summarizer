import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from summarizer import extract_transcript
from youtube_id_extractor import extract_video_id
from yt_chat_processing import create_chunk_and_vector_db, use_input

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page Config
st.set_page_config("Chat With Youtube Videos")

# Page title
st.title("Chat with Youtube Videos using Gemini")


########### Functions ###########

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


@st.cache_data
def extract_and_process(youtube_url):
    # Extract video ID from YouTube URL
    youtube_id = extract_video_id(youtube_url)
    
    # If YouTube ID is valid
    if youtube_id:

        # Extract transcript from the YouTube video
        transcript = extract_transcript(youtube_url)

        # If transcript extraction is successful
        if transcript != "Error":
            # Save transcript to a text file
            with open('transcript.txt', 'w') as f:
                f.write(transcript)
            # Process the transcript
            with st.spinner("Preparing for Q & A..."):
                create_chunk_and_vector_db()
                st.balloons()
        else:
            st.write("Error getting the transcript. Please check the video URL.")
    # Return thumbnail URL and transcript
    return  transcript

def main():
    # URL entry
    youtube_url = st.text_input("Enter the YouTube video URL or link")

    # show the user the summary of the video
    st.write("Click the button below to get the summary of the video")

    if st.button("process video"):

        if youtube_url is None or youtube_url.strip() == "":
            st.write("The input is empty, enter a valid URL.")
        else:
            transcript = extract_and_process(youtube_url)
            # Store state in session_state
            st.session_state.transcript = transcript
    
    # Taking User Input
    user_question = st.text_input("Enter your question for the youtube video: ")
    if st.session_state.transcript is not None:
        if st.button("Submit & Process"):
            with st.spinner('Getting answer'):
                # Passing the question to the chain
                if user_question:
                    response = user_input(user_question)
                    st.markdown(f"### Response")
                    st.write(response)


# Run the main function
if __name__ == "__main__":
    main()
