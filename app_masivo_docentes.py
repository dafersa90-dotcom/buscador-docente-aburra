import io
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
          "Institución": "Colegio San Lucas",
          "Tipo": "Privado",
          "Municipio": "Medellín",
          "Correo": "secretaria@colegiosanlucas.edu.co",
          "Áreas": ["Educación Inclusiva / Neurodivergencia", "Lengua Castellana y Literatura"],
          "Enfoque": "Inclusión y desarrollo emocional.",
      },
      {
          "Institución": "Institución Educativa Cefa",
          "Tipo": "Oficial / Pública",
          "Municipio": "Medellín",
          "Correo": "ie.cefa@medellin.gov.co",
          "Áreas": ["Matemáticas", "Álgebra", "Geometría", "Estadística", "Cálculo"],
          "Enfoque": "Educación media femenina de alta exigencia.",
      },
      {
          "Institución": "I.E. Inem José Félix de Restrepo",
          "Tipo": "Oficial / Pública",
          "Municipio": "Medellín",
          "Correo": "contacto@inemmedellin.edu.co",
          "Áreas": ["Matemáticas", "Álgebra", "Física", "Química", "Tecnología e Informática"],
          "Enfoque": "Modalidades técnicas y científicas diversificadas.",
      },
      {
          "Institución": "Colegio Gimnasio Los Alcázares",
          "Tipo": "Privado",
          "Municipio": "Medellín",
          "Correo": "info@alcazares.edu.co",
          "Áreas": ["Matemáticas", "Cálculo", "Física", "Emprendimiento / Gestión Empresarial"],
          "Enfoque": "Formación integral y liderazgo.",
      },
      {
          "Institución": "Universidad de Medellín",
          "Tipo": "Universidad",
          "Municipio": "Medellín",
          "Correo": "secretaria@udem.edu.co",
          "Áreas": ["Matemáticas", "Cálculo", "Estadística", "Ingeniería"],
          "Enfoque": "Educación superior e investigación.",
      },
      {
          "Institución": "Universidad Nacional de Colombia (Sede Medellín)",
          "Tipo": "Universidad",
          "Municipio": "Medellín",
          "Correo": "dirdoc_med@unal.edu.co",
          "Áreas": ["Matemáticas", "Física", "Álgebra", "Cálculo", "Robótica"],
          "Enfoque": "Investigación científica y tecnológica avanzada.",
      },
      # Envigado
      {
          "Institución": "Colegio Benedictino de Santa María",
          "Tipo": "Privado",
          "Municipio": "Envigado",
          "Correo": "teescuchamos@colegiobenedictino.edu.co",
          "Áreas": ["Filosofía", "Biología", "Química", "Matemáticas"],
          "Enfoque": "Pensamiento científico y valores humanistas.",
      },
      {
          "Institución": "Colegio Cumbres",
          "Tipo": "Privado",
          "Municipio": "Envigado",
          "Correo": "info@cumbres.edu.co",
          "Áreas": ["Cálculo", "Física", "Inglés", "Matemáticas"],
          "Enfoque": "Bilingüismo internacional y ciencias avanzadas.",
      },
      {
          "Institución": "I.E. Envigado",
          "Tipo": "Oficial / Pública",
          "Municipio": "Envigado",
          "Correo": "contacto@ieenvigado.edu.co",
          "Áreas": ["Matemáticas", "Álgebra", "Trigonometría", "Cálculo", "Física"],
          "Enfoque": "Formación académica integral pública.",
      },
      {
          "Institución": "Colegio La Salle Envigado",
          "Tipo": "Privado",
          "Municipio": "Envigado",
          "Correo": "contacto@lasalleenvigado.edu.co",
          "Áreas": ["Matemáticas", "Tecnología e Informática", "Religión y Ética"],
          "Enfoque": "Tradición formativa y tecnología.",
      },
      # Itagüí
      {
          "Institución": "Colegio Canadiense",
          "Tipo": "Privado",
          "Municipio": "Itagüí",
          "Correo": "info@colegiocanadiense.edu.co",
          "Áreas": ["Tecnología e Informática", "Matemáticas", "Geometría"],
          "Enfoque": "Inmersión digital y currículo canadiense.",
      },
      {
          "Institución": "I.E. Luis Carlos Galán Sarmiento",
          "Tipo": "Oficial / Pública",
          "Municipio": "Itagüí",
          "Correo": "contacto@galanitagui.edu.co",
          "Áreas": ["Matemáticas", "Estadística", "Física", "Álgebra"],
          "Enfoque": "Cobertura educativa oficial y técnica.",
      },
      # Bello
      {
          "Institución": "Instituto Parroquial Jesús de La Buena Esperanza",
          "Tipo": "Privado",
          "Municipio": "Bello",
          "Correo": "cpjbe@une.net.co",
          "Áreas": ["Trigonometría", "Estadística", "Tecnología e Informática"],
          "Enfoque": "Énfasis comercial y técnico.",
      },
      {
          "Institución": "I.E. Marco Fidel Suárez",
          "Tipo": "Oficial / Pública",
          "Municipio": "Bello",
          "Correo": "contacto@marcofidelbello.edu.co",
          "Áreas": ["Matemáticas", "Álgebra", "Geometría", "Física"],
          "Enfoque": "Institución oficial emblemática de Bello.",
      },
      # Sabaneta
      {
          "Institución": "Colegio San Marcos",
          "Tipo": "Privado",
          "Municipio": "Sabaneta",
          "Correo": "secretaria@colegiosanmarcos.edu.co",
          "Áreas": ["Robótica", "Matemáticas", "Diseño Digital", "Física"],
          "Enfoque": "Robótica y desarrollo tecnológico escolar.",
      },
      {
          "Institución": "Colegio San José de Calasanz",
          "Tipo": "Privado",
          "Municipio": "La Estrella",
          "Correo": "info@calasanzlaestrella.edu.co",
          "Áreas": ["Biología", "Química", "Matemáticas", "Física"],
          "Enfoque": "Ecología y ciencias exactas.",
      },
      {
          "Institución": "Colegio Campestre Horizontes",
          "Tipo": "Privado",
          "Municipio": "Caldas",
          "Correo": "contacto@colegiohorizontes.edu.co",
          "Áreas": ["Metodología de la Investigación", "Biología", "Matemáticas"],
          "Enfoque": "Ambiente campestre e investigación.",
      },
  ])


