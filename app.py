import streamlit as st
from utils import extract_transcript, generate_general_summary, geneate_academic_summary, generate_keywords, create_contents
from youtube_id_extractor import extract_video_id


st.set_page_config(page_title="YouTube Video Summarizer", page_icon="📹", layout="centered", initial_sidebar_state="auto")

st.title("Welcome to the YouTube Video Summarizer")

st.write("This app will take in link of a youtube video and based on your choice of use case, provides or create the important summary points.")

# Create a radio button group with 'Academic' and 'Content Creation' options
option = st.radio(
   "What is your preference?",
   ('General', 'Academic', 'Content Creation'))

st.write(f'You selected {option}.')

youtube_url = st.text_input("Enter the youtube video URL")

# display the thumbnail of the video

# show the user the summary of the video
st.write("Click the button below to get the summary of the video")
if st.button("Get Detailed Summary"):

    # display the thumbnail of the video
    st.markdown("### Video Thumbnail")
    if youtube_url:
        youtube_id = extract_video_id(youtube_url)
        st.image(f"http://img.youtube.com/vi/{youtube_id}/0.jpg", use_column_width=True)

    # a spinner to show that the transcript is being extracted
    with st.spinner("Getting the transcript..."):
    # get the transcript from the youtube video
        transcript = extract_transcript(youtube_url)
        # baloon to show successful extraction of the transcript
        st.balloons()
    # cretaing a function to call the right function for chosen use cases
    def select_method(option, transcript=transcript):
        if option == 'General':
            method = generate_general_summary(transcript)
        elif option == "Academic":
            method = geneate_academic_summary(transcript)
        else:
            method = create_contents(transcript)
        return method
    
    # if there is an error getting the transcript, display an error message
    if transcript == "Error":
        st.write("Error getting the transcript. Please check the video URL.")
    else:
        # generating keywords
        with st.spinner("Generating keywords ..."):
            keywords = generate_keywords(transcript)

        st.markdown(f"### Video Keywords")
        st.write(keywords)

        # spinner to show that the summary is being generated
        with st.spinner("Getting the summary..."):
            # get the summary based on the transcript
            try:
                summary = select_method(option)
                # baloon to show successful generation of the summary
                st.balloons()
                # a markdown to display the summary
                st.markdown(f"### Detailed Summary")
                st.write(summary)
            except Exception as e:
                st.write("Error getting the summary. Please try again.")
                st.write(e)
            