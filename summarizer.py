import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


prompt = """You are a youtube video summarizer. You will take in the transcript test
and summarizing the entire video and providing the important summary 
points within 200 to 500 words. Please provide the summary of the text given here:  """

# getting the transcript from the youtube video
def extract_transcript(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text = ""
        for i in transcript:
            transcript_text += i['text'] + " "

        return transcript_text
    except Exception as e:
        return "Error"

#getting the summary based on prompt and transcript
def generate_gemini_content(transcript, prompt=prompt):

    model = genai.GenerationModel("gemini-pro")

    response = model.generate_content(prompt+transcript, max_length=500)