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
st.title("YouTube Video Q & A")


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

# a function to wrap everything

def main():
# URL entry
    youtube_url = st.text_input("Enter the youtube video URL or link")

    # show the user the summary of the video
    st.write("Click the button below to get the summary of the video")
    if st.button("Get Detailed Summary"):

        # display the thumbnail of the video
        st.markdown("### Video Thumbnail")
        if youtube_url is None or youtube_url.strip() == "":
            st.write("The input is empty, enter a valid URL.")
        else:
            youtube_id = extract_video_id(youtube_url)
            if youtube_id is None or youtube_id.strip() == "":
                st.write("Invalid YouTube URL. Please enter a valid URL.")
            else:
                st.image(f"http://img.youtube.com/vi/{youtube_id}/0.jpg", use_column_width=True)

                # a spinner to show that the transcript is being extracted
                with st.spinner("Getting the transcript..."):
                    # get the transcript from the youtube video
                    transcript = extract_transcript(youtube_url)
                    # baloon to show successful extraction of the transcript
                    st.balloons()

                # if there is an error getting the transcript, display an error message
                if transcript == "Error":
                    st.write("Error getting the transcript. Please check the video URL.")
                else:
                    # saving the transcript in a text file
                    with open('transcript.txt', 'w') as f:
                        f.write(transcript)
                    
                    # processing the transcript
                    with st.spinner("Preparing for Q & A..."):
                            create_chunk_and_vector_db()
                            st.balloons()
                            st.success("Done")
                    # Next Phase
                    st.header("Chat with Youtube Videos using Gemini")

                    # Taking User Input
                    user_question = st.text_input("Enter your question for the youtube video: ")

                    if st.button("Submit & Process"):
                    # Passing the question to the chain
                        if user_question:
                            st.write("PASSED TO CHAIN")
                            use_input(user_question)


        
if __name__ == "__main__":
    main()
