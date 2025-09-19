import tempfile

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Missing file'}), 400

    audio_file = request.files['file']

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav:
        audio = AudioSegment.from_file(audio_file)
        audio.export(temp_wav.name, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav.name) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="es-ES")
                return jsonify({'text': text})
            except sr.UnknownValueError:
                return jsonify({'error': 'No se pudo entender el audio'}), 400
            except sr.RequestError:
                return jsonify({'error': 'Error al contactar el servicio de reconocimiento'}), 500

