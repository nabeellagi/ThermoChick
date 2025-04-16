import streamlit as st

import requests

# BACKEND URL
st.set_page_config(page_title="IoT+AI Prototype", layout="centered")

st.title("🌡️ AI-Powered Poultry Monitor")
st.write("Prototype to test temperature/humidity forecasting and FAQ system")

st.sidebar.header("🔧 Configuration")
FASTAPI_URL = st.sidebar.text_input("Enter your FastAPI backend URL:", value="http://localhost:8000")


# Tabs for separation
tab1, tab2, tab3, tab4 = st.tabs(["Intro dulu", "📈 Get Current Sensor Data", "📈 Forecast", "❓ RAG Sentence Transformer + Gemini"])

with tab1:
    st.header("👋 Selamat Datang di Halaman Uji Coba")

    st.markdown("""
    ### 📱 Tentang Aplikasi Ini

    Halaman ini merupakan **prototipe** berbasis **Streamlit** yang digunakan untuk **mengujicoba API** dari sistem monitoring suhu dan kelembapan pada kandang ayam.

    Tujuan utama dari halaman ini adalah untuk:
    - Menguji dan memastikan API berjalan dengan baik.
    - Melihat hasil prediksi suhu dan kelembapan secara langsung.
    - Menguji sistem FAQ cerdas berbasis AI yang dikembangkan untuk peternak ayam.

    ### 🐥 Tentang Produk Sebenarnya

    Aplikasi asli bernama **Thermochick** telah dikembangkan menggunakan **React Native** untuk platform mobile (Android/iOS). Fitur utama dari Thermochick meliputi:
    - **Monitoring suhu dan kelembapan secara real-time** dari sensor IoT.
    - **Prediksi kondisi lingkungan** beberapa detik ke depan menggunakan AI.
    - **Pusat bantuan berbasis AI** untuk menjawab pertanyaan peternak secara cerdas.

    ### 🔧 Kenapa Ada Halaman Ini?

    - Untuk **menguji API secara independen** sebelum diintegrasikan penuh dengan aplikasi React Native.
    - Untuk **debugging dan visualisasi cepat**.

    ---
    SILAHKAN MULAI DENGAN INPUT URL SERVER    
    Silakan lanjut ke tab berikutnya untuk mencoba fungsi-fungsi utamanya! ⏩
    """)


with tab2:
    # Penjelasan cara kerja aplikasi
    st.subheader("📊 Cara Kerja Aplikasi")

    st.markdown("""
    1. **Menggunakan Metode GET ke API**  
       Saat tombol **"Get Current Sensor Data"** ditekan, aplikasi ini akan mengirim permintaan **GET** ke API menggunakan alamat yang sudah dikonfigurasi. Kode untuk API ini bisa ditemukan di repositori GitHub.

    2. **API Mengambil Data Terbaru dari CSV**  
       API yang dibuat dengan **FastAPI** akan membaca data terbaru dari file **CSV** menggunakan **Pandas**. Data yang diambil adalah baris paling akhir, yang mencerminkan pembacaan sensor terkini.

    3. **API Mengembalikan dan Mengirimkan Data ke Aplikasi**  
       Setelah mendapatkan data, API mengirimkan data tersebut dalam format **JSON**, yang lalu ditampilkan di Streamlit sebagai:
       - Suhu dalam derajat Celsius (°C)
       - Kelembaban dalam persen (%)

    4. **Perangkat IoT Mengirim Data Setiap Detik**  
       Sementara itu, perangkat IoT (melalui file `sketch.ino`) secara otomatis mengirimkan data sensor setiap **detik** ke server menggunakan **MQTT**, dan data ini juga dicatat dalam file CSV.

    ---  
    """)

    if st.button("Get Current Sensor Data"):
        try:
            response = requests.get(f"{FASTAPI_URL}/sensor")
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    data = result["data"]
                    st.success("Sensor data retrieved")
                    st.metric("Current Temperature (°C)", f"{data['temperature']:.2f}")
                    st.metric("Current Humidity (%)", f"{data['humidity']:.2f}")
                else:
                    st.error("Could not fetch sensor data.")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")


