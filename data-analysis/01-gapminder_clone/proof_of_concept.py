"""
proof_of_concept.py — 讀取 gapminder.db 的 plotting 檢視表，驗證資料讀取是否正常。
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting""", con=connection)
connection.close()


# ========== 繪製分布圖及動畫 ==========
fig, ax = plt.subplots()
def update_plot(year_to_plot: int): #繪製的年份
    ax.clear()
    subset_df = plotting_df[plotting_df["dt_year"] == year_to_plot]
    gdp_pcap = subset_df["gdp_per_capita"].values   # X軸：人均GDP
    lex = subset_df["life_expectancy"].values       # Y軸：預期壽命
    cont = subset_df["continent"].values            # 用來決定散佈圖顏色的洲別
    color_map = {                                   # 各洲別對應的顏色
        "asia": "r",
        "africa": "g",
        "europe": "b",
        "americas": "c"
    }
    for xi, yi, ci in zip(gdp_pcap, lex, cont):
        ax.scatter(xi, yi, color=color_map[ci])
    ax.set_title(f"The world in {year_to_plot}")
    ax.set_xlabel("GDP Per Capita(in USD)")
    ax.set_ylabel("Life Expectancy")
    ax.set_ylim(20, 100)
    ax.set_xlim(0, 100000)
    plt.show()

ani = animation.FuncAnimation(fig, func=update_plot, frames=range(2000, 2024), interval=10)
ani.save("animation.gif", fps=10)