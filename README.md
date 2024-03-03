# YouTube Video Summarizer with Gemini Pro

![image](https://github.com/timothyafolami/Youtube_transcriber_summarizer/assets/109224656/13d18057-8e9b-4d0c-80bf-bd619a50ab70)

![image](https://github.com/timothyafolami/Youtube_transcriber_summarizer/assets/109224656/694706f3-b747-48a7-a37f-9c1e9149c0bd)


## Description
The YouTube Video Summarizer is an application that takes a YouTube video URL and generates a summary of the video content. It uses Google's Generative AI model to create summaries, extract keywords, and generate blog content points from a video transcript. The application is built with Streamlit, providing a simple and intuitive interface for users.

## Features
- Extracts transcripts from YouTube videos.
- Generates a general summary of the video.
- Extracts the top 10 keywords from the video.
- Generates a detailed, structured summary suitable for academic videos.
- Creates 5 to 7 blog content points from the video transcript.

## Installation
To install and run this project locally, you'll need to have Python installed on your machine. You'll also need to install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage
To use the application, follow these steps:

- Enter the URL of the YouTube video you want to summarize.
- Select your preference for the type of summary: ‘General’, ‘Academic’, or ‘Content Creation’.
- Click the ‘Get Detailed Summary’ button.

The application will then extract the transcript from the YouTube video, generate keywords, and create a summary based on your preference. The summary will be displayed on the page.

## Code Overview
The application uses several custom functions to extract transcripts from YouTube videos, generate keywords, and create summaries. These functions are imported from the summarizer and youtube_id_extractor modules at the beginning of the script.

The extract_video_id function is used to extract the unique ID of a YouTube video from its URL. This is done using a regular expression that matches the patterns of YouTube video URLs. The function returns the ID as a string if it finds a match, or None if it doesn’t.

The extract_transcript function uses the YouTubeTranscriptApi to get the transcript from a YouTube video. The transcript is then passed to one of four functions, depending on the user’s preference.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Contact
For any questions or collaborations, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/timothy-afolami).
