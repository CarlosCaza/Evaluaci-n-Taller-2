import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Monitor de Salud Pública", page_icon="🏥", layout="wide")

st.title("🏥 Dashboard: Monitor de Noticias de Salud (BBC & WHO)")
st.markdown("Sistema de recopilación de noticias de salud mediante RSS para el apoyo en la detección de desinformación.")

# ==========================================
# 2. CARGA DE DATOS (Conectado a la Fase 2/3)
# ==========================================
@st.cache_data
def cargar_datos():
    # Buscamos el nombre genérico que usarían para BBC y WHO
    archivo_csv = "datos_salud.csv" 
    try:
        return pd.read_csv(archivo_csv)
    except FileNotFoundError:
        # Si el profesor no corrió el scraper, mostramos un mensaje, pero cargamos datos de prueba
        # para que la interfaz NO se rompa durante la exposición y puedan ver tu trabajo.
        st.warning(f"⚠️ No se encontró '{archivo_csv}'. Mostrando datos de demostración.")
        datos_demo = {
            "Fecha": ["2026-06-25", "2026-06-25", "2026-06-24"],
            "Fuente": ["BBC Health", "WHO News", "BBC Health"],
            "Título": ["New guidelines on global nutrition", "COVID-19 update and variants", "Understanding cardiovascular health"],
            "URL": ["https://bbc.co.uk/health/1", "https://who.int/news/1", "https://bbc.co.uk/health/2"]
        }
        return pd.DataFrame(datos_demo)

df = cargar_datos()

# ==========================================
# 3. ESTRUCTURA DE PESTAÑAS (Para cumplir la Rúbrica Fase 4)
# ==========================================
# Dividimos la interfaz para responder a las preguntas de evaluación
tab1, tab2, tab3 = st.tabs(["📊 Resultados de Extracción", "📈 Métricas de Impacto", "⚖️ Ética y Limitaciones"])

# --- PESTAÑA 1: LA INTERFAZ DE RESULTADOS (Tu código original mejorado) ---
with tab1:
    st.header("Explorador de Noticias Extraídas")
    
    if not df.empty:
        # Métricas rápidas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Noticias Recopiladas", len(df))
        with col2:
            st.metric("Fuentes Activas", df['Fuente'].nunique())

        # Filtros
        st.subheader("Filtra la información")
        fuente_seleccionada = st.selectbox("Selecciona una fuente:", ["Todas"] + list(df['Fuente'].unique()))

        if fuente_seleccionada != "Todas":
            df_filtrado = df[df['Fuente'] == fuente_seleccionada]
        else:
            df_filtrado = df

        # Tabla visual
        st.dataframe(df_filtrado[['Fecha', 'Fuente', 'Título', 'URL']], use_container_width=True)

        # Lector
        st.subheader("📖 Visor de Registro")
        titulo_seleccionado = st.selectbox("Selecciona un artículo para ver los detalles:", df_filtrado['Título'])
        if titulo_seleccionado:
            registro = df_filtrado[df_filtrado['Título'] == titulo_seleccionado].iloc[0]
            st.info(f"**Fuente:** {registro['Fuente']} | **Fecha:** {registro['Fecha']}")
            st.markdown(f"**Enlace original:** [Leer en sitio web]({registro['URL']})")

# --- PESTAÑA 2: MÉTRICAS DE EVALUACIÓN (Requisito de la rúbrica) ---
with tab2:
    st.header("¿Cómo evaluamos el aporte de este proyecto?")
    st.markdown("""
    Para medir el éxito y el impacto de este prototipo en la lucha contra la desinformación, proponemos las siguientes métricas:
    
    * **Tasa de Cobertura Diaria:** Medir cuántas noticias oficiales de la OMS y BBC logramos indexar al día. Esto nos da nuestra base de "verdad" (Ground Truth).
    * **Latencia de Actualización:** El tiempo que tarda el sistema desde que la noticia se publica en el RSS hasta que aparece en este Dashboard.
    * **Tasa de Extracción Exitosa:** Porcentaje de intentos de conexión (Requests) que devuelven un código HTTP 200 vs Errores 4xx/5xx, garantizando la estabilidad del sistema.
    """)

# --- PESTAÑA 3: REFLEXIÓN ÉTICA Y LIMITACIONES (Requisito de la rúbrica) ---
with tab3:
    st.header("Limitaciones y Reflexión Ética")
    st.markdown("""
    **Limitaciones del Prototipo:**
    * **Escalabilidad:** Actualmente el sistema procesa datos por lotes y los guarda en un archivo CSV local. Para escalar a millones de datos, requeriríamos migrar a una base de datos NoSQL (ej. MongoDB) y automatizar el pipeline en la nube (ej. AWS o Google Cloud).
    * **Cambios en la Web:** Si la BBC o la OMS cambian la estructura de sus etiquetas XML en los feeds RSS, el script de extracción requerirá mantenimiento manual.
    
    **Reflexión Ética:**
    * **Uso de RSS vs Scraping agresivo:** Elegimos utilizar Feeds RSS deliberadamente. Esto reduce drásticamente la carga sobre los servidores de la OMS y la BBC en comparación con el scraping HTML continuo.
    * **Respeto al robots.txt:** La extracción está diseñada para ser no intrusiva y puramente informativa, cumpliendo estrictamente con los lineamientos de acceso automatizado.
    * **Privacidad:** No se extrae ningún tipo de Información Personal Identificable (PII), únicamente titulares públicos de organizaciones de salud global.
    """)