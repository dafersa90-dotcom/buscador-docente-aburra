
import io
import re
from datetime import date

import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Enfoque Docente | Valle de Aburrá",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.25);
        padding: 16px;
        border-radius: 12px;
    }
    .subtitulo {color: #64748b; font-size: 1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 Enfoque y Búsqueda Docente")
st.markdown(
    '<p class="subtitulo">Directorio de instituciones, enfoque profesional '
    'y seguimiento de oportunidades laborales en el Valle de Aburrá.</p>',
    unsafe_allow_html=True,
)

# =========================================================
# DATOS Y CATÁLOGOS
# =========================================================
MUNICIPIOS = [
    "Medellín",
    "Bello",
    "Envigado",
    "Itagüí",
    "Sabaneta",
    "La Estrella",
    "Caldas",
    "Copacabana",
    "Girardota",
    "Barbosa",
]

AREAS = [
    "Tecnología e Informática",
    "Robótica",
    "Diseño Gráfico",
    "Comunicación",
    "Marketing Digital",
    "Producción Audiovisual",
    "Informática",
    "Programación",
    "Inteligencia Artificial",
    "Diseño Web",
    "Matemáticas",
    "Física",
    "Otras áreas",
]

ESTADOS = [
    "Pendiente",
    "Correo enviado",
    "Convocatoria abierta",
    "Entrevista",
    "Prueba técnica",
    "Contratado",
    "Descartado",
]

COLUMNAS = [
    "Institución",
    "Tipo",
    "Municipio",
    "Correo",
    "Áreas",
    "Enfoque",
    "Estado",
    "Fecha de contacto",
    "Observaciones",
]

# Solo se incluyen registros de ejemplo aportados por el usuario.
# Verifica los datos de contacto antes de enviar una postulación.
DATOS_INICIALES = [
    {
        "Institución": "Colegio San José de Las Vegas",
        "Tipo": "Privado",
        "Municipio": "Medellín",
        "Correo": "comunicaciones@sanjosedelasvegas.edu.co",
        "Áreas": "Tecnología e Informática; Robótica; Matemáticas; Física",
        "Enfoque": "Laboratorios STEAM y bilingüismo.",
        "Estado": "Pendiente",
        "Fecha de contacto": "",
        "Observaciones": "Correo y áreas pendientes de verificación.",
    },
]


def crear_directorio():
    return pd.DataFrame(DATOS_INICIALES, columns=COLUMNAS)


if "directorio" not in st.session_state:
    st.session_state.directorio = crear_directorio()

if "perfil" not in st.session_state:
    st.session_state.perfil = {
        "Nombre": "Daniel Salazar",
        "Profesión": "Licenciado en Comunicación e Informática Educativa",
        "Experiencia": (
            "Docencia en Tecnología e Informática, diseño gráfico, "
            "comunicación digital y creación de contenidos."
        ),
        "Intereses": [
            "Tecnología e Informática",
            "Diseño Gráfico",
            "Comunicación",
            "Marketing Digital",
        ],
        "Municipios": ["Medellín", "Bello", "Envigado", "Itagüí", "La Estrella"],
        "Tipo de institución": ["Privado"],
    }


def normalizar(texto):
    return str(texto).strip().casefold()


def exportar_csv(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def contiene_area(valor, seleccionadas):
    texto = normalizar(valor)
    return any(normalizar(area) in texto for area in seleccionadas)


# =========================================================
# BARRA LATERAL: PERFIL PROFESIONAL
# =========================================================
with st.sidebar:
    st.header("👤 Mi perfil")

    perfil = st.session_state.perfil

    perfil["Nombre"] = st.text_input(
        "Nombre completo",
        value=perfil["Nombre"],
    )

    perfil["Profesión"] = st.text_input(
        "Título profesional",
        value=perfil["Profesión"],
    )

    perfil["Experiencia"] = st.text_area(
        "Experiencia y fortalezas",
        value=perfil["Experiencia"],
        height=130,
    )

    perfil["Intereses"] = st.multiselect(
        "Áreas de interés",
        options=AREAS,
        default=perfil["Intereses"],
    )

    perfil["Municipios"] = st.multiselect(
        "Municipios de interés",
        options=MUNICIPIOS,
        default=perfil["Municipios"],
    )

    perfil["Tipo de institución"] = st.multiselect(
        "Tipo de institución",
        options=["Público", "Privado", "Universidad", "Otro"],
        default=perfil["Tipo de institución"],
    )

    st.divider()
    st.caption(
        "La información del perfil y del directorio se conserva "
        "durante la sesión de Streamlit."
    )

# =========================================================
# NAVEGACIÓN
# =========================================================
tab_busqueda, tab_directorio, tab_perfil, tab_seguimiento = st.tabs(
    [
        "🔎 Buscar oportunidades",
        "🏫 Directorio",
        "✍️ Mi postulación",
        "📌 Seguimiento",
    ]
)

df = st.session_state.directorio.copy()

# =========================================================
# 1. BUSCADOR
# =========================================================
with tab_busqueda:
    st.subheader("Encuentra instituciones compatibles con tu perfil")
    st.write(
        "Filtra por ubicación, sector educativo y asignaturas. "
        "Los resultados dependen de los registros que hayas agregado."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        municipios = st.multiselect(
            "Municipios",
            MUNICIPIOS,
            default=perfil["Municipios"],
            key="buscar_municipios",
        )

    with col2:
        tipos = st.multiselect(
            "Tipo de institución",
            ["Público", "Privado", "Universidad", "Otro"],
            default=perfil["Tipo de institución"],
            key="buscar_tipos",
        )

    with col3:
        areas = st.multiselect(
            "Asignaturas o áreas",
            AREAS,
            default=perfil["Intereses"],
            key="buscar_areas",
        )

    termino = st.text_input(
        "Buscar por nombre, enfoque, correo o palabra clave",
        placeholder="Ej.: robótica, diseño, comunicación...",
    )

    resultados = df.copy()

    if municipios:
        resultados = resultados[
            resultados["Municipio"].isin(municipios)
        ]
    else:
        resultados = resultados.iloc[0:0]

    if tipos:
        resultados = resultados[resultados["Tipo"].isin(tipos)]
    else:
        resultados = resultados.iloc[0:0]

    if areas:
        resultados = resultados[
            resultados["Áreas"].apply(
                lambda valor: contiene_area(valor, areas)
            )
        ]
    else:
        resultados = resultados.iloc[0:0]

    if termino.strip():
        patron = re.escape(termino.strip())
        mascara = resultados.apply(
            lambda fila: fila.astype(str).str.contains(
                patron, case=False, regex=True
            ).any(),
            axis=1,
        )
        resultados = resultados[mascara]

    st.metric("Instituciones coincidentes", len(resultados))

    if resultados.empty:
        st.info(
            "No hay coincidencias con los filtros actuales. "
            "Prueba otras áreas o agrega instituciones al directorio."
        )
    else:
        for _, fila in resultados.iterrows():
            with st.container(border=True):
                izquierda, derecha = st.columns([3, 1])

                with izquierda:
                    st.markdown(f"### {fila['Institución']}")
                    st.write(
                        f"**Ubicación:** {fila['Municipio']} · "
                        f"**Sector:** {fila['Tipo']}"
                    )
                    st.write(f"**Áreas:** {fila['Áreas']}")
                    st.write(f"**Enfoque:** {fila['Enfoque']}")
                    st.caption(f"Estado: {fila['Estado']}")

                with derecha:
                    correo = str(fila["Correo"]).strip()
                    correo_valido = bool(
                        re.fullmatch(
                            r"[^@\s]+@[^@\s]+\.[^@\s]+",
                            correo,
                        )
                    )

                    if correo_valido:
                        st.link_button(
                            "Contactar",
                            f"mailto:{correo}",
                            use_container_width=True,
                        )
                    else:
                        st.caption("Sin correo válido registrado")

                    st.caption(
                        "Confirma el contacto y las vacantes "
                        "en los canales oficiales."
                    )

# =========================================================
# 2. DIRECTORIO EDITABLE
# =========================================================
with tab_directorio:
    st.subheader("Base de datos de instituciones")

    st.info(
        "Agrega instituciones reales y verifica sus datos. "
        "La aplicación no confirma vacantes activas automáticamente."
    )

    archivo = st.file_uploader(
        "Importar directorio desde CSV",
        type=["csv"],
        help="El archivo debe tener columnas compatibles con el directorio.",
    )

    if archivo is not None:
        if st.button("Importar registros", key="importar_csv"):
            try:
                importado = pd.read_csv(archivo).fillna("")
                faltantes = [
                    col for col in COLUMNAS
                    if col not in importado.columns
                ]

                if faltantes:
                    st.error(
                        "Faltan estas columnas: "
                        + ", ".join(faltantes)
                    )
                else:
                    importado = importado[COLUMNAS]
                    st.session_state.directorio = pd.concat(
                        [
                            st.session_state.directorio,
                            importado,
                        ],
                        ignore_index=True,
                    ).drop_duplicates(
                        subset=["Institución", "Municipio"],
                        keep="last",
                    )
                    st.success("Directorio importado correctamente.")
                    st.rerun()
            except Exception as error:
                st.error(f"No fue posible importar el archivo: {error}")

    with st.form("nuevo_registro"):
        st.markdown("#### Agregar institución")

        c1, c2 = st.columns(2)

        with c1:
            nueva_institucion = st.text_input("Nombre de la institución")
            nuevo_municipio = st.selectbox("Municipio", MUNICIPIOS)
            nuevo_tipo = st.selectbox(
                "Sector",
                ["Privado", "Público", "Universidad", "Otro"],
            )
            nuevo_correo = st.text_input("Correo de contacto")

        with c2:
            nuevas_areas = st.multiselect(
                "Áreas relacionadas",
                AREAS,
                key="nuevas_areas",
            )
            nuevo_enfoque = st.text_area(
                "Enfoque institucional o notas",
                height=90,
            )
            nuevo_estado = st.selectbox("Estado", ESTADOS)

        guardar = st.form_submit_button(
            "Guardar institución",
            type="primary",
        )

        if guardar:
            if not nueva_institucion.strip():
                st.error("Escribe el nombre de la institución.")
            else:
                registro = {
                    "Institución": nueva_institucion.strip(),
                    "Tipo": nuevo_tipo,
                    "Municipio": nuevo_municipio,
                    "Correo": nuevo_correo.strip(),
                    "Áreas": "; ".join(nuevas_areas),
                    "Enfoque": nuevo_enfoque.strip(),
                    "Estado": nuevo_estado,
                    "Fecha de contacto": "",
                    "Observaciones": "Registro agregado manualmente.",
                }

                actual = st.session_state.directorio
                duplicado = (
                    actual["Institución"].map(normalizar)
                    == normalizar(nueva_institucion)
                ) & (
                    actual["Municipio"].map(normalizar)
                    == normalizar(nuevo_municipio)
                )

                if duplicado.any():
                    st.warning(
                        "Esta institución ya existe en ese municipio."
                    )
                else:
                    st.session_state.directorio = pd.concat(
                        [actual, pd.DataFrame([registro])],
                        ignore_index=True,
                    )
                    st.success("Institución agregada.")
                    st.rerun()

    st.markdown("#### Editar registros existentes")

    editado = st.data_editor(
        st.session_state.directorio,
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        key="editor_directorio",
        column_config={
            "Institución": st.column_config.TextColumn(required=True),
            "Tipo": st.column_config.SelectboxColumn(
                options=["Privado", "Público", "Universidad", "Otro"]
            ),
            "Municipio": st.column_config.SelectboxColumn(
                options=MUNICIPIOS
            ),
            "Estado": st.column_config.SelectboxColumn(
                options=ESTADOS
            ),
            "Fecha de contacto": st.column_config.TextColumn(
                help="Formato sugerido: AAAA-MM-DD"
            ),
        },
    )

    if st.button("Guardar cambios del directorio"):
        st.session_state.directorio = editado[COLUMNAS].fillna("")
        st.success("Cambios guardados en la sesión.")
        st.rerun()

    st.download_button(
        "⬇️ Descargar directorio CSV",
        data=exportar_csv(st.session_state.directorio),
        file_name="directorio_docente_valle_aburra.csv",
        mime="text/csv",
    )

# =========================================================
# 3. GENERADOR DE POSTULACIÓN
# =========================================================
with tab_perfil:
    st.subheader("Generador de enfoque profesional")

    st.write(
        "Selecciona una institución y genera un texto base "
        "que puedas adaptar a una postulación."
    )

    opciones = st.session_state.directorio["Institución"].tolist()

    if opciones:
        institucion_objetivo = st.selectbox(
            "Institución objetivo",
            opciones,
        )

        registro = st.session_state.directorio[
            st.session_state.directorio["Institución"]
            == institucion_objetivo
        ].iloc[0]

        enfoque_texto = st.text_area(
            "¿Qué deseas destacar para esta institución?",
            value=(
                f"Mi experiencia en {perfil['Experiencia']} "
                f"Me interesa aportar especialmente en "
                f"{registro['Áreas']}."
            ),
            height=140,
        )

        texto_postulacion = f"""
Asunto: Postulación profesional – {", ".join(perfil["Intereses"])}

Cordial saludo, equipo de {institucion_objetivo}:

Mi nombre es {perfil["Nombre"]}, soy {perfil["Profesión"]} y
cuento con experiencia en educación, tecnología, comunicación
y creación de contenidos digitales.

{enfoque_texto}

Me gustaría conocer posibles oportunidades de vinculación en las
áreas relacionadas con mi perfil y compartir mi hoja de vida y
portafolio para su consideración.

Agradezco su tiempo y atención.

Atentamente,
{perfil["Nombre"]}
""".strip()

        st.text_area(
            "Texto listo para revisar y copiar",
            value=texto_postulacion,
            height=300,
            key="texto_final",
        )

        st.download_button(
            "⬇️ Descargar texto de postulación",
            data=texto_postulacion,
            file_name="postulacion_docente.txt",
            mime="text/plain",
        )

        correo_objetivo = str(registro["Correo"]).strip()

        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo_objetivo):
            st.link_button(
                "Abrir correo para esta institución",
                "mailto:" + correo_objetivo
                + "?subject="
                + "Postulacion%20profesional",
            )

        st.caption(
            "Revisa el contenido, confirma el destinatario y adjunta "
            "tu hoja de vida antes de enviar. La aplicación no envía "
            "correos por sí misma."
        )
    else:
        st.info("Agrega una institución para generar una postulación.")

# =========================================================
# 4. SEGUIMIENTO DE POSTULACIONES
# =========================================================
with tab_seguimiento:
    st.subheader("Seguimiento de oportunidades")

    seguimiento = st.session_state.directorio.copy()

    total = len(seguimiento)
    enviados = seguimiento["Estado"].isin(
        ["Correo enviado", "Entrevista", "Prueba técnica", "Contratado"]
    ).sum()
    entrevistas = seguimiento["Estado"].eq("Entrevista").sum()
    contratados = seguimiento["Estado"].eq("Contratado").sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Instituciones", total)
    m2.metric("Contactos o procesos", int(enviados))
    m3.metric("Entrevistas", int(entrevistas))
    m4.metric("Contrataciones", int(contratados))

    st.markdown("#### Distribución por estado")

    if total:
        resumen = (
            seguimiento["Estado"]
            .value_counts()
            .rename_axis("Estado")
            .reset_index(name="Cantidad")
        )
        st.bar_chart(resumen.set_index("Estado"))

        st.markdown("#### Registro de contactos")

        st.dataframe(
            seguimiento[
                [
                    "Institución",
                    "Municipio",
                    "Áreas",
                    "Estado",
                    "Fecha de contacto",
                    "Observaciones",
                ]
            ],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info(
            "Tu seguimiento está vacío. Agrega instituciones "
            "y actualiza su estado desde el directorio."
        )

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.divider()
st.caption(
    "Enfoque Docente · Valle de Aburrá | Herramienta de organización "
    "profesional. Las vacantes y los contactos deben verificarse "
    "con cada institución."
)
