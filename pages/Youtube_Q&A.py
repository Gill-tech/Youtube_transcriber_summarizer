import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils import extract_transcript
from youtube_id_extractor import extract_video_id
from yt_QandA_helper_function import create_chunk_and_vector_db, user_input
# from prefect import task, flow


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page Config
st.set_page_config("Chat With Youtube Videos")

# Page title
st.title("Chat with Youtube Videos using Gemini")


# @flow(name="Youtube Rag System")
def main():
    # Initialize session_state.transcript
    if "transcript" not in st.session_state:
        st.session_state.transcript = None

    # URL entry
    youtube_url = st.text_input("Enter the YouTube video URL or link")

    # show the user the summary of the video
    st.write("Click the button below to process the YT video")

    if st.button("process video"):
        if youtube_url is None or youtube_url.strip() == "":
            st.write("The input is empty, enter a valid URL.")
        else:
            youtube_id = extract_video_id(youtube_url)

            # If YouTube ID is valid
            if youtube_id:
                # Extract transcript from the YouTube video
                with st.spinner("Getting the transcript..."):
                    try:
                        transcript = extract_transcript(youtube_url)
                    except Exception as e:
                        st.write("Error getting the transcript:", str(e))
                        transcript = "Error"

                # If transcript extraction is successful
                if transcript != "Error":
                    # Save transcript to a text file
                    with open('transcript.txt', 'w') as f:
                        f.write(transcript)
                    st.balloons()

                    # Process the transcript
                    with st.spinner("Preparing for Q & A..."):
                        create_chunk_and_vector_db()
                    st.balloons()

                    # Store state in session_state
                    st.session_state.transcript = transcript
                else:
                    st.write("Error getting the transcript. Please check the video URL.")

    # Display a message while waiting for the transcript to be generated
    if st.session_state.transcript is None and "processing" not in st.session_state:
        st.session_state.processing = True
        with st.spinner('Waiting for transcript generation...'):
            st.empty()

    # Taking User Input
    user_question = st.text_input("Enter your question for the youtube video: ")

    # Check if transcript is ready and user has submitted a question
    if st.session_state.transcript is not None and user_question and st.button("Submit & Process"):
        with st.spinner('Getting answer'):
            # Passing the question to the chain
            response = user_input(user_question)
            st.markdown(f"### Response")
            st.write(response)


# Run the main function
if __name__ == "__main__":
    main()
