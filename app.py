import os
import uuid
from coqui_tts.TTS.utils.synthesizer import Synthesizer
from flask import Flask, request, send_file
from urllib.parse import unquote


OUTPUTS_DIR = 'tmp'

app = Flask(__name__)

# Initialize the output directory.
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Initialize the shared synthesizer.
synthesizer = Synthesizer(
    tts_checkpoint='./tts_model.pth.tar',
    tts_config_path='./tts_config.json',
    tts_speakers_file=None,
    vocoder_checkpoint='./vocoder_model.pth.tar',
    vocoder_config='./vocoder_config.json',
    encoder_checkpoint=None,
    encoder_config=None,
    use_cuda=False,
)


@app.route('/', methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    who = request.args.get('who', 'World')
    return f'Hello {who}!\n'


@app.route('/tts', methods=['GET'])
def tts():
    """Performs TTS on the given text."""
    # Synthesize the requested text.
    text = unquote(request.args.get('text', 'I am a big hotdog.'))
    wav = synthesizer.tts(text)
    tmp_filename = os.path.join(OUTPUTS_DIR, f'{uuid.uuid1().hex}.wav')
    synthesizer.save_wav(wav, tmp_filename)
    # Add these args to make it a downloadable attachment:
    # (as_attachment=True, attachment_filename='test.wav')
    result = send_file(tmp_filename, mimetype='audio/wav')
    # Cleanup.
    if os.path.exists(tmp_filename):
        os.remove(tmp_filename)
    return result


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
