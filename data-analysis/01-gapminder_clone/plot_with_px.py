"""plot_with_px.py — 使用 plotly.express 繪製互動式 Gapminder 動畫散佈圖，
輸出為可拖動時間軸的 HTML 檔案。"""

import sqlite3
import pandas as pd
import plotly.express as px

connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting""", con=connection)
connection.close()

fig = px.scatter(
    plotting_df,
    x="gdp_per_capita",           # X軸：人均GDP
    y="life_expectancy",          # Y軸：預期壽命
    animation_frame="dt_year",    # 時間軸：依年份播放動畫
    animation_group="country_name",  # 動畫播放時，正確追蹤每個國家的點
    size="population",            # 泡泡大小：人口數
    color="continent",            # 顏色：所屬洲別
    hover_name="country_name",    # 滑鼠懸停時顯示國家名稱
    size_max=100,                 # 泡泡最大尺寸上限
    range_x=[500, 100000],        # X軸顯示範圍
    range_y=[20, 90],             # Y軸顯示範圍
    log_x=True,                   # X軸取對數，避免GDP數值分布過於歪斜
    title="Gapminder Clone 1800-2023"
)

fig.write_html("gapminder_clone.html", auto_open=True)  # 輸出成互動式HTML，並自動開啟