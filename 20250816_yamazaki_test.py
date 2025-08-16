import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium import IFrame

import os.path as osp 

# データの読み込み
df = pd.read_csv('20250816_yamazaki_test.csv')

# 地図オブジェクトを作成
m = folium.Map(
    location=[35.59299166666667,139.65553333333335],
    zoom_start=14.5
)

# 各画像にマーカーを追加
# `CircleMarker`を使って、撮影位置に円形のマーカーを配置します。

html = '<img src="https://www.photolibrary.jp/mhd6/img406/450-20150801234758103726.jpg" width="320" >'
# iframe = IFrame(html)
# result = s.replace('　', '').

for i in range(len(df)):
    img_path = df.iloc[i]['image_path']
    b = osp.basename(img_path).replace(' ', '%20')
    # ex. http://localhost:8001/images_yamazaki/2025-08-15%2016.25.18.jpg 
    html = f'<img src="http://localhost:8001/images_yamazaki/{b}" width="320" >'
    folium.CircleMarker(
        location=[df.iloc[i]['GPSLatitude'], df.iloc[i]['GPSLongitude']],  # マーカーの緯度経度を設定
#        radius=df.iloc[i]['daily_users'] / 10000,  # 利用者数に応じて円の大きさを変える
        # popup=f"{df.iloc[i]['station_name']}: {df.iloc[i]['daily_users']}",  # マーカーをクリックしたときに表示されるポップアップを設定
        popup=html,
        tooltip="latlong: {}, {} ¥n  Date: {}".format(df.iloc[i]['GPSLatitude'], df.iloc[i]['GPSLongitude'], df.iloc[i]['GPSDate']),  # マーカーにマウスオーバーしたときに表示されるツールチップを設定
        color="blue",  # マーカーの枠線の色を設定
        fill=True,  # マーカーを塗りつぶすかどうかを設定
        fill_color="blue"  # マーカーの塗りつぶしの色を設定
    ).add_to(m)  # 作成したマーカーを地図に追加

# Streamlitに地図を表示
st.title("Yamazaki Photo Locations")
st_folium(m,use_container_width=True)