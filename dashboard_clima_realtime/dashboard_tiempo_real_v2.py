import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuración de la página
st.set_page_config(page_title="Dashboard en Tiempo Real", layout="wide")

st.title("📊 Dashboard Interactivo en Tiempo Real")
st.write("Este dashboard simula datos en tiempo real con filtros y gráficos actualizados dinámicamente.")

# --- Inicializar historial en session_state ---
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Tiempo", "Valor", "Categoría"])

# --- Función para generar un nuevo lote de datos ---
def generar_datos(n=5):
    tiempo = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="s")  # segundos en minúscula
    valor = np.random.normal(loc=50, scale=10, size=n).cumsum() + (st.session_state.historial["Valor"].iloc[-1] if not st.session_state.historial.empty else 0)
    categoria = np.random.choice(["A", "B", "C"], size=n)
    df = pd.DataFrame({"Tiempo": tiempo, "Valor": valor, "Categoría": categoria})
    return df

# --- Filtros interactivos ---
st.sidebar.header("🎛️ Filtros")
categoria_seleccionada = st.sidebar.multiselect("Seleccionar categoría", ["A", "B", "C"], default=["A", "B", "C"])
mostrar_tabla = st.sidebar.checkbox("Mostrar tabla de datos", value=True)
actualizar = st.sidebar.checkbox("Actualizar automáticamente", value=False)
intervalo = st.sidebar.number_input("Intervalo de actualización (segundos)", min_value=1, max_value=10, value=2)
max_puntos = st.sidebar.number_input("Máximo de puntos en historial", min_value=50, max_value=1000, value=200)

# --- Actualizar historial ---
nuevos_datos = generar_datos()
st.session_state.historial = pd.concat([st.session_state.historial, nuevos_datos]).tail(max_puntos)

# --- Aplicar filtros ---
df_filtrado = st.session_state.historial[st.session_state.historial["Categoría"].isin(categoria_seleccionada)]

# --- Layout principal ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Gráfico de línea")
    fig, ax = plt.subplots()
    for cat in categoria_seleccionada:
        datos_cat = df_filtrado[df_filtrado["Categoría"] == cat]
        ax.plot(datos_cat["Tiempo"], datos_cat["Valor"], label=f"Categoría {cat}")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Valor")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("📊 Gráfico de barras por categoría")
    promedio_por_categoria = df_filtrado.groupby("Categoría")["Valor"].mean()
    st.bar_chart(promedio_por_categoria)

if mostrar_tabla:
    st.subheader("🧾 Tabla de datos filtrados")
    st.dataframe(df_filtrado)

# --- Actualización automática ---
if actualizar:
    time.sleep(intervalo)
    st.experimental_rerun()