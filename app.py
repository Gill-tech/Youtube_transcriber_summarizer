import streamlit as st
from summarizer import extract_transcript, generate_gemini_content


st.title("Welcome to the YouTube Video Summarizer")

st.write("This app will take in the transcript text of a youtube video and summarize the entire video and provide the important summary points within 200 to 500 words.")

youtube_url = st.text_input("Enter the youtube video URL")

# display the thumbnail of the video

# show the user the summary of the video
st.write("Click the button below to get the summary of the video")
if st.button("Get Detailed Summary"):

    # display the thumbnail of the video
    st.markdown("### Video Thumbnail")
    if youtube_url:
        st.image(f"http://img.youtube.com/vi/{youtube_url.split('=')[1]}/0.jpg", use_column_width=True)

    # get the transcript from the youtube video
    transcript = extract_transcript(youtube_url)
    # baloon to show that transcript has being extracted
    st.balloons()
    st.write()
    # if there is an error getting the transcript, display an error message
    if transcript == "Error":
        st.write("Error getting the transcript. Please check the video URL.")
    else:
        # spinner to show that the summary is being generated
        st.spinner("Getting the summary...")
        # get the summary based on the transcript
        summary = generate_gemini_content(transcript)
        # a markdown to display the summary
        st.markdown(f"### Detailed Summary")
        st.write(summary)