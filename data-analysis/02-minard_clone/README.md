# 練習專案二 : 拿破崙征俄戰爭

## 簡介
本專案「拿破崙征俄戰爭」復刻了 Charles Minard 經典的資料視覺化作品
[Napoleon's disastrous Russian campaign of 1812](https://www.datavis.ca/gallery/re-minard.php)。
使用 `pandas` 與 `sqlite3` 建立資料庫，以 `matplotlib` 與 `basemap`
進行概念驗證，並產出最終成品。


## 如何重現
- 安裝 `Miniconda`
- 依據 `environment.yml` 建立環境：
```bash
  conda env create -f environment.yml
```
- 將 `data/` 資料夾中的 `minard.txt` 置放於工作目錄中的 `data/` 資料夾
- 啟動環境並執行 `python create_minard_db.py`，會在 `data/` 資料夾中建立 `minard.db`
- 啟動環境並執行 `python plot_with_basemap.py`，會生成 `minard_clone.png`
![minard_clone](minard_clone.png)

## 檔案結構

02-minard_clone/
├── data/ # 原始文字檔與 minard.db
├── create_minard_db.py # 解析文字檔並建立資料庫
├── proof_of_concept.py # matplotlib 概念驗證（四張圖分開繪製）
├── plot_with_basemap.py # 合併四圖，產出最終成品
└── minard_clone.png # 最終成品

## 快速連結

- [最終成品（minard_clone.png）](./minard_clone.png)