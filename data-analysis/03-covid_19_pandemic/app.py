import sqlite3
import pandas as pd
import gradio as gr
import plotly.graph_objects as go
import os

# ========== 讀取資料 ==========
connection = sqlite3.connect("data/covid_19.db")
daily_report = pd.read_sql("""SELECT * FROM daily_report;""", con=connection)
time_series = pd.read_sql("""SELECT * FROM time_series;""", con=connection)
connection.close()

# ========== 計算統計數字（累計確診/死亡/疫苗接種） ==========
total_cases = daily_report["confirmed"].sum()
total_deaths = daily_report["deaths"].sum()
latest_time_series = time_series[time_series["reported_on"] == "2023-03-09"]
total_vaccinated = latest_time_series["doses_administered"].sum()

# 依國家加總確診數並排序，取前30個國家作為地圖預設顯示
sum_confirmed_by_country = daily_report.groupby("country")["confirmed"].sum().sort_values(ascending=False)
top_confirmed = sum_confirmed_by_country.index[:30].to_list()
time_series["reported_on"] = pd.to_datetime(time_series["reported_on"])

 
# ========== 依選定國家，繪製散佈點地圖（scattermapbox） ==========
def filter_global_map(country_names):
    filtered_daily_report = daily_report[daily_report["country"].isin(country_names)]

    countries = filtered_daily_report["country"].values
    provinces = filtered_daily_report["province"].values
    counties = filtered_daily_report["county"].values
    confirmed = filtered_daily_report["confirmed"].values
    deaths = filtered_daily_report["deaths"].values

    # 依地區程度（縣市/省州/國家）組合懸停顯示資訊（位置+確診+死亡數）
    information_when_hovered = []
    information_when_hovered = []
    for country, province, county, c, d in zip(countries, provinces, counties, confirmed, deaths):
        if county is not None:
            marker_information = [(country, province, county), c, d]
        elif province is not None:
            marker_information = [(country, province), c, d]
        else:
            marker_information = [country, c, d]
        information_when_hovered.append(marker_information)

    # 泡泡大小與顏色皆對應確診數
    fig = go.Figure(
        go.Scattermap(
            lat=filtered_daily_report["latitude"],
            lon=filtered_daily_report["longitude"],
            customdata=information_when_hovered,   # 綁定每個點對應的懸停資訊
            hoverinfo="text", 
            hovertemplate="Location: %{customdata[0]}<br>Confirmed: %{customdata[1]}<br>Deaths: %{customdata[2]}",  # 自訂懸停顯示格式
            mode="markers",
            marker={
                "size": filtered_daily_report["confirmed"],
                "color": filtered_daily_report["confirmed"],
                "sizemin": 2,             
                "sizeref": filtered_daily_report["confirmed"].max() / 2500,  # 泡泡尺寸縮放比例
                "sizemode": "area"                                 
            }
        )
    )

    # 底圖樣式與初始置中位置（台灣）
    fig.update_layout(
        map_style="open-street-map",
        map=dict(
            zoom=2,
            center=go.layout.map.Center(lat=23.7, lon=121.0)  # 改成台灣座標
        )
    )
    return fig

# ========== 建立 gradio 地圖 介面 ==========
with gr.Blocks() as global_map_tab:
    gr.Markdown("""# Covid 19 Global Map""")
    with gr.Row():
        gr.Label(f"{total_cases:,}", label="Total cases")
        gr.Label(f"{total_deaths:,}", label="Total deaths")
        gr.Label(f"{total_vaccinated:,}", label="Total doses administered")
    with gr.Column():
        countries = gr.Dropdown(choices=daily_report["country"].unique().tolist(),
                                label="Select countries:", multiselect=True, 
                                value=top_confirmed,
                                info="點選標籤旁空白處展開選單")
        btn = gr.Button(value="Update")
        global_map = gr.Plot()

    # 頁面載入與點擊按鈕時，都重新繪製地圖
    global_map_tab.load(fn=filter_global_map,
              inputs=countries,
              outputs=global_map)
    btn.click(fn=filter_global_map,
              inputs=countries,
              outputs=global_map)


# ========== 建立折線圖介面 ==========
with gr.Blocks() as country_time_series_tab:
    gr.Markdown("""# Covid 19 Country Time Series""")
    with gr.Row():
        country = gr.Dropdown(choices=time_series["country"].unique().tolist(), value="Taiwan*",
                              label="Select a country:")
     # 三張折線圖，初始先顯示全部資料，之後依選定國家更新
    plt_confirmed = gr.LinePlot(time_series.head(), x="reported_on", y="confirmed")
    plt_deaths = gr.LinePlot(time_series.head(), x="reported_on", y="deaths")
    plt_doses = gr.LinePlot(time_series.head(), x="reported_on", y="doses_administered")

    @gr.on(inputs=country, outputs=plt_doses)
    @gr.on(inputs=country, outputs=plt_deaths)
    @gr.on(inputs=country, outputs=plt_confirmed)
    def filter_time_series(country):
        """依選定國家篩選時間序列資料。"""
        filtered_df = time_series[time_series["country"] == country]
        return filtered_df

    # 頁面載入時，依預設國家（Taiwan*）繪製三張圖
    country_time_series_tab.load(
        fn=filter_time_series,
        inputs=country,
        outputs=plt_confirmed)
    country_time_series_tab.load(
        fn=filter_time_series,
        inputs=country,
        outputs=plt_deaths)
    country_time_series_tab.load(
        fn=filter_time_series,
        inputs=country,
        outputs=plt_doses)

# ========== 整合成分頁介面 ==========
demo = gr.TabbedInterface([global_map_tab, country_time_series_tab], ["Global Map", "Country Time Series"])
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

# demo.launch()


