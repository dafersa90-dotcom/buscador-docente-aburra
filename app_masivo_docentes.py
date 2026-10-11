import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Enfoque y Búsqueda Docente - Valle de Aburrá",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Generador de Enfoque y Vacantes - Valle de Aburrá")
st.markdown(
    "Herramienta inteligente para enfocar tu perfil profesional exclusivamente "
    "en las instituciones y asignaturas exactas que selecciones."
)


# ---------------------------------------------------------
# BASE DE DATOS DE INSTITUCIONES DEL VALLE DE ABURRÁ
# ---------------------------------------------------------
@st.cache_data
def cargar_directorio_enfocado():
  return pd.DataFrame([
      # Medellín
      {
          "Institución": "Colegio San José de Las Vegas",
          "Tipo": "Privado",
          "Municipio": "Medellín",
          "Correo": "comunicaciones@sanjosedelasvegas.edu.co",
          "Áreas": ["Tecnología e Informática", "Robótica", "Matemáticas", "Física"],
          "Enfoque": "Laboratorios STEAM y bilingüismo.",
      },
      {
          "Institución": "
