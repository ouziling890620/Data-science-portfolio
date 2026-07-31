import sqlite3
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd

# 讀取三張資料表
connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql("""SELECT * FROM cities;""", con=connection)
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""", con=connection)
troop_df = pd.read_sql("""SELECT * FROM troops;""", con=connection)
connection.close()

# ========== 準備繪圖資料 ==========
loncs = city_df["lonc"].values         # 城市經度
latcs = city_df["latc"].values         # 城市緯度
city_names = city_df["city"].values    # 城市名稱

rows = troop_df.shape[0]
lonps = troop_df["lonp"].values        # 軍隊位置經度
latps = troop_df["latp"].values        # 軍隊位置緯度
survivals = troop_df["surviv"].values  # 存活人數
directions = troop_df["direc"].values  # 方向（A=進攻, R=撤退）

# 「列氏」轉「攝氏」溫度：Celsius(°C) = Réaumur(°Ré) × 5/4
temp_celsius = (temperature_df["temp"] * 5/4).astype(int)
# 組合成「溫度+日期」的標註文字，如 "0°C Oct 18"
annotations = temp_celsius.astype(str).str.cat(temperature_df["date"], sep="°C ")
lonts = temperature_df["lont"].values  # 溫度記錄點經度

# ========== 建立畫布：上層地圖區、下層氣溫區 ==========
fig, axes = plt.subplots(nrows=2, figsize=(25, 12), gridspec_kw={"height_ratios": [4, 1]})

# ========== 在第零個軸物件地圖底圖 ==========
# Lambert Conformal 投影，涵蓋東歐地區（拿破崙戰役範圍）
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=axes[0])

m.drawcountries()  # 國界
m.drawrivers()     # 河流
m.drawmeridians(range(23, 56, 2), labels=[False, False, False, True])# 經線，標籤只顯示右側
m.drawparallels(range(54, 58), labels=[True, False, False, False])# 緯線，標籤只顯示左側

# ========== 疊加城市標註 ==========
x, y = m(loncs, latcs)  # 城市經緯度轉換為地圖投影座標
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name, xy=(xi, yi), fontsize=16, zorder=2)

# ========== 疊加軍隊移動路徑 ==========
x, y = m(lonps, latps)  # 軍隊位置經緯度轉換為地圖投影座標
# 逐段繪製軍隊移動路徑：每一段連接相鄰兩個位置點
# 依方向決定顏色：進攻(A)土黃色／撤退(R)黑色
# 粗細：存活人數（縮放1/10000）
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"

    start_stop_lons = (x[i], x[i + 1])
    start_stop_lats = (y[i], y[i + 1])
    line_width = survivals[i]
    m.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color, zorder=1)



# ========== 在第一個軸物件繪製氣溫折線圖 ==========
axes[1].plot(lonts, temp_celsius, linestyle="dashed", color="black")

# 在每個溫度點旁標註「溫度+日期」文字
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont - 0.3, temp_c - 7), fontsize=16)
axes[1].set_ylim(-50, 10)
# 隱藏邊框
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)

axes[1].grid(True, which="major", axis="both")  # 顯示格線
axes[1].set_xticklabels([])  
axes[1].set_yticklabels([]) 

# ========== 輸出成品 ==========
axes[0].set_title("Napoleon's disastrous Russian campaign of 1812", loc="left", fontsize=30)
plt.tight_layout()
fig.savefig("minard_clone.png")

