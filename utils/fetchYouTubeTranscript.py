from youtube_transcript_api import YouTubeTranscriptApi
from utils.youtube_id_extracter import extract_youtube_id

ytt_api = YouTubeTranscriptApi()

def getYoutubeTranscript(url):
    try:
        videoId = extract_youtube_id(url)
        # Fetched Youtube Transcripts List from Video Id
        dataList = ytt_api.fetch(videoId,languages=['en','hi'])
        return dataList,videoId
    except Exception as e:
        print(f"Erorr : {e}")