
import re
import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Buscador de Instituciones Educativas",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Buscador de Instituciones Educativas")
st.write(
    "Consulta instituciones del Valle de Aburrá según el municipio, "
    "el sector educativo y las áreas de interés."
)

# =========================================================
# CONSTANTES
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

TIPOS = ["Privado", "Público", "Universidad", "Otro"]

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

# =========================================================
# BASE DE DATOS INICIAL
# =========================================================

DATOS_INICIALES = [
    {
        "Institución": "Colegio San José de Las Vegas",
        "Tipo": "Privado",
        "Municipio": "Medellín",
        "Correo": "comunicaciones@sanjosedelasvegas.edu.co",
        "Áreas": (
            "Tecnología e Informática; Robótica; Matemáticas; Física"
        ),
        "Enfoque": "Laboratorios STEAM y bilingüismo.",
        "Estado": "Pendiente",
        "Fecha de contacto": "",
        "Observaciones": (
            "Verificar correo, áreas de contratación y vacantes."
        ),
    },
]


def crear_directorio():
    return pd.DataFrame(DATOS_INICIALES, columns=COLUMNAS)


# =========================================================
# INICIALIZAR SESIÓN
# =========================================================

if "directorio" not in st.session_state:
    st.session_state.directorio = crear_directorio()

if "resultados_busqueda" not in st.session_state:
    st.session_state.resultados_busqueda = None

if "busqueda_realizada" not in st.session_state:
    st.session_state.busqueda_realizada = False


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def normalizar(texto):
    return str(texto).strip().casefold()


def correo_valido(correo):
    correo = str(correo).strip()
    return bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo)
    )


def contiene_area(valor, seleccionadas):
    texto = normalizar(valor)
    return any(
        normalizar(area) in texto
        for area in seleccionadas
    )


def preparar_directorio(df):
    """Garantiza que el directorio tenga las columnas requeridas."""
    df = df.copy()

    for columna in COLUMNAS:
        if columna not in df.columns:
            df[columna] = ""

    df = df[COLUMNAS].fillna("")

    for columna in COLUMNAS:
        df[columna] = df[columna].astype(str)

    return df


def exportar_csv(df):
    return df.to_csv(index=False).encode("utf-8-sig")


# =========================================================
# INDICADORES
# =========================================================

directorio = st.session_state.directorio

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Instituciones registradas", len(directorio))

with col2:
    st.metric(
        "Municipios registrados",
        directorio["Municipio"].nunique()
        if not directorio.empty else 0,
    )

with col3:
    st.metric(
        "Procesos de contacto",
        int(
            directorio["Estado"].isin(
                ["Correo enviado", "Entrevista", "Prueba técnica"]
            ).sum()
        ),
    )

st.divider()

# =========================================================
# PESTAÑAS PRINCIPALES
# =========================================================

tab_busqueda, tab_directorio, tab_seguimiento = st.tabs(
    [
        "🔎 Buscar instituciones",
        "🏫 Directorio",
        "📌 Seguimiento",
    ]
)

# =========================================================
# PESTAÑA 1: BUSCADOR
# =========================================================

with tab_busqueda:

    st.subheader("Buscar instituciones educativas")

    st.write(
        "Selecciona uno o varios filtros. Si dejas un filtro vacío, "
        "no se aplicará ninguna restricción por ese criterio."
    )

    with st.form("formulario_busqueda"):

        col1, col2, col3 = st.columns(3)

        with col1:
            municipios = st.multiselect(
                "Municipio",
                options=MUNICIPIOS,
                key="filtro_municipios",
            )

        with col2:
            tipos = st.multiselect(
                "Tipo de institución",
                options=TIPOS,
                key="filtro_tipos",
            )

        with col3:
            areas = st.multiselect(
                "Área de interés",
                options=AREAS,
                key="filtro_areas",
            )

        termino = st.text_input(
            "Palabra clave (opcional)",
            placeholder="Ej.: robótica, diseño, informática...",
        )

        buscar = st.form_submit_button(
            "🔎 Buscar",
            type="primary",
            use_container_width=True,
        )

    if buscar:

        resultados = st.session_state.directorio.copy()

        if municipios:
            resultados = resultados[
                resultados["Municipio"].isin(municipios)
            ]

        if tipos:
            resultados = resultados[
                resultados["Tipo"].isin(tipos)
            ]

        if areas:
            resultados = resultados[
                resultados["Áreas"].apply(
                    lambda valor: contiene_area(valor, areas)
                )
            ]

        if termino.strip():
            patron = re.escape(termino.strip())

            mascara = resultados.apply(
                lambda fila: fila.astype(str).str.contains(
                    patron,
                    case=False,
                    regex=True,
                ).any(),
                axis=1,
            )

            resultados = resultados[mascara]

        st.session_state.resultados_busqueda = resultados.copy()
        st.session_state.busqueda_realizada = True

    # Mostrar resultados después de presionar Buscar
    if st.session_state.busqueda_realizada:

        resultados = st.session_state.resultados_busqueda

        st.divider()
        st.subheader("Resultados")

        st.metric(
            "Instituciones encontradas",
            len(resultados),
        )

        if resultados.empty:

            st.warning(
                "No se encontraron instituciones con esos criterios. "
                "Prueba con otros filtros o agrega instituciones "
                "en la pestaña Directorio."
            )

        else:

            for _, fila in resultados.iterrows():

                with st.container(border=True):

                    st.markdown(f"### {fila['Institución']}")

                    col_info, col_contacto = st.columns([3, 1])

                    with col_info:

                        st.write(
                            f"**Municipio:** {fila['Municipio']}"
                        )

                        st.write(
                            f"**Tipo:** {fila['Tipo']}"
                        )

                        st.write(
                            f"**Áreas:** {fila['Áreas']}"
                        )

                        st.write(
                            f"**Enfoque:** {fila['Enfoque']}"
                        )

                        st.write(
                            f"**Estado:** {fila['Estado']}"
                        )

                    with col_contacto:

                        correo = str(fila["Correo"]).strip()

                        if correo_valido(correo):

                            st.link_button(
                                "Contactar",
                                f"mailto:{correo}",
                                use_container_width=True,
                            )

                        else:

                            st.caption(
                                "No hay un correo válido registrado."
                            )

                        st.caption(
                            "Verifica la información y las vacantes "
                            "en los canales oficiales."
                        )

            st.download_button(
                "⬇️ Descargar resultados CSV",
                data=exportar_csv(resultados),
                file_name="resultados_busqueda_docente.csv",
                mime="text/csv",
            )

    else:

        st.info(
            "Configura los filtros y presiona el botón Buscar "
            "para consultar las instituciones."
        )


