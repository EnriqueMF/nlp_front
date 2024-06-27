from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

app = Flask(__name__)

# Variable global para almacenar los subtítulos
transcript_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_subtitles', methods=['POST'])
def get_subtitles():
    global transcript_data
    video_id = request.json['video_id']
    language = request.json.get('language', 'es')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    except NoTranscriptFound as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404
    transcript_data = transcript
    return jsonify({'status': 'success'})

@app.route('/get_subtitle_segment', methods=['POST'])
def get_subtitle_segment():
    global transcript_data
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    segment = [entry for entry in transcript_data if entry['start'] >= start_time and entry['start'] < end_time]
    return jsonify(segment)
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
