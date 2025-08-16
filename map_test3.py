import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium import IFrame

# データの読み込み
# 今回はサンプルデータとして、駅名、緯度、経度、1日の利用者数のデータを使います。

df = pd.read_csv('https://raw.githubusercontent.com/JS2IIU-MH/Streamlit_sample_data/refs/heads/main/data/yamanote_line.csv')

# 地図オブジェクトを作成
# 地図の中心は皇居付近に設定し、ズームレベルは11に設定しています。
m = folium.Map(location=[35.6863581,139.7502537], zoom_start=11.5)

# 各駅にマーカーを追加
# `CircleMarker`を使って、駅の位置に円形のマーカーを配置します。
# 円の半径は、駅の利用者数に比例するように設定しています。

html = '<img src="https://www.photolibrary.jp/mhd6/img406/450-20150801234758103726.jpg" width="320" >'
iframe = IFrame(html)

for i in range(len(df)):
    folium.CircleMarker(
        location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],  # マーカーの緯度経度を設定
#        radius=df.iloc[i]['daily_users'] / 10000,  # 利用者数に応じて円の大きさを変える
        # popup=f"{df.iloc[i]['station_name']}: {df.iloc[i]['daily_users']}",  # マーカーをクリックしたときに表示されるポップアップを設定
        popup=html,
        tooltip=df.iloc[i]['station_name'],  # マーカーにマウスオーバーしたときに表示されるツールチップを設定
        color="blue",  # マーカーの枠線の色を設定
        fill=True,  # マーカーを塗りつぶすかどうかを設定
        fill_color="blue"  # マーカーの塗りつぶしの色を設定
    ).add_to(m)  # 作成したマーカーを地図に追加

# Streamlitに地図を表示
st.title("Yamazaki Photo Locations")
st_folium(m,use_container_width=True)