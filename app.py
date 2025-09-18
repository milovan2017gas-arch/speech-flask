from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Missing file'}), 400

    audio_file = request.files['file']
    audio = AudioSegment.from_file(audio_file)
    audio.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'No se pudo entender el audio'}), 400
        except sr.RequestError:
            return jsonify({'error': 'Error al contactar el servicio de reconocimiento'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
