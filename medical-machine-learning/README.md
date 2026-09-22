# Medical Machine Learning Projects

紀錄應用機器學習於醫學資訊領域的專題實作。

## 專題列表

1. [心臟病預測](./01-heart-disease-prediction) - 透過病人臨床參數，
   比較多種分類演算法並進行超參數調校，預測是否罹患心臟病

2. [ECG 心律不整辨識](./02-ecg-arrhythmia) - 使用 MIT-BIH 資料集，
   以 1D-CNN 辨識 5 種心律類型，測試集準確率達 98.47%

3. [肺炎 X 光影像辨識](./03-pneumonia-xray) - 使用胸部 X 光影像，
   分別以自建 CNN 與 ResNet50 遷移學習實作，比較兩種方法辨識肺炎的差異

4. [敗血症預測](./04-sepsis-prediction) - 使用 ICU 臨床時序資料，
   以雙輸入 LSTM 模型預測下一小時發生敗血症的機率，測試集 AUC 達 0.77