
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Buscador de instituciones educativas",
    page_icon="🔎",
    layout="wide"
)

# CONFIGURACIÓN DE OPENAI
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = ""

st.title("Buscador de instituciones educativas")
st.write(
    "Encuentra instituciones educativas, colegios privados "
    "y oportunidades laborales en el Valle de Aburrá."
)

if not API_KEY:
    st.error(
        "No se encuentra OPENAI_API_KEY. Configúrala en "
        "Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

# FORMULARIO DE BÚSQUEDA
with st.form("formulario_busqueda"):
    consulta = st.text_input(
        "¿Qué deseas encontrar?",
        placeholder=(
            "Ej.: colegios privados que busquen docentes "
            "de Tecnología e Informática"
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

# EJECUCIÓN DE LA BÚSQUEDA
if buscar:
    if not consulta.strip():
        st.warning("Escribe lo que deseas buscar.")
        st.stop()

    consulta_final = consulta.strip()

    if municipio != "Todos los municipios del Valle de Aburrá":
        consulta_final += f". Municipio: {municipio}"
    else:
        consulta_final += (
            ". Ubicación: Valle de Aburrá, Antioquia, Colombia"
        )

    instrucciones = f"""
    Busca en internet información relevante y actualizada sobre:
    {consulta_final}

    Prioriza fuentes oficiales y páginas verificables.

    Para instituciones educativas y empleos, identifica cuando
    la información esté disponible:
    1. Nombre de la institución.
    2. Municipio.
    3. Vacante o convocatoria publicada.
    4. Área o asignatura.
    5. Correo institucional o contacto público.
    6. Enlace directo a la fuente.

    No inventes datos, correos, teléfonos ni vacantes.
    Diferencia las vacantes confirmadas de las instituciones
    que simplemente podrían recibir hojas de vida.

    Si no encuentras resultados, indícalo claramente.
    Presenta la información en español y con enlaces.
    """

    try:
        cliente = OpenAI(api_key=API_KEY)

        with st.spinner("Buscando información en internet..."):
            respuesta = cliente.responses.create(
                model="gpt-4.1",
                tools=[
                    {"type": "web_search"}
                ],
                tool_choice="required",
                input=instrucciones
            )

        resultado = respuesta.output_text

        if resultado and resultado.strip():
            st.subheader("Resultados de la búsqueda")
            st.markdown(resultado)
        else:
            st.warning("La búsqueda no devolvió resultados.")

    except Exception as error:
        st.error("No se pudo completar la búsqueda.")
        st.code(
            f"{type(error).__name__}: {error}",
            language="text"
        )
        st.caption(
            "Revisa la validez de la clave, el acceso al modelo, "
            "el saldo o límite de uso de la API y la configuración "
            "de la herramienta de búsqueda web."
        )
