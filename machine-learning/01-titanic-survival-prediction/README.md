# Titanic 生存預測

## 專案說明

本專題參考 [Yeh James 的教學文章](https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC4-1%E8%AC%9B-kaggle%E7%AB%B6%E8%B3%BD-%E9%90%B5%E9%81%94%E5%B0%BC%E8%99%9F%E7%94%9F%E5%AD%98%E9%A0%90%E6%B8%AC-%E5%89%8D16-%E6%8E%92%E5%90%8D-a8842fea7077)，
利用 Kaggle 上的鐵達尼號生存預測資料集，練習機器學習專案的完整流程：
資料探索、特徵工程、缺失值處理、模型訓練與結果評估。

## 資料來源

- [Kaggle: Titanic - Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic/data)
- 使用檔案：`train.csv`、`test.csv`、`gender_submission.csv`

## 使用工具

Python, pandas, numpy, matplotlib, seaborn, scikit-learn

## 流程

### 1. 讀取與合併資料
讀入訓練集與測試集，合併成同一份資料，方便特徵工程一次套用在兩者上。

### 2. 探索性資料分析（EDA）
觀察生存與死亡比例、艙等、性別、上船港口、年齡、票價、
家庭人數等特徵與生存率的關係，找出可能影響生存機率的因素。

### 3. 特徵工程
- 從姓名擷取稱謂（Title），並將稀少的稱謂合併為 Mr / Mrs / Miss / Master 四大類
- 從票號擷取代碼資訊（Ticket_info）
- 從艙房編號擷取所在甲板區域（Cabin），缺失則標記為 NoCabin
- 將 SibSp（兄弟姊妹/配偶數）與 Parch（父母/子女數）合併為 Family_Size

### 4. 補齊缺失值
- Embarked：以出現次數最多的港口補齊
- Fare：以平均值補齊
- Age：訓練一個隨機森林迴歸模型，利用其他特徵（艙等、性別、稱謂等）預測缺失的年齡值

### 5. 類別資料轉換
將性別、上船港口、艙等、稱謂、艙房、票號代碼等文字類別欄位，
轉換為模型可以讀取的整數編碼。

### 6. 模型訓練
使用隨機森林分類模型（Random Forest Classifier）進行訓練，
並利用 OOB（Out-of-Bag）評分估算模型準確率，不需額外切分驗證集。

### 7. 產生提交檔案
使用訓練好的模型對測試集進行預測，輸出符合 Kaggle 格式的 `submit.csv`。

## 結果

- 隨機森林模型 OOB（Out-of-Bag）準確率：**0.8361**
- 特徵重要性排名前三：Sex、Fare、Title2，其中 Sex（性別）影響最大，
  與資料探索階段觀察到「女性生存率遠高於男性」的結果一致

## 分析筆記：發現並修正離群值篩選的邏輯錯誤

原文章在訓練「年齡預測模型」前，會先篩選出 Fare、Family_Size 極端異常的
樣本，變數命名為 `remove_outlier`，原意應為「排除離群值後的乾淨資料」。

但實際檢查後發現，原文章的篩選條件**沒有使用反轉（`~`）**，導致
`remove_outlier` 實際上只留下 26 筆「被判定為離群值」的資料本身，
而非排除離群值後、應有的 1020 筆乾淨資料，這代表原文章的年齡預測模型
只用了 26 筆極端樣本進行訓練。

修正方式：在篩選條件前加上 `~`，取得排除離群值後的乾淨資料，
再用這份資料訓練年齡預測模型。修正後，最終隨機森林分類模型的 OOB
準確率由原文章的 0.8294 提升至 **0.8361**，驗證了修正後的年齡補值
更貼近實際情況，也連帶提升了整體模型表現。

## 檔案結構

```
01-titanic-survival-prediction/
├── README.md
├── train.csv
├── test.csv
├── gender_submission.csv
├── titanic_analysis.ipynb
└── submit.csv
```

## 快速連結

- [完整分析筆記（titanic_analysis.ipynb）](./titanic_analysis.ipynb)
- [提交結果（submit.csv）](./submit.csv)

## 參考資料

- [Yeh James - 資料分析＆機器學習 第4.1講：Kaggle競賽-鐵達尼號生存預測（前16%排名）](https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC4-1%E8%AC%9B-kaggle%E7%AB%B6%E8%B3%BD-%E9%90%B5%E9%81%94%E5%B0%BC%E8%99%9F%E7%94%9F%E5%AD%98%E9%A0%90%E6%B8%AC-%E5%89%8D16-%E6%8E%92%E5%90%8D-a8842fea7077)