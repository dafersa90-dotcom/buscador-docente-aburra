
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Buscador de instituciones educativas",
    page_icon="🔎",
    layout="wide"
)

st.title("Buscador de instituciones educativas")
st.write(
    "Busca colegios, instituciones educativas y vacantes "
    "docentes en Medellín y el Valle de Aburrá."
)

# 1. Leer la clave de forma segura
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = None

if not api_key:
    st.error(
        "Falta OPENAI_API_KEY en Settings → Secrets "
        "de Streamlit Cloud."
    )
    st.stop()

# 2. Formulario de búsqueda
with st.form("formulario_busqueda"):
    consulta = st.text_input(
        "¿Qué deseas encontrar?",
        placeholder=(
            "Ej.: colegios privados de Medellín "
            "que busquen docentes de tecnología"
        )
    )

    municipio = st.selectbox(
        "Municipio",
        [
            "Todos los municipios del Valle de Aburrá",
            "Medellín",
            "Bello",
            "Envigado",
            "Itagüí",
            "La Estrella",
            "Sabaneta",
            "Caldas",
            "Copacabana",
            "Girardota",
            "Barbosa"
        ]
    )

    buscar = st.form_submit_button(
        "Buscar en internet",
        type="primary",
        use_container_width=True
    )

# 3. Ejecutar la búsqueda
if buscar:
    if not consulta.strip():
        st.warning("Escribe qué institución o vacante deseas buscar.")
        st.stop()

    consulta_final = consulta.strip()

    if municipio != "Todos los municipios del Valle de Aburrá":
        consulta_final += f". Municipio: {municipio}"
    else:
        consulta_final += ". Zona: Valle de Aburrá, Antioquia, Colombia"

    instruccion = f"""
    Investiga en internet la siguiente consulta:

    {consulta_final}

    Prioriza información verificable y actualizada de Colombia.

    Si corresponde, identifica:
    - Nombre de la institución educativa.
    - Municipio y dirección, si está publicada.
    - Vacante o convocatoria docente.
    - Área o asignatura.
    - Correo institucional o medio de contacto público.
    - Enlace directo a la página que respalda cada resultado.

    No inventes instituciones, vacantes, correos ni direcciones.
    Diferencia las vacantes confirmadas de las instituciones
    que solamente podrían recibir hojas de vida.
    Si no encuentras información suficiente, dilo claramente.

    Presenta los resultados organizados y con enlaces clicables.
    """

    try:
        with st.spinner("Buscando información en internet..."):
            cliente = OpenAI(api_key=api_key)

            respuesta = cliente.responses.create(
                model="gpt-4.1",
                tools=[
                    {
                        "type": "web_search",
                        "search_context_size": "high"
                    }
                ],
                tool_choice="required",
                input=instruccion
            )

        resultado = respuesta.output_text

        if resultado and resultado.strip():
            st.subheader("Resultados de la búsqueda")
            st.markdown(resultado)
        else:
            st.warning(
                "La API respondió, pero no devolvió texto. "
                "Intenta con otra consulta."
            )

        # Mostrar información técnica para diagnosticar
        with st.expander("Información de diagnóstico"):
            st.write("ID de respuesta:", respuesta.id)
            st.write("Modelo:", respuesta.model)
            st.write("Respuesta recibida correctamente.")

    except Exception as error:
        st.error("No se pudo completar la búsqueda.")
        st.code(
            f"{type(error).__name__}: {error}",
            language="text"
        )
        st.info(
            "Comprueba la clave API, el saldo o límite de uso "
            "de la API y los permisos del modelo."
        )
