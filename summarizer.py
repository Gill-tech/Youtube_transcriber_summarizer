import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


gen_prompt = """You are a youtube video summarizer. You will take in the transcript text
, you will summarize the entire video and provide the important summary 
points. Please provide the summary of the text given here:  """

keyword_extraction_prompt = """You are an experienced Youtube video keyword extractor. 
You will take in the transcript text, properly analyze the texts,
rank the keywords and extract the top 10 keywords.
Please provide the top 10 keywords from the text given here:  """

academic_prompts = """
You are an experienced Youtube academic video summarizer.
You method of summarizing academic videos is to take in the Youtube video transcript text,
you take a look into the transcript and understand the main points of the video.
You then create a summary in a detailed manner, providing the important summary points.
The summary is placed in sections and subsections as per the video content. 
Then finally present it in a well structured manner.

Please provide the summary of the text given here: 
"""

######### Blog Content Prompts #########
blog_content_prompts = """
You are an experienced Youtube blog content creator.
You method of creating blog content is to take in the Youtube video transcript text,
you take a look into the transcript and understand the main points of the video.
You then create 5 to 7 blog content points from the video transcript.

You think about recent trends and topics that are popular in the industry corresponding to the video context.
After several consideration and excellent research, you create the blog contents.
You mention an attractive title for each blog, then the blog content will come under it. 
For every blog content, you make sure that the word count is between 50 to 100 words.
Enhance the blog content to make sure it's very interesting to read.

Please provide the blog content points from the text given here: 
"""

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
def generate_general_summary(transcript, prompt=gen_prompt):

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

def generate_keywords(transcript, prompt=keyword_extraction_prompt):

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

def geneate_academic_summary(transcript, prompt=academic_prompts):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

def create_contents (transcript, prompt=blog_content_prompts):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text