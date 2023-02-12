from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Define a variable to hold you app
app = Flask(__name__)

'''
@app.route('/')
def index():
    return render_template('index.html')
'''

# Define your resource endpoints
@app.route("/summary")
def summary_api():
    url = request.args.get('url', '')
    # url = request.args.get('https://www.youtube.com/watch?v=8HslUzw35mc', '')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    # summary = get_summary(get_transcript('Yldkh0aOEcg'))
    return summary, 200
    # return render_template('test.html', summary=summary)


def get_transcript(video_id):
    # Returns a list of dictionaries
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

    # Dictionary format
    '''
        [
            {
                'text': 'Hey there',
                'start': 7.58,
                'duration': 6.13
            },
            {
                'text': 'how are you',
                'start': 14.08,
                'duration': 7.58
            },
            # ...
        ]
    '''

    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript


def get_summary(transcript):
    summarizer = pipeline('summarization')
    summary = ''
    for i in range(len(transcript)//1000+1):
        summary_text = summarizer(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary += summary_text+' '
        return summary

'''
    is T5 better?

    from transformers import T5ForConditionalGeneration, T5Tokenizer

    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")

'''


# Server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)