from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
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


@router.post("/text-questions")
async def get_text_questions(file: UploadFile = File(...)):
    try:
        temp_path = Path(f"temp_{file.filename}")

        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = vtt.recognize_audio(temp_path)

        temp_path.unlink()  
        if not text:
            raise HTTPException(status_code=404, detail="Belum ada teks yang dikenali")

        answer = get_faq_answer(text)
        return {"text": answer}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce:
        raise HTTPException(status_code=503, detail=str(ce))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
