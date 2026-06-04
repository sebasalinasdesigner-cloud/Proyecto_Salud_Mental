import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Salud Mental y Redes Sociales",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para mejorar el diseño
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        color: #4f46e5;
    }
    .metric-label {
        font-size: 1rem;
        color: #6b7280;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Intentar cargar el modelo entrenado
try:
    model = joblib.load('modelo_adiccion.pkl')
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Error al cargar el modelo `modelo_adiccion.pkl`: {e}. Por favor, asegúrate de que el cuaderno `03_Regresion_Lineal.ipynb` se ha ejecutado y generado el archivo.")

# Panel lateral con información del proyecto
with st.sidebar:
    st.image("https://img.icons8.com/illustrations/external-linear-bicolor-kliwir-art/100/external-mental-health-medical-care-linear-bicolor-kliwir-art.png", width=100)
    st.title("Proyecto Salud Mental")
    st.markdown("""
    Este predictor utiliza un modelo de **Regresión Lineal** entrenado bajo la metodología **CRISP-ML** con un dataset sobre hábitos de estudiantes en redes sociales.
    
    ### Fases CRISP-ML:
    1. **01_ETL.ipynb**: Limpieza y preprocesamiento de datos.
    2. **02_EDA.ipynb**: Análisis exploratorio y visualizaciones.
    3. **03_Regresion_Lineal.ipynb**: Entrenamiento del modelo.
    """)
    st.info("Desarrollado para el proyecto de Inteligencia Artificial de Talento Tech.")

# Contenido principal
st.title("🧠 Predictor de Adicción a Redes Sociales")
st.write("Introduce los datos del estudiante en el panel inferior para estimar su puntaje de adicción en una escala de 1 a 10.")

if model_loaded:
    col1, col2 = st.columns([2, 1.2])

    with col1:
        st.subheader("📋 Datos del Estudiante")
        
        # Agrupar las entradas de forma visual en columnas
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            age = st.slider("Edad (Años)", min_value=12, max_value=30, value=19, step=1)
            usage_hours = st.slider("Uso Diario Promedio de Redes Sociales (Horas)", min_value=0.0, max_value=16.0, value=5.0, step=0.5)
            sleep_hours = st.slider("Horas de Sueño por Noche", min_value=3.0, max_value=12.0, value=7.0, step=0.5)
        
        with subcol2:
            mental_health = st.slider("Puntaje de Salud Mental (1 = Crítico, 10 = Excelente)", min_value=1, max_value=10, value=6, step=1)
            conflicts = st.slider("Frecuencia de Conflictos por Redes Sociales (0 = Ninguno, 5 = Muy frecuente)", min_value=0, max_value=5, value=2, step=1)

    with col2:
        st.subheader("🎯 Resultado de la Predicción")
        
        # Preparar inputs para el modelo
        input_data = pd.DataFrame([[age, usage_hours, sleep_hours, mental_health, conflicts]], 
                                  columns=['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score', 'Conflicts_Over_Social_Media'])
        
        # Realizar predicción
        prediction = model.predict(input_data)[0]
        # Limitar la predicción a los rangos de la escala del dataset (1 a 10)
        prediction_clipped = np.clip(prediction, 1.0, 10.0)
        
        # Determinar el nivel de riesgo y el color del mensaje
        if prediction_clipped < 4.0:
            level = "Bajo Riesgo de Adicción"
            color_theme = "success"
            emoji = "🟢"
            message = "El estudiante presenta un uso saludable y controlado de las plataformas de redes sociales."
        elif prediction_clipped < 7.0:
            level = "Riesgo Moderado"
            color_theme = "warning"
            emoji = "🟡"
            message = "Se aconseja prestar atención al tiempo de uso y fomentar desconexiones digitales periódicas."
        else:
            level = "Alto Riesgo de Adicción"
            color_theme = "danger"
            emoji = "🔴"
            message = "Es altamente recomendable reducir el tiempo en pantalla y buscar hábitos de sueño y ocio más saludables."

        # Mostrar métrica y alerta dinámica
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{prediction_clipped:.2f} / 10.0</div>
                <div class="metric-label">Puntaje Estimado de Adicción</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        if color_theme == "success":
            st.success(f"{emoji} **{level}**\n\n{message}")
        elif color_theme == "warning":
            st.warning(f"{emoji} **{level}**\n\n{message}")
        else:
            st.error(f"{emoji} **{level}**\n\n{message}")

else:
    st.warning("⚠️ Carga el modelo de Inteligencia Artificial para habilitar el predictor interactivo.")
