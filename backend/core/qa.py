import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
from google import genai
from google.genai import types

df = pd.read_csv("data/faq.csv")

faq_data = df.to_dict(orient="records")

model = SentenceTransformer('all-MiniLM-L6-v2')
faq_questions = [item["question"] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def generate_gemini_response(input_text: str) -> str:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=input_text)],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(temperature=0.8, response_mime_type="text/plain")
    
    # Collect the result in a string
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text


def get_faq_answer(user_input: str) -> str:
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    cos_scores = util.cos_sim(input_embedding, faq_embeddings)
    best_match_idx = cos_scores.argmax().item()
    best_score = cos_scores[0][best_match_idx].item()


    if best_score > 0.5:
        prompt = f"""
Kamu adalah seorang asisten muda untuk seorang peternak ayam di Indonesia. Tugas kamu adalah untuk membantu peternak tersebut dengan menjawab seluruh pertanyaan yang ada.
Kamu akan diberikan jawaban, namun ini terlalu singkat. Sehingga tugas kamu adalah untuk memberikan analisis dan eksplanasi mengenai jawaban tersebut dengan bahasa yang mudah dipahami.
Tetapi jangan buat terlalu panjang sehingga sulit dimengerti, ringkas saja ke dalam beberapa poin.

Pertanyaan : {user_input}
Jawaban awal : {faq_data[best_match_idx]["answer"]}

Jawab dengan format markdown yang rapi dan baik.
"""
        out = generate_gemini_response(prompt)
        return out
    else:
        return "Maaf jawaban belum tersedia."