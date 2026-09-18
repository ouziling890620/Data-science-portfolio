# 肺炎 X 光影像辨識

## 專題說明
使用胸部 X 光影像辨識正常與肺炎兩種類別，分別以自建 CNN 與 ResNet50 遷移學習實作，比較兩種方法的差異。
作為呼吸治療師，本專題結合臨床背景對模型結果進行專業詮釋。

## 資料集
- 來源：[Kaggle Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

| 資料集 | v1 張數 | v2 張數 |
|--------|---------|---------|
| 訓練集 | 5,216   | 4,173   |
| 驗證集 | 16      | 1,043   |
| 測試集 | 624     | 無      |

## 模型比較

| 項目 | v1 自建 CNN | v2 ResNet50 遷移學習 |
|------|------------|---------------------|
| 框架 | Keras | fastai |
| 模型 | 自建 CNN | ResNet50 預訓練模型 |
| 圖片大小 | 64 × 64 | 128 × 128 |
| 驗證集大小 | 16 張 | 1,043 張 |
| 最佳準確率 | 89.26% | 97.7% |
| 過擬合 | epochs=10 出現 | 輕微 |

## 訓練結果

### v1 自建 CNN
| epochs | 訓練準確率 | 測試準確率 |
|--------|-----------|-----------|
| 1      | 90.11%    | 88.96%    |
| 5      | 95.86%    | 89.26%    |
| 10     | 94.90%    | 85.41%    |

### v2 ResNet50 遷移學習
| 階段 | 輪數 | 最終準確率 |
|------|------|-----------|
| 第一階段 | 4輪 | 93.8% |
| 第二階段 | 20輪 | 97.1% |
| 微調 | 10輪 | 97.7% |

> v2 遷移學習準確率（97.7%），顯著優於 v1 自建 CNN（89.26%）。

## 臨床觀點
身為呼吸治療師，FN（假陰性：肺炎被預測為正常）是最危險的錯誤，
可能導致延誤治療。實際臨床應用仍需搭配醫師判斷，不可單獨作為診斷依據。

## 參考
- [Intro to CNN using Keras](https://www.kaggle.com/code/sanwal092/intro-to-cnn-using-keras-to-predict-pneumonia/notebook)
- [Pneumonia Detection using CNN 96%+](https://www.kaggle.com/code/arbazkhan971/pneumonia-detection-using-cnn-96-accuracy)