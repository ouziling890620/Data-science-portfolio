# 心臟病預測｜Heart Disease Prediction

## 專題說明
透過病人的臨床參數，比較多種分類演算法並進行超參數調校，預測是否罹患心臟病（二元分類）。

## 資料集
- 來源：[UCI Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+Disease)
- 共 14 個欄位：13 個臨床特徵 + 1 個預測目標（有無心臟病）

## 分析流程
1. 探索性資料分析：目標變數分布、特徵相關性
2. 比較 KNN、Logistic Regression、Random Forest 三種演算法
3. 使用 RandomizedSearchCV 與 GridSearchCV 進行超參數調校
4. 以混淆矩陣、ROC 曲線、交叉驗證評估模型

## 評估結果
- 最終模型：調校後的 Logistic Regression
- 測試集準確率：88.5%
- 交叉驗證 F1-score：87%
- 最重要特徵：胸痛類型（cp）、靜態心電圖（restecg）、ST 段斜率（slope）

## 臨床觀點
胸痛類型與 ST 段變化是臨床上評估心臟病的重要指標，
模型結果與臨床判斷方向一致，但實際應用仍需搭配醫師診斷。

## 參考來源
- [UCI Heart Disease Dataset - GitHub](https://github.com/nmiuddin/UCI-Heart-Disease-Dataset/blob/master/UCI-heart-disease.ipynb)