# =========================================================
# PESTAÑA 2: DIRECTORIO
# =========================================================

with tab_directorio:

    st.subheader("Directorio de instituciones")

    st.write(
        "Agrega nuevas instituciones, importa registros o actualiza "
        "la información existente."
    )

    # -----------------------------------------------------
    # IMPORTAR CSV
    # -----------------------------------------------------

    st.markdown("#### Importar directorio")

    archivo = st.file_uploader(
        "Selecciona un archivo CSV",
        type=["csv"],
        key="archivo_directorio",
    )

    if archivo is not None:

        if st.button(
            "Importar registros",
            key="boton_importar",
        ):

            try:

                importado = pd.read_csv(
                    archivo,
                    dtype=str,
                ).fillna("")

                if "Institución" not in importado.columns:

                    st.error(
                        "El archivo debe incluir una columna "
                        "llamada Institución."
                    )

                else:

                    importado = preparar_directorio(importado)

                    actual = st.session_state.directorio

                    combinado = pd.concat(
                        [actual, importado],
                        ignore_index=True,
                    )

                    combinado["_clave"] = (
                        combinado["Institución"].map(normalizar)
                        + "|"
                        + combinado["Municipio"].map(normalizar)
                    )

                    combinado = combinado.drop_duplicates(
                        subset="_clave",
                        keep="last",
                    ).drop(columns="_clave")

                    st.session_state.directorio = preparar_directorio(
                        combinado
                    )

                    st.session_state.busqueda_realizada = False
                    st.session_state.resultados_busqueda = None

                    st.success(
                        "El directorio se importó correctamente."
                    )

                    st.rerun()

            except Exception as error:

                st.error(
                    f"No fue posible importar el archivo: {error}"
                )

    st.divider()

    # -----------------------------------------------------
    # AGREGAR INSTITUCIÓN
    # -----------------------------------------------------

    st.markdown("#### Agregar institución")

    with st.form("formulario_nueva_institucion"):

        col1, col2 = st.columns(2)

        with col1:

            nueva_institucion = st.text_input(
                "Nombre de la institución"
            )

            nuevo_municipio = st.selectbox(
                "Municipio",
                MUNICIPIOS,
            )

            nuevo_tipo = st.selectbox(
                "Tipo",
                TIPOS,
            )

            nuevo_correo = st.text_input(
                "Correo institucional"
            )

        with col2:

            nuevas_areas = st.multiselect(
                "Áreas relacionadas",
                AREAS,
                key="nuevas_areas",
            )

            nuevo_enfoque = st.text_area(
                "Enfoque institucional",
                height=100,
            )

            nuevo_estado = st.selectbox(
                "Estado inicial",
                ESTADOS,
            )

        nuevas_observaciones = st.text_area(
            "Observaciones",
            placeholder="Información adicional o fuente de verificación...",
        )

        guardar_nuevo = st.form_submit_button(
            "➕ Agregar institución",
            type="primary",
            use_container_width=True,
        )

        if guardar_nuevo:

            if not nueva_institucion.strip():

                st.error(
                    "Debes ingresar el nombre de la institución."
                )

            elif nuevo_correo.strip() and not correo_valido(
                nuevo_correo
            ):

                st.error(
                    "El correo no tiene un formato válido. "
                    "Corrígelo o deja el campo vacío."
                )

            else:

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
                        "Esta institución ya está registrada "
                        "en ese municipio."
                    )

                else:

                    nuevo_registro = {
                        "Institución": nueva_institucion.strip(),
                        "Tipo": nuevo_tipo,
                        "Municipio": nuevo_municipio,
                        "Correo": nuevo_correo.strip(),
                        "Áreas": "; ".join(nuevas_areas),
                        "Enfoque": nuevo_enfoque.strip(),
                        "Estado": nuevo_estado,
                        "Fecha de contacto": "",
                        "Observaciones": nuevas_observaciones.strip(),
                    }

                    st.session_state.directorio = pd.concat(
                        [
                            actual,
                            pd.DataFrame([nuevo_registro]),
                        ],
                        ignore_index=True,
                    )

                    st.session_state.busqueda_realizada = False
                    st.session_state.resultados_busqueda = None

                    st.success(
                        "Institución agregada correctamente."
                    )

                    st.rerun()

    st.divider()

    # -----------------------------------------------------
    # EDITAR DIRECTORIO
    # -----------------------------------------------------

    st.markdown("#### Editar registros")

    st.caption(
        "Modifica los campos directamente en la tabla. "
        "Después presiona Guardar cambios."
    )

    editado = st.data_editor(
        st.session_state.directorio,
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
        key="tabla_editable",
        column_config={
            "Institución": st.column_config.TextColumn(
                "Institución",
                required=True,
            ),
            "Tipo": st.column_config.SelectboxColumn(
                "Tipo",
                options=TIPOS,
            ),
            "Municipio": st.column_config.SelectboxColumn(
                "Municipio",
                options=MUNICIPIOS,
            ),
            "Correo": st.column_config.TextColumn(
                "Correo",
            ),
            "Áreas": st.column_config.TextColumn(
                "Áreas separadas por punto y coma",
            ),
            "Estado": st.column_config.SelectboxColumn(
                "Estado",
                options=ESTADOS,
            ),
        },
    )

    if st.button(
        "💾 Guardar cambios",
        type="primary",
        key="guardar_edicion",
    ):

        editado = preparar_directorio(editado)

        editado = editado[
            editado["Institución"].str.strip() != ""
        ]

        editado["_clave"] = (
            editado["Institución"].map(normalizar)
            + "|"
            + editado["Municipio"].map(normalizar)
        )

        duplicados = editado["_clave"].duplicated(keep=False)

        if duplicados.any():

            st.error(
                "Hay instituciones duplicadas en el mismo municipio. "
                "Corrige los registros antes de guardar."
            )

        else:

            editado = editado.drop(columns="_clave")

            correos_incorrectos = editado[
                editado["Correo"].str.strip().ne("")
                & ~editado["Correo"].apply(correo_valido)
            ]

            if not correos_incorrectos.empty:

                st.error(
                    "Hay correos con formato inválido. "
                    "Corrígelos antes de guardar."
                )

            else:

                st.session_state.directorio = editado.reset_index(
                    drop=True
                )

                st.session_state.busqueda_realizada = False
                st.session_state.resultados_busqueda = None

                st.success("Directorio actualizado.")

                st.rerun()

    st.divider()

    # -----------------------------------------------------
    # EXPORTAR DIRECTORIO
    # -----------------------------------------------------

    st.download_button(
        "⬇️ Descargar directorio completo",
        data=exportar_csv(st.session_state.directorio),
        file_name="directorio_instituciones.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# PESTAÑA 3: SEGUIMIENTO
# =========================================================

with tab_seguimiento:

    st.subheader("Seguimiento de oportunidades")

    seguimiento = st.session_state.directorio.copy()

    total = len(seguimiento)

    pendientes = int(
        seguimiento["Estado"].eq("Pendiente").sum()
    )

    contactos = int(
        seguimiento["Estado"].eq("Correo enviado").sum()
    )

    entrevistas = int(
        seguimiento["Estado"].eq("Entrevista").sum()
    )

    contratados = int(
        seguimiento["Estado"].eq("Contratado").sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Instituciones", total)
    c2.metric("Pendientes", pendientes)
    c3.metric("Entrevistas", entrevistas)
    c4.metric("Contrataciones", contratados)

    st.divider()

    st.markdown("#### Resumen por estado")

    if not seguimiento.empty:

        resumen = (
            seguimiento["Estado"]
            .value_counts()
            .rename_axis("Estado")
            .reset_index(name="Cantidad")
        )

        st.bar_chart(
            resumen.set_index("Estado")
        )

        st.markdown("#### Historial de oportunidades")

        st.dataframe(
            seguimiento[
                [
                    "Institución",
                    "Municipio",
                    "Tipo",
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
            "Todavía no hay instituciones registradas "
            "para realizar el seguimiento."
        )

    st.download_button(
        "⬇️ Descargar seguimiento CSV",
        data=exportar_csv(seguimiento),
        file_name="seguimiento_oportunidades.csv",
        mime="text/csv",
    )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "Buscador de Instituciones Educativas · Valle de Aburrá. "
    "Las instituciones, sus contactos y las vacantes deben verificarse "
    "por medio de fuentes oficiales."
)
