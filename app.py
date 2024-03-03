import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Youtube Summarizer",
    page_icon=":🎆",
    layout="centered",
    initial_sidebar_state="collapsed",

)

# Main Page Title
st.title("Welcome to the :blue[Youtube Summarizer!]")
# Main Page Description
st.write("This app will take in link of a youtube video and based on your choice of use case, provides or create the important summary points.")

st.write("it has five use cases: General, Academic, Blog Creation, Chat with Youtube Videos and Q&A, and Children YT video recommender")

st.write("Choose the use case and enter the youtube video URL to get the summary of the video")

st.write("Click the button below to carry out the corresponding action to the video")


