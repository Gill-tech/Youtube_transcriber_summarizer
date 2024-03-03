import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_id_extractor import extract_video_id
from prefect import task

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


gen_prompt = """
You are an expert YouTube video summarizer. Here's is a guidline on how to summarize the video transcript.
Video Summary: "Title of the Video"

Introduction:
- Briefly introduce the topic of the video.
- Mention the speaker or presenter.

Main Points:

1. Point One
   - Explain the first major concept discussed in the video.
   - Provide relevant details and examples.

2. Point Two
   - Describe the second important topic covered.
   - Include any statistics, data, or case studies.

3. Point Three
   - Discuss the third significant aspect.
   - Highlight key takeaways or implications.

Conclusion:
- Recap the main points.
- End with a call to action or a thought-provoking statement.

Transcription: 
"""


keyword_extraction_prompt = """You are an experienced Youtube video keyword extractor. 
You will take in the transcript text, properly analyze the texts,
rank the keywords and extract the top 10 keywords.

Please provide the top 10 keywords from the text given here:  
"""

academic_prompts = """
You are an experienced YouTube academic video summarizer. 
Your method involves analyzing video transcripts to understand 
the main points of academic content. Here's your task:

Academic Video Summary: "Title of the Video"

Introduction:
- Briefly introduce the academic topic discussed in the video.
- Mention the presenter or speaker.

Main Sections:

1. **Conceptual Framework**
   - Explain the foundational concepts or theories covered.
   - Provide context for the academic discussion.

2. **Research Findings**
   - Summarize any empirical research or studies mentioned.
   - Highlight key results and implications.

3. **Critical Analysis**
   - Discuss any critiques or alternative viewpoints presented.
   - Evaluate the strengths and limitations of the content.

4. **Application and Practical Insights**
   - Explore how the academic content can be applied in real-world scenarios.
   - Provide actionable takeaways for viewers.

Conclusion:
- Recap the main academic points.
- Encourage further exploration or discussion.

Transcription: 
"""


######### Blog Content Prompts #########
blog_content_prompts = """
You are an experienced YouTube blog content creator. 
Your method involves analyzing video transcripts to understand the main points of the video. 
Here's your task:

1. **Blog Content Creation (YouTube Expertise):**
   - Imagine you're creating blog content based on a YouTube video. Your goal is to take in the transcript text, identify the key points, and craft 5 to 7 blog content points.
   - Consider recent trends and industry topics relevant to the video context.
   - For each blog point, provide an attractive title followed by a concise content snippet (50 to 100 words).
   - Enhance the content to make it interesting and engaging for readers.

Remember to create captivating titles and ensure the word count falls within the specified range. Happy blogging! 🎥📝

Please provide the blog content points from the text given here:


"""


######## Children Recommendation ########

children_prompt = """
You are an **Educator Advisor** skilled at understanding content suitable for children. 
Your role is to review video transcripts and assess their appropriateness for children aged **two to eight**.

Here's what you'll do:
1. Evaluate the content for anything related to **sexual**, **hurtful**, or **dangerous** material.
2. Provide a single response with two sections:
    a. Explain how suitable and beneficial the video is for children.
    b. Offer a detailed summary (if necessary) of the content (video).

**Transcript Text**:
"""

# getting the transcript from the youtube video
@task(log_prints=True, cache_result_in_memory=True, task_run_name="Extract Transcript", retry_delay_seconds=5, tags=["youtube", "transcript"])
def extract_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text = ""
        for i in transcript:
            transcript_text += i['text'] + " "

        return transcript_text
    except Exception as e:
        return "Error"

#getting the summary based on prompt and transcript
@task(log_prints=True, cache_result_in_memory=True, task_run_name="Generate General Summary", retry_delay_seconds=5, tags=["youtube", "summary"])
def generate_general_summary(transcript, prompt=gen_prompt):

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

@task(log_prints=True, cache_result_in_memory=True, task_run_name="Generate Keywords", retry_delay_seconds=5, tags=["youtube", "keywords"])
def generate_keywords(transcript, prompt=keyword_extraction_prompt):

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

@task(log_prints=True, cache_result_in_memory=True, task_run_name="Generate Academic Summary", retry_delay_seconds=5, tags=["youtube", "academic"])
def geneate_academic_summary(transcript, prompt=academic_prompts):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

@task(log_prints=True, cache_result_in_memory=True, task_run_name="Create Contents", retry_delay_seconds=5, tags=["youtube", "content"])
def create_contents (transcript, prompt=blog_content_prompts):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text

@task(log_prints=True, cache_result_in_memory=True, task_run_name="Children Recommendation", retry_delay_seconds=5, tags=["youtube", "children"])
def children_reccomendation (transcript, prompt=children_prompt):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt+transcript)
    return response.text