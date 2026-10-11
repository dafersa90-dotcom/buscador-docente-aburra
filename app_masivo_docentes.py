
import streamlit as st
from openai import OpenAI

st.subheader("Buscador inteligente de vacantes docentes")

st.write(
    "Busca oportunidades laborales en colegios y universidades "
    "del Valle de Aburrá utilizando inteligencia artificial."
)

# Leer la clave desde los secretos de Streamlit
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = None

if not api_key:
    st.warning(
        "Configura OPENAI_API_KEY en los secretos de Streamlit "
        "para habilitar la búsqueda inteligente."
    )
else:
    cliente = OpenAI(api_key=api_key)

    consulta = st.text_input(
        "¿Qué vacantes deseas encontrar?",
        placeholder=(
            "Ej.: docente de Tecnología e Informática "
            "en colegios privados de Medellín"
        ),
    )

    if st.button("Buscar vacantes", type="primary"):
        if not consulta.strip():
            st.warning("Escribe qué tipo de vacantes buscas.")
        else:
            instruccion = f"""
            Busca oportunidades laborales docentes en internet
            relacionadas con esta solicitud:

            {consulta}

            Prioriza fuentes oficiales de colegios, universidades,
            secretarías de educación y portales de empleo reconocidos.

            Para cada oportunidad encontrada, indica:
            - Institución y cargo.
            - Municipio.
            - Requisitos publicados.
            - Fecha de publicación, si está disponible.
            - Estado de la convocatoria, solo si se puede verificar.
            - Enlace directo a la fuente.

            No inventes vacantes, correos, fechas ni enlaces.
            Diferencia las convocatorias vigentes de las antiguas
            o de aquellas cuya vigencia no se pudo confirmar.
            Si no encuentras resultados verificables, indícalo.
            """

            with st.spinner("Buscando y analizando resultados..."):
                try:
                    respuesta = cliente.responses.create(
                        model="gpt-4.1",
                        tools=[
                            {"type": "web_search"}
                        ],
                        input=instruccion,
                    )

                    st.markdown("### Resultados de la búsqueda")
                    st.markdown(respuesta.output_text)

                except Exception as error:
                    st.error(
                        "No fue posible completar la búsqueda. "
                        "Verifica la clave API, el acceso al modelo, "
                        "la facturación y la configuración de búsqueda web."
                    )
                    st.caption(f"Detalle técnico: {error}")
