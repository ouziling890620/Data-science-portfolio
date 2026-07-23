
# 共享單車需求預測

## 專案說明

本專題參考 [Yeh James 的教學文章](https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC4-2%E8%AC%9B-%E5%85%B1%E4%BA%AB%E5%96%AE%E8%BB%8A%E9%9C%80%E6%B1%82%E9%A0%90%E6%B8%AC-%E5%89%8D17-%E6%8E%92%E5%90%8D-505ed7100825)，
利用基礎的機器學習知識，搭配 Random Forest（隨機森林）演算法，
練習 Kaggle 共享單車租借數量預測競賽的完整流程。

## 資料來源

- [Kaggle: Bike Sharing Demand](https://www.kaggle.com/competitions/bike-sharing-demand/data)
- 使用檔案：`train.csv`、`test.csv`、`sampleSubmission.csv`
- 訓練集為每月 1-19 日的資料，測試集為每月 20 日至月底的資料

## 使用工具

Python, pandas, numpy, matplotlib, seaborn, scikit-learn

## 流程

### 1. 讀取資料
讀入訓練集、測試集與提交範例格式。資料完整度高，無缺失值。

### 2. 排除離群值
count（租借數量）分布中，最大值遠高於中位數，判斷存在極端值，
以「與平均值差距超過 3 倍標準差」為門檻排除離群值。

### 3. 合併資料並拆解時間特徵
合併訓練集與測試集，從 datetime 拆解出日期、小時、年份、
星期幾、月份，作為獨立的數值特徵。

### 4. 檢視數值特徵分布並修正風速異常值
觀察溫度、體感溫度、濕度、風速的分布，發現風速為 0 的資料異常地多，
推測是缺失值被統一補為 0。訓練隨機森林迴歸模型，
利用其他特徵重新預測這些風速值。

### 5. 對 count 取對數，處理資料歪斜
count 分布嚴重右偏，取對數（log）轉換使其更接近常態分布，
以此作為訓練模型時使用的答案。

### 6. 拆分回訓練/測試集，移除不需要的欄位
依 count 是否為空拆分資料，移除答案本身與高度相關欄位
（casual、registered，避免資訊洩漏），以及已轉換的原始文字欄位。

### 7. 訓練模型並產生提交檔案
使用取對數後的 count 訓練隨機森林迴歸模型，對測試集進行預測，
再以 exp() 轉換回原始數值，負值修正為 0，組裝成提交檔案。

## 檔案結構
02-bike-sharing-demand-prediction/
├── README.md
├── train.csv
├── test.csv
├── sampleSubmission.csv
├── bike_sharing_analysis.ipynb
└── bike_predictions_RF.csv

## 快速連結

- [完整分析筆記（bike_sharing_analysis.ipynb）](./bike_sharing_analysis.ipynb)
- [提交結果（bike_predictions_RF.csv）](./bike_predictions_RF.csv)

## 參考資料

- [Yeh James - 資料分析＆機器學習 第4.2講：共享單車需求預測（前17%排名）](https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC4-2%E8%AC%9B-%E5%85%B1%E4%BA%AB%E5%96%AE%E8%BB%8A%E9%9C%80%E6%B1%82%E9%A0%90%E6%B8%AC-%E5%89%8D17-%E6%8E%92%E5%90%8D-505ed7100825)
