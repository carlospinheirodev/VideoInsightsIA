import re
from main import app
from flask import render_template, request
from video_analysis import videoExtraction
from video_analysis import ai_text_analysis
from video_analysis import analysis_with_n8n


def is_valid_youtube_url(url):
    youtube_url_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|shorts/)?([a-zA-Z0-9_-]+)"
    match = re.match(youtube_url_regex, url)
    return match is not None

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        input_type = request.form.get('input-type')
        use_n8n = request.form.get('use-n8n')
        analysis_complete = False
        complete_analysis = None

        print(use_n8n)
        if use_n8n == 'on':
            videoData = None
            if input_type == 'url':
                videoUrl = request.form.get('video-url')
                if not videoUrl or not is_valid_youtube_url(videoUrl):
                    return render_template('index.html', errorForm="URL inválida! Insira um link válido do YouTube.", analysis_complete=False)

                videoData = videoUrl
            else:
                transcription = request.form.get('video-transcription')
                if not transcription or transcription.strip() == "":
                    return render_template('index.html', errorForm="Por favor, insira uma transcrição válida.", analysis_complete=False)

                videoData = transcription

            complete_analysis = analysis_with_n8n(videoData, input_type)

        if input_type == 'url':
            videoUrl = request.form.get('video-url')
            if not videoUrl or not is_valid_youtube_url(videoUrl):
                return render_template('index.html', errorForm="URL inválida! Insira um link válido do YouTube.", analysis_complete=False)

            complete_analysis = videoExtraction(videoUrl)

        elif input_type == 'text':
            transcription = request.form.get('video-transcription')
            if not transcription or transcription.strip() == "":
                return render_template('index.html', errorForm="Por favor, insira uma transcrição válida.", analysis_complete=False)

            complete_analysis = ai_text_analysis(transcription)

        else:
            return render_template('index.html', errorForm="Opção inválida de entrada.", analysis_complete=False)

        return render_template('index.html', analysis_complete=True, analysis=complete_analysis)
    else:
        return render_template('index.html', analysis_complete=False)
