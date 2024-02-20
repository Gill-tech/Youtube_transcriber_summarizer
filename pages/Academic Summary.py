import streamlit as st
from summarizer import extract_transcript, geneate_academic_summary, generate_keywords
from youtube_id_extractor import extract_video_id

# Title
st.title("Academic YouTube Video Summarizer")

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
                # generating keywords
                with st.spinner("Generating keywords ..."):
                    keywords = generate_keywords(transcript)

                st.markdown(f"### Video Keywords")
                st.write(keywords)

                # spinner to show that the summary is being generated
                with st.spinner("Getting the summary..."):
                    # get the summary based on the transcript
                    try:
                        summary = geneate_academic_summary(transcript)
                        # balloon to show successful generation of the summary
                        st.balloons()
                        # a markdown to display the summary
                        st.markdown(f"### Detailed Summary")
                        st.write(summary)
                    except Exception as e:
                        st.write("Error getting the summary. Please try again.")
                        st.write(e)

            