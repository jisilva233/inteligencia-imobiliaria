"""
Helpers para manipulação de mapas Mapbox com pydeck
"""

import pandas as pd
import pydeck as pdk
from config import settings


def create_mapbox_layer(
    df: pd.DataFrame,
    latitude_col: str = "latitude",
    longitude_col: str = "longitude",
    color_col: str = None,
    size_col: str = None,
    label_col: str = None,
    color_range: tuple = (0, 255, 0),  # RGB padrão: verde
) -> pdk.Layer:
    """
    Cria uma ScatterplotLayer para pydeck.

    Args:
        df (pd.DataFrame): DataFrame com dados de pontos
        latitude_col (str): Nome da coluna de latitude
        longitude_col (str): Nome da coluna de longitude
        color_col (str): Coluna para cor dos pontos (será normalizada a 0-255)
        size_col (str): Coluna para tamanho dos pontos
        label_col (str): Coluna para labels/tooltips
        color_range (tuple): Cor RGB padrão (R, G, B)

    Returns:
        pdk.Layer: Layer configurado para o mapa
    """
    # Filtrar apenas linhas com lat/lon válidos
    df_filtered = df.dropna(subset=[latitude_col, longitude_col]).copy()

    if df_filtered.empty:
        # Retornar layer vazio
        return pdk.Layer(
            "ScatterplotLayer",
            data=[],
            get_position=[0, 0],
            get_fill_color=[0, 0, 0],
            get_radius=100,
        )

    # Normalizar cores se color_col foi fornecido
    if color_col and color_col in df_filtered.columns:
        col_min = df_filtered[color_col].min()
        col_max = df_filtered[color_col].max()

        if col_max > col_min:
            df_filtered["_color_normalized"] = (
                (df_filtered[color_col] - col_min) / (col_max - col_min) * 255
            )
        else:
            df_filtered["_color_normalized"] = 128

        # Criar vetor de cores: gradiente de vermelho para verde
        get_fill_color = [
            "case",
            ["<", ["_color_normalized"], 85],  # < 1/3
            [255, 0, 0],  # Vermelho
            ["<", ["_color_normalized"], 170],  # < 2/3
            [255, 255, 0],  # Amarelo
            [0, 255, 0],  # Verde
        ]
    else:
        # Cor sólida
        get_fill_color = list(color_range)

    # Tamanho dos pontos
    if size_col and size_col in df_filtered.columns:
        # Normalizar tamanho entre 100 e 1000 metros
        size_min = df_filtered[size_col].min()
        size_max = df_filtered[size_col].max()

        if size_max > size_min:
            df_filtered["_size_normalized"] = (
                (df_filtered[size_col] - size_min) / (size_max - size_min) * 900 + 100
            )
        else:
            df_filtered["_size_normalized"] = 500

        get_radius = ["_size_normalized"]
    else:
        get_radius = 300  # Tamanho fixo

    return pdk.Layer(
        "ScatterplotLayer",
        data=df_filtered,
        get_position=[longitude_col, latitude_col],
        get_fill_color=get_fill_color,
        get_radius=get_radius,
        pickable=True,
        opacity=0.8,
        stroked=True,
        fill_color=[0, 0, 0],
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2,
    )


def create_map_view(
    latitude: float,
    longitude: float,
    zoom: int = 12,
    pitch: int = 0,
    bearing: int = 0,
) -> pdk.ViewState:
    """
    Cria ViewState para centralizar o mapa em um ponto.

    Args:
        latitude (float): Latitude central
        longitude (float): Longitude central
        zoom (int): Nível de zoom (0-20)
        pitch (int): Inclinação do mapa em graus
        bearing (int): Rotação do mapa em graus

    Returns:
        pdk.ViewState: ViewState configurado
    """
    return pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=zoom,
        pitch=pitch,
        bearing=bearing,
    )


def get_city_center(cidade: str) -> dict:
    """
    Retorna latitude/longitude do centro da cidade.
    Dados hardcoded para cidades principais.

    Args:
        cidade (str): Nome da cidade

    Returns:
        dict: {'lat': float, 'lon': float, 'zoom': int}
    """
    centers = {
        "São Paulo": {"lat": -23.5505, "lon": -46.6333, "zoom": 11},
        "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729, "zoom": 11},
        "Belo Horizonte": {"lat": -19.9203, "lon": -43.9345, "zoom": 11},
        "Brasília": {"lat": -15.8267, "lon": -47.8822, "zoom": 11},
        "Salvador": {"lat": -12.9714, "lon": -38.5014, "zoom": 11},
    }

    return centers.get(cidade, {"lat": -15.0, "lon": -50.0, "zoom": 4})


def create_map_with_layer(
    df: pd.DataFrame,
    layer: pdk.Layer,
    cidade: str = None,
    title: str = "Mapa Interativo",
) -> pdk.Deck:
    """
    Cria um mapa Deck.gl completo com layer.

    Args:
        df (pd.DataFrame): DataFrame com dados
        layer (pdk.Layer): Layer a renderizar
        cidade (str): Cidade para centralizar mapa
        title (str): Título do mapa

    Returns:
        pdk.Deck: Mapa configurado
    """
    # Obter centro da cidade ou usar valores padrão de df
    if cidade:
        center = get_city_center(cidade)
        view_state = create_map_view(
            latitude=center["lat"],
            longitude=center["lon"],
            zoom=center["zoom"],
        )
    else:
        # Usar centro dos dados
        if not df.empty and "latitude" in df.columns and "longitude" in df.columns:
            lat_mean = df["latitude"].mean()
            lon_mean = df["longitude"].mean()
            view_state = create_map_view(latitude=lat_mean, longitude=lon_mean, zoom=12)
        else:
            # Brasil inteiro
            view_state = create_map_view(latitude=-15.0, longitude=-50.0, zoom=4)

    return pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=view_state,
        layers=[layer],
        tooltip={
            "html": "<b>{nome}</b><br/>Score: {score_oportunidade}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white",
                "fontSize": "12px",
                "padding": "10px",
            },
        },
    )


def format_map_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara DataFrame para renderização em mapa.
    Remove NaNs e adiciona colunas de cor/tamanho se necessário.

    Args:
        df (pd.DataFrame): DataFrame original

    Returns:
        pd.DataFrame: DataFrame formatado para mapa
    """
    df_copy = df.copy()

    # Remover linhas com lat/lon nulos
    df_copy = df_copy.dropna(subset=["latitude", "longitude"])

    # Preencher colunas de score com 5.0 se não existir
    if "score_oportunidade" not in df_copy.columns:
        df_copy["score_oportunidade"] = 5.0

    # Garantir que lat/lon são floats
    df_copy["latitude"] = pd.to_numeric(df_copy["latitude"], errors="coerce")
    df_copy["longitude"] = pd.to_numeric(df_copy["longitude"], errors="coerce")

    return df_copy
