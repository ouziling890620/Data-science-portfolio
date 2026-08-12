import sqlite3
import pandas as pd
import gradio as gr
import plotly.graph_objects as go

connection = sqlite3.connect("data/covid_19.db")
daily_report = pd.read_sql("""SELECT * FROM daily_report;""", con=connection)
connection.close()

# ========== 顯示散佈點地圖（scattermapbox） ==========
# 用經緯度在地圖上畫散佈點，泡泡大小與顏色皆對應確診數
fig = go.Figure(
    go.Scattermapbox(
        lat=daily_report["latitude"],
        lon=daily_report["longitude"],
        mode="markers",
        marker={
            "size": daily_report["confirmed"],
            "color": daily_report["confirmed"],
            "sizemin": 2,                                      # 泡泡最小尺寸
            "sizeref": daily_report["confirmed"].max() / 2500,  # 泡泡尺寸縮放比例
            "sizemode": "area"                                 # 依面積比例呈現大小差異
        }
    )
)

# 設定地圖底圖樣式、縮放層級與置中位置
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        zoom=2,
        center=go.layout.mapbox.Center(lat=0, lon=0)
    )
)

# 用 gr.Blocks 自由排版：標題文字 + 地圖圖表
with gr.Blocks() as demo:
    gr.Markdown("""# Covid 19 Global Map""")
    gr.Plot(fig)

demo.launch()


