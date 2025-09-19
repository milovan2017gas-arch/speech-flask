from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Archivo de audio no recibido'}), 400

    audio_file = request.files['file']

    try:
        # Crear archivo temporal WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav:
            # Convertir a WAV usando pydub
            audio = AudioSegment.from_file(audio_file)
            audio.export(temp_wav.name, format="wav")

            # Reconocimiento de voz
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav.name) as source:
                audio_data = recognizer.record(source)

                try:
                    text = recognizer.recognize_google(audio_data, language="es-ES")
                    return jsonify({'text': text})
                except sr.UnknownValueError:
                    return jsonify({'error': 'No se pudo entender el audio'}), 400
                except sr.RequestError:
                    return jsonify({'error': 'Error al contactar el servicio de Google'}), 500

    except Exception as e:
        return jsonify({'error': f'Error procesando audio: {str(e)}'}), 500

# Iniciar la app en el puerto que Render asigna (por variable de entorno)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
