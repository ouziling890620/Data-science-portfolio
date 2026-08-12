# 練習專案六: 找出章魚里

## 簡介

本專題透過中選會選舉及公投資料庫的
[2024 ー 第16任總統副總統選舉](https://db.cec.gov.tw/ElecTable/Election/ElecTickets?dataType=tickets&typeId=ELC&subjectId=P0&legisId=00&themeId=4d83db17c1707e3defae5dc4d4e9c800&dataLevel=N&prvCode=00&cityCode=000&areaCode=00&deptCode=000&liCode=0000)
資料，計算全台灣 7700 餘個村鄰里的得票率，並以餘弦相似度與全國得票率比較，
針對媒體常見的「章魚里」報導提出兩點反思：

1. 人口結構會變動、選舉有不同類型，將特定村鄰里訂為長年不變的章魚里並不合理
2. 「得票率跟最終結果非常相近」的定義非常模糊，缺乏一致的量化標準

透過這個專題，練習了處理含合併儲存格的原始 Excel 資料、
建立正規化的 SQLite 資料庫（投開票所、候選人、得票三張表）、
以向量與餘弦相似度衡量得票結構的相似程度，並用 `gradio` 建立互動式查詢介面。

## 資料來源

來自中選會選舉及公投資料庫：
- [2024 第16任總統副總統選舉](https://db.cec.gov.tw/ElecTable/Election/ElecTickets?dataType=tickets&typeId=ELC&subjectId=P0&legisId=00&themeId=4d83db17c1707e3defae5dc4d4e9c800&dataLevel=N&prvCode=00&cityCode=000&areaCode=00&deptCode=000&liCode=0000)
- 下載「各投票所得票明細及概況」試算表（22 個縣市，各為一份 xlsx 檔案）

## 計算方法

將全國得票率視為向量 →a，村鄰里得票率視為向量 →bi，
以餘弦相似度衡量兩者的相似程度：

$$
SC(\vec{a}, \vec{b_i}) = \frac{\vec{a} \cdot \vec{b_i}}{\|\vec{a}\| \|\vec{b_i}\|}
$$

依相似度遞減排序，相似度最高者即為最貼近全國得票結構的「章魚里」。


## 如何重現

- 安裝 `Miniconda`
- 依據 `environment.yml` 建立環境：

```bash
conda env create -f environment.yml
```

- 將 22 個縣市的「總統-A05-4-候選人得票數一覽表-各投開票所」試算表檔案，
  置放於工作目錄中的 `data/` 資料夾
- 啟動環境並執行 `python create_taiwan_presidential_election_2024_db.py`，
  會在 `data/` 資料夾中建立 `taiwan_presidential_election_2024.db`
- 啟動環境並執行 `python app.py`，並前往 `http://127.0.0.1:7860` 瀏覽成品

## 檔案結構

```
06-taiwan_presidential_election_2024/
├── data/ # 原始 xlsx 與 taiwan_presidential_election_2024.db
├── create_taiwan_presidential_election_2024_db.py # 建立資料庫與檢視表
├── proof_of_concept.py # numpy 計算餘弦相似度概念驗證
└── app.py # gradio 互動式查詢介面
```

## 快速連結

- [建立資料庫程式碼](./create_taiwan_presidential_election_2024_db.py)
- [gradio 查詢介面](./app.py)