df_instituciones = cargar_directorio_enfocado()

# ---------------------------------------------------------
# PANEL LATERAL DE FILTROS Y ENFOQUE
# ---------------------------------------------------------
st.sidebar.title("🎛️ Panel de Enfoque Docente")

perfil_usuario = st.sidebar.text_area(
    "Tu Perfil Profesional:",
    (
        "Licenciado en Matemáticas experto en álgebra, geometría y cálculo,"
        " con enfoque pedagógico activo."
    ),
    height=90,
)

municipios_disponibles = sorted(df_instituciones["Municipio"].unique().tolist())
municipios_seleccionados = st.sidebar.multiselect(
    "Selecciona Municipio(s):",
    options=municipios_disponibles,
    default=["Medellín", "Envigado"],
)

todas_areas = sorted(
    list(set([a for sublist in df_instituciones["Áreas"] for a in sublist]))
)
areas_seleccionadas = st.sidebar.multiselect(
    "Selecciona Asignatura(s) a Enfocar:",
    options=todas_areas,
    default=["Matemáticas", "Cálculo"],
)

# Botón de ejecución con enfoque estricto
ejecutar_btn = st.sidebar.button(
    "🚀 Generar Enfoque y Opciones", type="primary"
)

# ---------------------------------------------------------
# CUERPO PRINCIPAL
# ---------------------------------------------------------
st.subheader("📋 Instituciones Focalizadas según tus Asignaturas")

if ejecutar_btn:
  if not municipios_seleccionados or not areas_seleccionadas:
    st.warning(
        "⚠️ Por favor selecciona al menos un municipio y una asignatura en el"
        " panel lateral."
    )
  else:
    # FILTRADO ESTRICTO: Instituciones que coincidan con los municipios y contengan al menos una de las áreas seleccionadas
    df_filtrado = df_instituciones[
        df_instituciones["Municipio"].isin(municipios_seleccionados)
    ]
    df_filtrado = df_filtrado[
        df_filtrado["Áreas"].apply(
            lambda x: any(area in x for area in areas_seleccionadas)
        )
    ]

    if not df_filtrado.empty:
      st.success(
          f"¡Se encontraron {len(df_filtrado)} instituciones enfocadas en tus"
          " áreas!"
      )

      resultados_enfocados = []
      for _, row in df_filtrado.iterrows():
        query_enfocada = f"vacantes docente {row['Institución']} {row['Municipio']} {' '.join(areas_seleccionadas)}"
        link_google = (
            f"https://www.google.com/search?q={query_enfocada.replace(' ', '+')}"
        )

        resultados_enfocados.append({
            "Institución": row["Institución"],
            "Tipo": row["Tipo"],
            "Municipio": row["Municipio"],
            "Correo de Contacto": row["Correo"],
            "Áreas Coincidentes": ", "
            .join([a for a in row["Áreas"] if a in areas_seleccionadas]),
            "Enfoque Institucional": row["Enfoque"],
            "Enlace de Búsqueda Activa": link_google,
        })

      df_final = pd.DataFrame(resultados_enfocados)
      st.dataframe(df_final, use_container_width=True)

      # Generar archivo Excel en memoria para descarga directa en la nube
      output = io.BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_final.to_excel(writer, index=False, sheet_name="Instituciones")
      excel_data = output.getvalue()

      st.download_button(
          label="📥 Descargar Reporte en Excel (.xlsx)",
          data=excel_data,
          file_name="Reporte_Enfocado_Docentes_Aburra.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          type="primary",
      )
    else:
      st.warning(
          "No se encontraron instituciones que coincidan con la combinación de"
          " municipios y áreas seleccionadas. Prueba ampliando los filtros."
      )
else:
  st.info(
      "👈 Configura tus municipios y asignaturas en la barra lateral y haz clic"
      " en **'🚀 Generar Enfoque y Opciones'**."
  )
