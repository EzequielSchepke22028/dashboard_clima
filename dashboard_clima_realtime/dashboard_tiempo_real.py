import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Dashboard en Tiempo Real", layout="wide")

st.title("📊 Dashboard Interactivo en Tiempo Real")
st.write("Este dashboard simula datos en tiempo real con filtros y gráficos actualizados dinámicamente.")

# Simulación de datos en tiempo real
def generar_datos(n=100):
    tiempo = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="S")
    valor = np.random.normal(loc=50, scale=10, size=n).cumsum()
    categoria = np.random.choice(["A", "B", "C"], size=n)
    df = pd.DataFrame({"Tiempo": tiempo, "Valor": valor, "Categoría": categoria})
    return df

# Filtros interactivos
st.sidebar.header("🎛️ Filtros")
categoria_seleccionada = st.sidebar.multiselect("Seleccionar categoría", ["A", "B", "C"], default=["A", "B", "C"])
mostrar_tabla = st.sidebar.checkbox("Mostrar tabla de datos", value=True)
actualizar = st.sidebar.checkbox("Actualizar automáticamente", value=False)

# Área principal
placeholder = st.empty()

# Loop de actualización en tiempo real
while True:
    df = generar_datos()

    # Aplicar filtros
    df_filtrado = df[df["Categoría"].isin(categoria_seleccionada)]

    with placeholder.container():
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

    if not actualizar:
        break
    time.sleep(2)