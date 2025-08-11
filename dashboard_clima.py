#f032ac87f9eb3ca429b3f849a598f9bb apirest para poder testear 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests

# Función para obtener datos del clima desde OpenWeatherMap API
def get_weather_data(city, api_key, days=5):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("No se pudo obtener la información del clima.")
        return []

    data = response.json()
    forecast_list = data['list']

    weather_data = []
    for entry in forecast_list:
        date = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        weather_data.append({'date': date, 'temperature': temp, 'humidity': humidity})

    return weather_data

# Interfaz de usuario con Streamlit
st.title("🌤️ Dashboard de Clima Interactivo")
st.write("Consulta el pronóstico del clima para los próximos días.")

# Entrada del usuario
city = st.text_input("Ingrese el nombre de la ciudad:", "Buenos Aires")
api_key = st.text_input("Ingrese su API Key de OpenWeatherMap:", type="password")

# Selección de rango de fechas
start_date = st.date_input("Fecha de inicio:", datetime.today())
end_date = st.date_input("Fecha de fin:", datetime.today() + timedelta(days=4))

# Botón para consultar
if st.button("Consultar clima"):
    if not api_key:
        st.warning("Por favor, ingrese su API Key.")
    else:
        data = get_weather_data(city, api_key)
        if data:
            df = pd.DataFrame(data)
            df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]

            st.subheader("📊 Datos del clima")
            st.dataframe(df)

            # Gráfico de temperatura
            st.subheader("🌡️ Temperatura")
            fig, ax = plt.subplots()
            ax.plot(df['date'], df['temperature'], marker='o', color='orange')
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Temperatura (°C)")
            ax.set_title(f"Temperatura en {city}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Gráfico de humedad
            st.subheader("💧 Humedad")
            fig2, ax2 = plt.subplots()
            ax2.plot(df['date'], df['humidity'], marker='s', color='blue')
            ax2.set_xlabel("Fecha")
            ax2.set_ylabel("Humedad (%)")
            ax2.set_title(f"Humedad en {city}")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            