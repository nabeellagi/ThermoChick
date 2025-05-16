import streamlit as st
import plotly.graph_objs as go
import numpy as np
import tempfile
import os
import base64
from xhtml2pdf import pisa
import plotly.io as pio
import requests

pio.kaleido.scope.default_format = "png"
st.set_page_config(page_title="Dasbor ThermoFarm", layout="wide")

# Inject Bulma CSS for better styling and mobile responsiveness
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
<style>
    body{
        background-color : ##FFF3F0;
    }       
    .bulma-container {
        padding: 1rem;
        margin: auto;
        max-width: 1000px;
    }
    .plotly-chart {
        width: 100% !important;
        overflow-x: auto;
    }
    .button.is-primary {
        background-color: #00d1b2;
        color: white;
        border: none;
        font-weight: bold;
        margin-top: 1rem;
    }
    .notification.is-success {
        background-color: #dff0d8;
        color: #3c763d;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .notification.is-danger {
        background-color: #f2dede;
        color: #a94442;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
<div class="bulma-container">
<h1 class="title is-3">🌡️ Data ThermoFarm</h1>
<h2 class="subtitle is-5">Pantau suhu & kelembapan kandang secara real-time dan unduh laporan dalam bentuk PDF</h2>
</div>
""", unsafe_allow_html=True)

# Fetch data
sensor_url = "http://localhost:8000/sensor/recent?device_id=test"
weather_url = "http://localhost:8000/weather?device_id=test"

sensor_data = requests.get(sensor_url).json()
weather_data = requests.get(weather_url).json()

timestamps = sensor_data["data"]["timestamps"]
temps = sensor_data["data"]["temperatures"]
humids = sensor_data["data"]["humidities"]

def add_stat_lines(fig, data, label_prefix):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    median = np.median(data)
    mean = np.mean(data)

    fig.add_trace(go.Scatter(x=timestamps, y=[q1]*len(timestamps), mode="lines",
                             name=f"{label_prefix} Q1", line=dict(dash='dot', color='green')))
    fig.add_trace(go.Scatter(x=timestamps, y=[median]*len(timestamps), mode="lines",
                             name=f"{label_prefix} Median", line=dict(dash='dash', color='blue')))
    fig.add_trace(go.Scatter(x=timestamps, y=[q3]*len(timestamps), mode="lines",
                             name=f"{label_prefix} Q3", line=dict(dash='dot', color='purple')))
    fig.add_trace(go.Scatter(x=timestamps, y=[mean]*len(timestamps), mode="lines",
                             name=f"{label_prefix} Mean", line=dict(dash='dashdot', color='red')))
    return fig

fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=timestamps, y=temps, mode="lines+markers",
                              name="Suhu Dalam (°C)", line=dict(color="firebrick")))
fig_temp = add_stat_lines(fig_temp, temps, "Suhu")
fig_temp.update_layout(title="🌡️ Suhu Kandang (Dalam)", xaxis_title="Waktu", yaxis_title="Suhu (°C)", template="plotly_white")

fig_humid = go.Figure()
fig_humid.add_trace(go.Scatter(x=timestamps, y=humids, mode="lines+markers",
                               name="Kelembapan Dalam (%)", line=dict(color="royalblue")))
fig_humid = add_stat_lines(fig_humid, humids, "Kelembapan")
fig_humid.update_layout(title="💧 Kelembapan Kandang", xaxis_title="Waktu", yaxis_title="Kelembapan (%)", template="plotly_white")

st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_humid, use_container_width=True)

def generate_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = os.path.join(tmpdir, "temp_chart.png")
        humid_path = os.path.join(tmpdir, "humid_chart.png")
        fig_temp.write_image(temp_path, width=800, height=400)
        fig_humid.write_image(humid_path, width=800, height=400)

        pdf_path = os.path.join(tmpdir, "dashboard.pdf")

        sensor_html = f"""
        <h2>📊 Data Sensor Terkini</h2>
        <ul>
            <li><strong>Data Terakhir:</strong> {timestamps[-1]}</li>
            <li><strong>Suhu Terakhir:</strong> {temps[-1]} °C</li>
            <li><strong>Kelembapan Terakhir:</strong> {humids[-1]}%</li>
            <li><strong>Rata-rata Suhu:</strong> {np.mean(temps):.2f} °C</li>
            <li><strong>Rata-rata Kelembapan:</strong> {np.mean(humids):.2f}%</li>
        </ul>
        """

        weather_html = f"""
        <h2>🌤️ Cuaca Sekitar Kandang</h2>
        <ul>
            <li><strong>Lokasi:</strong> {weather_data['name']}, {weather_data['region']}, {weather_data['country']}</li>
            <li><strong>Suhu Luar:</strong> {weather_data['outside_temp']} °C (Terasa: {weather_data['outside_feelslike']} °C)</li>
            <li><strong>Perbedaan Suhu:</strong> +{weather_data['difference']['amount']} °C — {weather_data['difference']['interpret']}</li>
            <li><strong>Tekanan Udara:</strong> {weather_data['pressure']['mb']} mb — {weather_data['pressure']['interpret']}</li>
            <li><strong>Kecepatan Angin:</strong> {weather_data['wind']} m/s</li>
            <li><strong>Kualitas Udara:</strong> {weather_data['gbdefra']['index']} — {weather_data['gbdefra']['interpret']['level']} ({weather_data['gbdefra']['interpret']['pesan']})</li>
            <li><strong>Kondisi Saat Ini:</strong> {weather_data['text']}</li>
        </ul>
        """

        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; font-size: 12px; }}
                h1, h2, h3 {{ color: #2C3E50; }}
                ul {{ padding-left: 20px; }}
                img {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>🌡️ Laporan ThermoFarm</h1>
            {sensor_html}
            {weather_html}
            <h3>📈 Grafik Suhu Dalam</h3>
            <img src="{temp_path}" width="600"/>
            <h3>💧 Grafik Kelembapan</h3>
            <img src="{humid_path}" width="600"/>
        </body>
        </html>
        """

        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
            if pisa_status.err:
                return None

        with open(pdf_path, "rb") as f:
            return f.read()

# Button area styled with Bulma
st.markdown("""<div class="bulma-container">""", unsafe_allow_html=True)

if st.button("📥 Buat Laporan PDF"):
    pdf_bytes = generate_pdf()
    if pdf_bytes:
        st.markdown('<div class="notification is-success">PDF berhasil dibuat. Silakan unduh menggunakan tombol di bawah ini.</div>', unsafe_allow_html=True)
        st.download_button(
            label="📄 Unduh PDF Sekarang",
            data=pdf_bytes,
            file_name="thermofarm_laporan.pdf",
            mime="application/pdf"
        )
    else:
        st.markdown('<div class="notification is-danger">Terjadi kesalahan saat membuat PDF.</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
