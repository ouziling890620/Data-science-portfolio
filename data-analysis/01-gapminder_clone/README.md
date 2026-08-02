# 練習專案一: 兩百個國家、兩百年、四分鐘

## 簡介

本專題復刻了 Hans Rosling 經典的資料視覺化作品
[200 Countries, 200 Years, 4 Minutes](https://youtu.be/jbkSRLYSojo?si=5WkjOoiU_IPuKGsR)，
呈現兩百年間，各國人均GDP與預期壽命如何隨時間演變。

透過這個專題，使用 `pandas` 與 `sqlite3` ，練習了從原始 CSV 資料建立 SQLite 資料庫、
以 SQL JOIN 整併多張資料表，並比較 `matplotlib`（靜態驗證）
與 `plotly.express`（互動式成品）在資料視覺化上的差異與應用時機。

## 資料來源

[Gapminder Foundation](https://www.gapminder.org/data/)，資料分為：
- `datapoints`：隨時間變化的數值（人均GDP、預期壽命、人口）
- `entities`：固定不變的屬性（國家名稱、所屬洲別） 

## 資料需求對照

| 視覺元素 | 對應資料 |
|---|---|
| X 軸 | 人均 GDP |
| Y 軸 | 預期壽命 |
| 顏色 | 洲別 |
| 大小 | 人口數 |
| 時間軸 | 年份 |


## 流程

1. **建立資料庫**：讀取四份 Gapminder 原始資料（人均GDP、預期壽命、人口、地理資訊），存入 SQLite 資料庫，並以 SQL JOIN 建立整合檢視表 `plotting`
2. **概念驗證**：用 matplotlib 繪製單一年份的靜態散佈圖，確認呈現邏輯正確
3. **產出成品**：用 plotly.express 繪製整合五個維度（GDP、壽命、洲別、人口、年份）的互動式動畫散佈圖

## 如何重現

- 安裝 `Miniconda`
- 依據 `environment.yml` 建立環境： 

```bash
conda env create -f environment.yml`
```

- 將 `data/` 資料夾中的四個 CSV 檔案置放於工作目錄中的 `data/` 資料夾。
- 啟動環境並執行 `python create_gapminder_db.py` 就能在 `data/` 資料夾中建立 `gapminder.db`
- 啟動環境並執行 `python plot_with_px.py` 就能生成 `gapminder_clone.html`

## 檔案結構
```
01-gapminder_clone/
├── data/ # 原始 CSV 與 gapminder.db
├── create_gapminder_db.py # 建立資料庫與檢視表
├── proof_of_concept.py # matplotlib 概念驗證
├── plot_with_px.py # plotly.express 產出成品
└── gapminder_clone.html # 最終互動式成品
```

## 快速連結

- [互動式瀏覽](https://ouziling890620.github.io/Data-science-portfolio/data-analysis/01-gapminder_clone/gapminder_clone.html)