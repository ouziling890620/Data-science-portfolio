# 心臟病預測（Heart Disease Prediction）

## 簡介

本專題參考 [UCI Heart Disease Dataset](https://github.com/nmiuddin/UCI-Heart-Disease-Dataset/blob/master/UCI-heart-disease.ipynb)，
透過病人的臨床參數，建立機器學習模型預測是否罹患心臟病，
屬於二元分類問題。

## 資料來源

- [UCI Machine Learning Repository - Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+Disease)

## 特徵說明

共14個欄位，13個臨床特徵（年齡、性別、胸痛類型、血壓、膽固醇等）
與1個預測目標（target：是否有心臟病，1=有、0=無）。

## 流程

1. **探索性資料分析**：檢查目標變數分布、性別/年齡/胸痛類型與心臟病的關係、變數間相關性
2. **建立基準模型**：比較 KNN、Logistic Regression、Random Forest 三種分類演算法
3. **超參數調校**：手動調校KNN鄰居數量後表現仍不佳，改用 RandomizedSearchCV
   與 GridSearchCV 調校 Logistic Regression 與 Random Forest
4. **模型評估**：以混淆矩陣、classification report、5折交叉驗證計算的
   precision/recall/F1、ROC曲線與AUC，全面評估最終模型
5. **特徵重要性**：分析 Logistic Regression 的 `coef_` 係數，找出影響力最大的特徵

## 結果

- 最終模型（調校後的 Logistic Regression）測試集準確率約 88.5%，
  交叉驗證 F1-score 約 87%，未達到一開始設定的95%目標
- 胸痛類型（cp）、靜息心電圖結果（restecg）、
  運動高峰ST段斜率（slope）為影響力最強的特徵

## 結論與反思

雖未達到95%的目標準確率，但透過系統性地比較三種演算法、
兩種超參數搜尋方法，已釐清目前資料集與模型的表現上限。
後續可能的改進方向包括收集更多樣本、嘗試更適合結構化資料的
演算法（如XGBoost、CatBoost），或進一步優化特徵工程。