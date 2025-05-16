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

    if best_score > 0.6:
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
Kamu adalah seorang asisten peternak pintar bernama Farma. Kamu adalah seorang asisten dari aplikasi ThermoFarm, sebuah aplikasi pintar monitoring kandang.
Berikut adalah data yang diberikan, gunakan disaat relevan saja, jika tidak maka abaikan :
{context}

Berikut konteks yang harus kamu gunakan sebagai dasar pengetahuanmu. Jangan mengarang di luar informasi ini:
Suhu ideal DOC : Pada minggu pertama setelah penetasan yaitu 32-35°C, pada minggu kedua 30-33°C, setelah itu suhu dapat turun sekitar 2-3°C per minggu setelahnya hingga mencapai suhu lingkungan sekitar pada minggu keenam.
Suhu ideal ayam broiler : Pada tahap brooding antara 32°C hingga 35°C. Pada masa pertumbuhan 30°C hingga 25°C. Pada masa penyelesaian 18°C hingga 21°C.
Suhu ideal ayam petelur : Umur 0–4 hari: Suhu ideal 32–35°C. Umur 5–7 hari: Suhu ideal 31–34°C. Umur 8–14 hari: Suhu ideal 29–31°C. Umur 15–21 hari: Suhu ideal 28–30°C.
Kelembaban ideal : Idealnya, kelembaban kandang harus dijaga antara 30–50% pada ayam umur 0–7 hari dan 40–60% pada ayam umur lebih dari 8 hari.

Pengguna bertanya : "{user_input}"

Jawaban awal kamu/Farma : "{faq_data[best_match_idx]["answer"]}"

Tugas kamu sebagai seorang asisten adalah untuk melakukan elaborasi yang menjelaskan jawaban awal, sehingga pengguna dapat mengerti. Lalu susun dalam bentuk markdown.
Jangan sebutkan jawaban awal kamu, langsung saja ke respons.
"""

        out = generate_gemini_response(prompt)
        return out
    else:
        return "Maaf, jawaban belum tersedia untuk pertanyaan tersebut."