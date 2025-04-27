import speech_recognition as sr
from pathlib import Path
from pydub import AudioSegment
import tempfile

recognizer = sr.Recognizer()

def recognize_audio(file_path: Path) -> str:
    if file_path.suffix.lower() != '.wav':

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            audio = AudioSegment.from_file(file_path)
            audio.export(tmp_wav.name, format="wav")
            file_path_to_use = Path(tmp_wav.name)
    else:
        file_path_to_use = file_path

    try:
        with sr.AudioFile(str(file_path_to_use)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="id-ID")
        return text
    except sr.UnknownValueError:
        raise ValueError("Tidak dapat memahami audio.")
    except sr.RequestError as e:
        raise ConnectionError(f"Error dalam permintaan ke Google API; {e}")
    finally:
        # Clean up temporary file if conversion was made
        if file_path_to_use != file_path and file_path_to_use.exists():
            file_path_to_use.unlink()
