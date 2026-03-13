"""
Componente de tabela reutilizável com export
"""

import streamlit as st
import pandas as pd
from io import BytesIO


def render_data_table(
    df: pd.DataFrame,
    titulo: str = "Dados",
    exportar_para: list = None,
    altura_max: int = 500,
    mostrar_index: bool = False,
):
    """
    Renderiza uma tabela de dados com opções de export.

    Args:
        df (pd.DataFrame): DataFrame a exibir
        titulo (str): Título da tabela
        exportar_para (list): Formatos de export ['csv', 'excel']
        altura_max (int): Altura máxima da tabela em pixels
        mostrar_index (bool): Mostrar índice da tabela
    """
    if exportar_para is None:
        exportar_para = ["csv", "excel"]

    # Header com título e botões de export
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader(titulo)

    with col2:
        if df.empty:
            st.caption("Sem dados")
        else:
            st.caption(f"📊 {len(df)} linha(s)")

    # Botões de export
    with col3:
        if not df.empty:
            # Export CSV
            if "csv" in exportar_para:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 CSV",
                    data=csv,
                    file_name=f"{titulo.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            # Export Excel
            if "excel" in exportar_para:
                buffer = BytesIO()

                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name="Dados", index=False)

                buffer.seek(0)

                st.download_button(
                    label="📊 Excel",
                    data=buffer,
                    file_name=f"{titulo.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

    # Renderizar tabela
    if df.empty:
        st.warning("❌ Nenhum dado para exibir")
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=not mostrar_index,
            height=altura_max,
        )


def render_data_table_with_search(
    df: pd.DataFrame,
    titulo: str = "Dados",
    coluna_busca: str = None,
    exportar_para: list = None,
):
    """
    Renderiza tabela com busca de texto inline.

    Args:
        df (pd.DataFrame): DataFrame a exibir
        titulo (str): Título da tabela
        coluna_busca (str): Nome da coluna para busca (default: primeira coluna)
        exportar_para (list): Formatos de export
    """
    if exportar_para is None:
        exportar_para = ["csv", "excel"]

    if df.empty:
        st.warning("❌ Sem dados")
        return

    # Definir coluna de busca
    if coluna_busca is None or coluna_busca not in df.columns:
        coluna_busca = df.columns[0]

    # Input de busca
    col1, col2 = st.columns([3, 1])

    with col1:
        termo_busca = st.text_input(
            f"🔎 Buscar em {coluna_busca}...",
            key=f"busca_{titulo}",
        )

    with col2:
        st.caption(f"📊 {len(df)} resultado(s)")

    # Filtrar DataFrame
    if termo_busca:
        df_filtrado = df[
            df[coluna_busca].astype(str).str.contains(termo_busca, case=False, na=False)
        ]
    else:
        df_filtrado = df

    # Renderizar tabela
    render_data_table(
        df_filtrado,
        titulo=titulo,
        exportar_para=exportar_para,
        altura_max=500,
    )
