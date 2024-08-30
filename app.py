from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def get_youtube_transcript(video_url):
    try:
        # Extract video ID
        video_id = re.search(r"watch\?v=([^\&]+)", video_url).group(1)
        
        # Get transcripts
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Extract text from transcripts without timestamps
        captions = ""
        for entry in transcripts:
            captions += entry['text'] + '\n\n'
        
        return captions
    except Exception as e:
        return f"Error for {video_url}: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_transcripts', methods=['POST'])
def fetch_transcripts():
    data = request.get_json()
    video_urls = data.get('urls')
    if not video_urls:
        return jsonify({'error': 'URLs are required'}), 400

    transcripts = {}
    for video_url in video_urls:
        captions = get_youtube_transcript(video_url)
        transcripts[video_url] = captions
    
    return jsonify(transcripts)

if __name__ == '__main__':
    app.run(debug=True)
