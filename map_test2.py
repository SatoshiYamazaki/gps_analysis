import numpy as np
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile

st.set_page_config(
    page_title="st.map",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_data(csv_file: UploadedFile) -> pd.DataFrame:
    """Read CSV file

    Args:
        csv_file (UploadedFile): Up file

    Returns:
        pd.DataFrame: DataFrame
    """
    try:
        return pd.read_csv(csv_file)
    except UnicodeDecodeError:
        st.error("ファイルのエンコードは Utf-8 のみ有効です。")
        st.stop()


with st.expander("README"):
    st.info(
        """
        1. ファイルを読み込む
        1. 「データフレームの編集」を開いて、緯度・経度のあるカラム名を「lat」「lon」に変更
        1. 「Generate new points」ボタンをクリック
        1. Separate ヘッダーのパラメーターを変更
        1. 「Update map」ボタンをクリック
        """
    )

upload_file: UploadedFile | None = st.file_uploader("Choose a file")

if upload_file is not None:
    df: pd.DataFrame = get_data(upload_file)

    if not ("lat" in df.columns and "lon" in df.columns):
        with st.expander("データフレームの編集"):
            st.info(
                "緯度・経度のあるカラム名を「lat」「lon」に書き換えると、表示できます。"
            )
            st.dataframe(df)

            # カラム名の編集フィールド
            df.columns = [
                st.text_input(f"{col} の新しい名前", value=col) for col in df.columns
            ]

if st.button("Generate new points", type="primary"):
    st.session_state.df = df

if "df" not in st.session_state:
    st.stop()

if not ("lat" in st.session_state.df.columns and "lon" in st.session_state.df.columns):
    st.error("カラム名に「lat」「lon」が存在しません。")
    st.info("「データフレームの編集」を開いてカラム名を変更してください。")
    st.stop()

df = st.session_state.df

def create_team_row(
    team_name: str, default_color: str, default_opacity: int, default_size: int
) -> tuple[str, int, int]:
    """
    st.map の設定アイテム

    Args:
        team_name (str): チーム名
        default_color (str): 既定色
        default_opacity (int): 透明度
        default_size (int): サイズ

    Returns:
        tuple[str, Any, Any]: カラー、透明度、サイズ
    """
    row: list[DeltaGenerator] = st.columns([1, 2, 2])
    return (
        row[0].color_picker(team_name, default_color),
        row[1].slider("Opacity", 20, 100, default_opacity, label_visibility="hidden"),
        row[2].slider(
            "Size",
            50,
            200,
            default_size,
            step=10,
            label_visibility="hidden",
        ),
    )

with st.expander("Team Details"):
    with st.form("map_form"):
        header: list[DeltaGenerator] = st.columns([1, 2, 2])
        header[0].subheader("Color")
        header[1].subheader("Opacity")
        header[2].subheader("Size")

        colorA, opacityA, sizeA = create_team_row("Team A", "#fff0f5", 35, 100)
        colorB, opacityB, sizeB = create_team_row("Team B", "#66cdaa", 50, 150)
        colorC, opacityC, sizeC = create_team_row("Team C", "#800000", 60, 200)

        header = st.columns([2, 3])
        header[0].subheader("Separate")

        row4: list[DeltaGenerator] = st.columns([2, 3])
        target: str | None = row4[0].selectbox(
            "Divide into teams",
            [col for col in df.columns if "数" in col],
            # 値の型で判断するなら
            # [col for col in df.columns if df[col].dtype == "int64"],
            help="数値でチームを分けます。A: 0, B: 1, C: more",
        )

        st.form_submit_button("Update map", type="primary")

    alphaA = int(opacityA * 255 / 100)
    alphaB = int(opacityB * 255 / 100)
    alphaC = int(opacityC * 255 / 100)

    df["color"] = np.where(
        df[target] == 0,
        colorA + f"{alphaA:02x}",
        np.where(df[target] == 1, colorB + f"{alphaB:02x}", colorC + f"{alphaC:02x}"),
    )

    df["size"] = np.where(
        df[target] == 0, sizeA, np.where(df[target] == 1, sizeB, sizeC)
    )

if st.button("マップを表示"):
    st.map(df, size="size", color="color")