
# =========================================================
# 1. BUSCADOR CON BOTÓN
# =========================================================
with tab_busqueda:
    st.subheader("Buscar instituciones educativas")
    st.write(
        "Selecciona tus criterios de búsqueda y presiona el botón "
        "para consultar las instituciones registradas."
    )

    with st.form("formulario_busqueda"):
        col1, col2, col3 = st.columns(3)

        with col1:
            municipios = st.multiselect(
                "Municipio",
                MUNICIPIOS,
                key="buscar_municipios",
            )

        with col2:
            tipos = st.multiselect(
                "Tipo de institución",
                ["Público", "Privado", "Universidad", "Otro"],
                key="buscar_tipos",
            )

        with col3:
            areas = st.multiselect(
                "Área de interés",
                AREAS,
                key="buscar_areas",
            )

        termino = st.text_input(
            "Palabra clave (opcional)",
            placeholder="Ej.: robótica, diseño, informática...",
        )

        buscar = st.form_submit_button(
            "🔎 Buscar instituciones",
            type="primary",
            use_container_width=True,
        )

    if buscar:
        resultados = st.session_state.directorio.copy()

        # Aplicar filtros solo cuando se seleccionan
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

        st.divider()
        st.subheader("Resultados de la búsqueda")
        st.metric("Instituciones encontradas", len(resultados))

        if resultados.empty:
            st.warning(
                "No se encontraron instituciones con esos criterios. "
                "Prueba con otros filtros o agrega registros al directorio."
            )
        else:
            for _, fila in resultados.iterrows():
                with st.container(border=True):
                    st.markdown(f"### {fila['Institución']}")
                    st.write(f"**Municipio:** {fila['Municipio']}")
                    st.write(f"**Tipo:** {fila['Tipo']}")
                    st.write(f"**Áreas:** {fila['Áreas']}")
                    st.write(f"**Enfoque:** {fila['Enfoque']}")
                    st.write(f"**Estado:** {fila['Estado']}")

                    correo = str(fila["Correo"]).strip()

                    if re.fullmatch(
                        r"[^@\s]+@[^@\s]+\.[^@\s]+",
                        correo,
                    ):
                        st.link_button(
                            "Contactar institución",
                            f"mailto:{correo}",
                        )
    else:
        st.info(
            "Configura los filtros y presiona «Buscar instituciones» "
            "para consultar los resultados."
        )
