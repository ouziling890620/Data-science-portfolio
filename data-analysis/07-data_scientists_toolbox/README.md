# 練習專案七: 資料科學家的工具箱

## 目前狀態

本專題已完成資料處理與六張圖表產出，
分析結果的文字說明尚在整理中。

## 簡介

透過 2020-2022 年 [kaggle.com](https://www.kaggle.com/) 舉辦的
Kaggle Machine Learning and Data Science Survey 普查問卷進行縱貫研究，
針對三個資料科學初學者常見的問題進行探索性分析：

1. 從事資料科學工作的職缺抬頭（title）有哪些？
2. 從事資料科學工作的日常內容是什麼？
3. 想要從事資料科學工作，需要具備哪些技能與知識？

練習了處理跨年度、欄位命名邏輯不一致的原始資料，將寬格式問卷轉為長格式，
並以 SQL JOIN 建立彙總檢視表，
最後用 `matplotlib` 進行跨年份比較視覺化。

## 資料來源

- [2020](https://www.kaggle.com/competitions/kaggle-survey-2020) /
  [2021](https://www.kaggle.com/competitions/kaggle-survey-2021) /
  [2022](https://www.kaggle.com/competitions/kaggle-survey-2022) Kaggle ML & DS Survey
- 選用 2020-2022 三年資料，因題目固定、適合縱貫比較，且該調查已於 2023 年停辦

## 分析主題對應題號

| 分析主題 | 2020 | 2021 | 2022 |
|---|---|---|---|
| 職缺抬頭 | Q5 | Q5 | Q23 |
| 日常工作內容 | Q23 | Q24 | Q28 |
| 常用程式語言 | Q7 | Q7 | Q12 |
| 常用大數據工具 | Q29A | Q32A | Q35 |
| 常用視覺化工具 | Q14 | Q14 | Q15 |
| 常用ML演算法 | Q17 | Q17 | Q18 |

## 分析結果

| 主題 | 主要發現 |
|---|---|
| 職缺抬頭 | Data Scientist、Data Analyst、Software Engineer 為前幾大職稱 |
| 日常工作 | 「分析資料以影響產品或商業決策」為最主要工作內容 |
| 程式語言 | Python、SQL 為最常用 |
| 資料庫 | MySQL、PostgreSQL 使用率較高 |
| 視覺化工具 | Matplotlib、Seaborn 最常見 |
| ML演算法 | 線性/邏輯回歸、決策樹/隨機森林最普遍 |

## 如何重現

```bash
conda env create -f environment.yml
python create_kaggle_survey_db.py             # 建立 kaggle_survey.db
python create_longitudinal_analysis_plots.py  # 輸出六張長條圖
```

三份問卷 CSV 需事先置於 `data/` 資料夾。

## 檔案結構
```
├── data/ # 原始 CSV 與 kaggle_survey.db
├── create_kaggle_survey_db.py # 建立資料庫與彙總檢視表
├── create_longitudinal_analysis_plots.py # 產出六張跨年份長條圖
└── *.png # 各主題的最終成品圖
```
## 快速連結
- [成品圖片：職缺抬頭](./data_science_job_titles.png)（其餘圖片位於本資料夾）

