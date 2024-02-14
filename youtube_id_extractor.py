import re

def extract_video_id(url):
    # Regular expression to match a YouTube video ID
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)([^"&?\/ ]{11})'
    match = re.match(regex, url)
    if match:
        return match.group(1)
    return None

# Test the function
# print(extract_video_id("https://www.youtube.com/watch?v=z5rpft6xZwk"))  # Outputs: z5rpft6xZwk
# print(extract_video_id("https://youtu.be/z5rpft6xZwk?si=Ui-CeJ6cGbDuZxa_"))  # Outputs: z5rpft6xZwk
# print(extract_video_id("https://youtube.com/shorts/8QyR_nhprJM?si=ac4cakald6R66krW"))  # Outputs: 8QyR_nhprJM
# print(extract_video_id("https://youtube.com/shorts/8QyR_nhprJM?si=ac4cakald6R66krW"))  # Outputs: 12345678901
