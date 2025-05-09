import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
from google import genai
from google.genai import types
from core.sensor import get_latest_data
from core.userdata import get_latest_temperature
from core.weather import get_weather_data

df = pd.read_csv("data/faq.csv")

faq_data = df.to_dict(orient="records")

model = SentenceTransformer('all-MiniLM-L6-v2')
faq_questions = [item["question"] for item in faq_data]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def generate_gemini_response(input_text: str) -> str:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    model = "gemini-2.0-flash-lite"
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


def get_faq_answer(user_input: str, device_id: str) -> str:
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    cos_scores = util.cos_sim(input_embedding, faq_embeddings)
    best_match_idx = cos_scores.argmax().item()
    best_score = cos_scores[0][best_match_idx].item()

    if best_score > 0.5:
        try:
            latest_data = get_latest_data(device_id)
            temperature = latest_data["temperature"]
            humidity = latest_data["humidity"]

            threshold = get_latest_temperature(device_id)
            temp_threshold = threshold["temperature"]

            outside = get_weather_data(device_id)
            outside_temp = outside["outside_temp"]
            difference = outside["difference"]["interpret"]            

        except Exception as e:
            temperature, humidity = None, None, None

        # Create context block
        context = f"""
temperatur kandang = {temperature},
kelembapan kandang = {humidity},
lampu akan menyala saat = {temp_threshold},
suhu diluar kandang = {outside_temp},
perbedaan = {difference}

        """

        prompt = f"""
Kamu adalah seorang asisten peternak pintar bernama Farma. Kamu adalah seorang asisten dari aplikasi Thermochick, sebuah aplikasi pintar monitoring kandang.
Berikut adalah data yang diberikan, gunakan disaat relevan saja, jika tidak maka abaikan :
{context}

Pengguna bertanya : "{user_input}"

Jawaban awal kamu/Farma : "{faq_data[best_match_idx]["answer"]}"

Tugas kamu sebagai seorang asisten adalah untuk melakukan elaborasi yang menjelaskan jawaban awal, sehingga pengguna dapat mengerti. Lalu susun dalam bentuk markdown.
"""

        out = generate_gemini_response(prompt)
        return out
    else:
        return "Maaf, jawaban belum tersedia untuk pertanyaan tersebut."