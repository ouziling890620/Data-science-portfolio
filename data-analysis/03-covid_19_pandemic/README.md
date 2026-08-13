# 練習專案三: 大疫世代

## 簡介

本專題透過 CSSE at Johns Hopkins University 的
[csse_covid_19_data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)，
使用 2020-01-22 至 2023-03-09（資料停止更新前最後一天）期間的每日報告與
時間序列資料，製作出頁籤式疫情儀表板，呈現全球COVID-19確診、死亡與疫苗接種概況。

透過這個專題，練習了處理寬轉長格式的時間序列資料、建立SQLite資料庫，
並以 `gradio` 建立含地理散佈地圖與互動篩選折線圖的儀表板。

## 資料來源

來自 CSSE at Johns Hopkins University：
- [csse_covid_19_daily_reports](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)
- [csse_covid_19_time_series](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
- [time_series_covid19_vaccine_global](https://github.com/govex/COVID-19/blob/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv)


## 如何重現

```bash
conda env create -f environment.yml
python create_covid_19_db.py   # 建立 covid_19.db
python app.py   # 前往 http://127.0.0.1:7860 瀏覽成品
```

4個原始CSV需事先置於 `data/` 資料夾。

## 檔案結構
```
05-covid_19_pandemic/
├── data/ # 原始 CSV 與 covid_19.db
├── create_covid_19_db.py # 建立資料庫
└── app.py # gradio 疫情儀表板
```

## 快速連結

- [建立資料庫程式碼](./create_covid_19_db.py)
- [gradio 儀表板程式碼](./app.py)
- [線上互動瀏覽（Railway部署）](https://covid-19-dashboard-production.up.railway.app)