with tab3:
    st.header("Predict Future Temperature & Humidity")

    st.subheader("📊 Cara Kerja Aplikasi")

    st.markdown("""
    ### Proses Prediksi Suhu dan Kelembapan

    Aplikasi ini dapat memprediksi suhu dan kelembapan untuk waktu yang akan datang berdasarkan data yang sudah ada. Berikut adalah tahapan yang terjadi di **API** untuk melakukan prediksi:

    1. **Menggunakan Data CSV Terbaru** \n
       API akan membaca data terbaru yang tersimpan dalam file **CSV** yang berisi informasi suhu dan kelembapan dari perangkat IoT. Data ini diperbarui setiap detik oleh perangkat.

    2. **Persiapan dan Pelatihan Model**\n
       Setelah data diambil, aplikasi menggunakan model **Polynomial Regression** untuk mempelajari hubungan antara waktu dan suhu serta kelembapan. Model ini dilatih menggunakan data yang ada untuk memprediksi nilai lanjutan berdasarkan pola yang ditemukan.

    3. **Prediksi Suhu dan Kelembapan di Masa Depan**\n
       Dengan menggunakan input waktu yang dipilih oleh pengguna (berapa detik ke depan), model akan memprediksi suhu dan kelembapan yang diharapkan pada waktu tersebut. Hasil prediksi ini kemudian di-return API dan ditampilkan di aplikasi.

    4. **Pengembalian dan Tampilan Hasil Prediksi**\n
       Setelah prediksi dilakukan, API mengembalikan hasil prediksi berupa suhu dan kelembapan yang diperkirakan untuk waktu yang dipilih.

    ---  
    """)

    seconds = st.slider("Seconds Ahead", min_value=1, max_value=59, step=10, value=10)

    if st.button("Get Prediction"):
        try:
            response = requests.get(f"{FASTAPI_URL}/predict", params={"seconds_ahead": seconds})
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    st.success("Prediction Retrieved")
                    temp = result["data"]["temperature"]
                    humid = result["data"]["humidity"]
                    st.metric("Predicted Temperature (°C)", f"{temp:.2f}")
                    st.metric("Predicted Humidity (%)", f"{humid:.2f}")

                    # 🎯 Display plot after prediction
                    st.subheader("📈 Grafik Prediksi vs Data Aktual")
                    plot_response = requests.get(f"{FASTAPI_URL}/plot")
                    if plot_response.status_code == 200:
                        st.image(plot_response.content, caption="Prediksi vs Data Aktual", use_column_width=True)
                    else:
                        st.error(f"Gagal memuat plot: {plot_response.status_code}")
                else:
                    st.error(f"Error: {result['message']}")
            else:
                st.error(f"Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")


with tab4:
    st.header("Ask a Frequently Asked Question")

    st.subheader("📊 Cara Kerja Aplikasi")

    st.markdown("""
    ### 🧠 1. **Mencari Pertanyaan yang Mirip (Similarity Matching)**

    - Semua pertanyaan di file `faq.csv` diubah menjadi **representasi angka (embedding)** menggunakan model bernama `all-MiniLM-L6-v2` dari **SentenceTransformer**.
    - Ketika user mengetik pertanyaan baru, pertanyaan tersebut juga diubah jadi embedding.
    - Lalu sistem membandingkan pertanyaan user dengan semua pertanyaan di database, dan mencari yang **paling mirip (similar)** menggunakan **cosine similarity**.
    - Kalau **tingkat kemiripannya di atas 0.5**, maka dianggap cocok.

    ---

    ### 🤖 2. **Menjawab dengan Bantuan Gemini (LLM dari Google)**

    - Setelah menemukan pertanyaan yang mirip, sistem mengambil jawaban singkat dari file CSV.
    - Tapi karena jawaban itu terlalu pendek, sistem mengirim **permintaan (prompt)** ke **Gemini API** untuk membuat penjelasan yang **lebih jelas dan mudah dipahami**, khususnya untuk peternak ayam.
    - API Gemini akan mengembalikan jawaban yang **lebih terstruktur, ringkas, dan mudah dicerna** dalam format markdown.

    ---

    """)

    query = st.text_input("Enter your question:")
    if st.button("Ask FAQ"):
        if query.strip():
            try:
                res = requests.post(f"{FASTAPI_URL}/faq/ask", json={"query": query})
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.success("Answer retrieved")
                    st.write(f"💬 **Answer**: {answer}")
                else:
                    st.error(f"Backend returned error: {res.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a question")

