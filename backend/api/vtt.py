from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
from gtts import gTTS
import uuid, shutil, os, time
import re

from core import vtt
from core.qa import get_faq_answer

router = APIRouter(
    prefix="/vtt",
    tags=["Voice to Text"]
)

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        temp_path = Path(f"temp_{file.filename}")

        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = vtt.recognize_audio(temp_path)

        temp_path.unlink()  # Clean up the temporary file
        return {"text": text}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce:
        raise HTTPException(status_code=503, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# --- Cleanup function ---
def delete_file_after_delay(file_path: Path, delay: int = 45):
    time.sleep(delay)
    if file_path.exists():
        file_path.unlink()

def clean_markdown(md_text):

    # Remove code blocks (```...```)
    md_text = re.sub(r'```.*?```', '', md_text, flags=re.DOTALL)
    
    # Remove inline code (`...`)
    md_text = re.sub(r'`([^`]*)`', r'\1', md_text)

    # Remove images ![alt](url)
    md_text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)

    # Convert links [text](url) → text
    md_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', md_text)

    # Remove emphasis: bold and italic
    md_text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', md_text)  # bold
    md_text = re.sub(r'(\*|_)(.*?)\1', r'\2', md_text)     # italic

    # Remove headings (e.g. ### Heading)
    md_text = re.sub(r'^\s{0,3}#{1,6}\s+', '', md_text, flags=re.MULTILINE)

    # Remove blockquotes
    md_text = re.sub(r'^>\s+', '', md_text, flags=re.MULTILINE)

    # Remove horizontal rules (---, ***, ___)
    md_text = re.sub(r'^\s*([-*_]\s*?){3,}\s*$', '', md_text, flags=re.MULTILINE)

    # Remove unordered list markers (*, -, +)
    md_text = re.sub(r'^\s*[-*+]\s+', '', md_text, flags=re.MULTILINE)

    # Remove ordered list markers (1., 2., etc.)
    md_text = re.sub(r'^\s*\d+\.\s+', '', md_text, flags=re.MULTILINE)

    # Remove extra spaces and trim
    md_text = re.sub(r'\n{2,}', '\n\n', md_text)  # Collapse multiple newlines
    md_text = md_text.strip()

    return md_text


@router.post("/text-questions")
async def get_text_questions(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    try:
        # Generate unique filename
        unique_id = uuid.uuid4().hex
        temp_path = Path(f"temp_{unique_id}_{file.filename}")

        # Save uploaded file temporarily
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert to text
        text = vtt.recognize_audio(temp_path)
        temp_path.unlink()  # Delete uploaded audio after processing

        if not text:
            raise HTTPException(status_code=404, detail="Belum ada teks yang dikenali")

        # Get answer from semantic search
        answer = get_faq_answer(text)

        # Generate TTS audio

        cleaned_answer = clean_markdown(answer)
        tts = gTTS(cleaned_answer, lang="id")
        audio_filename = f"tts_{unique_id}.mp3"
        audio_path = Path(f"static/audio/{audio_filename}")
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        tts.save(str(audio_path))

        # Schedule cleanup in background
        background_tasks.add_task(delete_file_after_delay, audio_path)

        # Return result
        return JSONResponse(content={
            "text": answer,
            "audio_url": f"/static/audio/{audio_filename}"
        })

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce:
        raise HTTPException(status_code=503, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
