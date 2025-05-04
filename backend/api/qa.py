from fastapi import APIRouter
from pydantic import BaseModel
from core.qa import get_faq_answer

router = APIRouter(prefix="/faq", tags=["FAQ"])

class FAQRequest(BaseModel):
    query: str
    device_id : str

class FAQResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=FAQResponse)
async def ask_faq(request: FAQRequest):
    answer = get_faq_answer(request.query, request.device_id)
    return {"answer": answer}