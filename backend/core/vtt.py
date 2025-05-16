import speech_recognition as sr
from pathlib import Path
from pydub import AudioSegment
from io import BytesIO

recognizer = sr.Recognizer()

def recognize_audio(file_path: Path) -> str:
    try:
        if file_path.suffix.lower() != '.wav':
            # Convert to wav in-memory
            audio = AudioSegment.from_file(file_path)
            wav_io = BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)
            audio_file = sr.AudioFile(wav_io)
        else:
            audio_file = sr.AudioFile(str(file_path))

        with audio_file as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="id-ID")
        return text

    except sr.UnknownValueError:
        raise ValueError("Tidak dapat memahami audio.")
    except sr.RequestError as e:
        raise ConnectionError(f"Error dalam permintaan ke Google API; {e}")
