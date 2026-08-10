import pandas as pd
import os
import re
import sqlite3
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class CreateTaiwanPresidentialElection2024DB:

    def __init__(self):
        """讀取 data 資料夾內的檔名，取得所有縣市名稱。"""
        county_names = []
        file_names = os.listdir("data")
        for file_name in file_names:
            if ".xlsx" in file_name:
                # 檔名格式如 "...(臺北市).xlsx"，用括號切割取出縣市名稱
                file_name_split = re.split("\\(|\\)", file_name)
                county_names.append(file_name_split[1])
        self.county_names = county_names
        
    def tidy_county_dataframe(self, county_name: str):
        # 讀取指定縣市的原始得票 Excel，整理成長格式的 DataFrame。
        file_path = f"data/總統-A05-4-候選人得票數一覽表-各投開票所({county_name}).xlsx"
        # 跳過標題文字與空白列，只讀取前6欄核心資料
        df = pd.read_excel(file_path, skiprows=[0, 3, 4])
        df = df.iloc[:, :6]
        # 擷取候選人資訊，記錄到欄位名稱後，原始列即可捨棄
        candidates_info = df.iloc[0, 3:].values.tolist()
        df.columns = ["town", "village", "polling_place"] + candidates_info
        # 前向填補鄉鎮市區未定義值（合併儲存格造成的空白）
        df.loc[:, "town"] = df["town"].ffill()
        df.loc[:, "town"] = df["town"].str.strip()  # 去除多餘空白
        # 刪除有未定義值的列（候選人資訊列、總計列、鄉鎮市區小計列）
        df = df.dropna()
        # 投票所編號轉為整數
        df["polling_place"] = df["polling_place"].astype(int)
        # 轉成長格式：一列代表「單一投開票所 + 單一候選人」的得票數
        id_variables = ["town", "village", "polling_place"]
        melted_df = pd.melt(df, id_vars=id_variables, var_name="candidate_info", value_name="votes")
        # 新增縣市名稱欄位
        melted_df["county"] = county_name
        return melted_df
    
    # ========== 整合 22 個縣市 ==========
    def concat_country_dataframe(self):
        # 逐一讀取每個縣市的資料，合併成全國一份長格式表
        country_df = pd.DataFrame()
        for county_name in self.county_names:
            county_df = self.tidy_county_dataframe(county_name)
            country_df = pd.concat([country_df, county_df])
        country_df = country_df.reset_index(drop=True)

        # candidate_info 原始格式如 "(1)\n柯文哲\n吳欣盈"，拆解成號碼與正副候選人姓名
        numbers, candidates = [], []
        for elem in country_df["candidate_info"].str.split("\n"):
            number = re.sub("\\(|\\)", "", elem[0])   # 去掉括號，"(1)" → "1"
            numbers.append(int(number))
            candidate = elem[1] + "/" + elem[2]       # 正副候選人姓名合併，如 "柯文哲/吳欣盈"
            candidates.append(candidate)

        # 把候選人號碼、姓名、得票數，補回縣市/鄉鎮/村里/投開票所資訊
        presidential_votes = country_df.loc[:, ["county", "town", "village", "polling_place"]]
        presidential_votes["number"] = numbers
        presidential_votes["candidate"] = candidates
        presidential_votes["votes"] = country_df["votes"].values
        return presidential_votes

    def create_database(self):
        """建立三張正規化資料表（投開票所、候選人、得票），
        並建立以村里為單位彙總得票數的檢視表。"""
        presidential_votes = self.concat_country_dataframe()

        # 建立投開票所表：依縣市/鄉鎮/村里/投開票所分組去重複，建立流水號當主鍵
        polling_places_df = presidential_votes.groupby(["county", "town", "village", "polling_place"]).count().reset_index()
        polling_places_df = polling_places_df[["county", "town", "village", "polling_place"]]
        polling_places_df = polling_places_df.reset_index()
        polling_places_df["index"] = polling_places_df["index"] + 1  # 主鍵從1開始
        polling_places_df = polling_places_df.rename(columns={"index": "id"})

        # 建立候選人表：依號碼/姓名分組去重複，候選人號碼本身即可當主鍵
        candidates_df = presidential_votes.groupby(["number", "candidate"]).count().reset_index()
        candidates_df = candidates_df[["number", "candidate"]]
        candidates_df = candidates_df.rename(columns={"number": "id"})

        # 建立得票表：用 left join 對應到投開票所id，確保保留所有得票紀錄
        join_keys = ["county", "town", "village", "polling_place"]
        votes_df = pd.merge(presidential_votes, polling_places_df, left_on=join_keys, right_on=join_keys, how="left")
        votes_df = votes_df[["id", "number", "votes"]]
        votes_df = votes_df.rename(columns={"id": "polling_place_id", "number": "candidate_id"})

        # ========== 寫入資料庫 ==========
        connection = sqlite3.connect("data/taiwan_presidential_election_2024.db")
        polling_places_df.to_sql("polling_places", con=connection, if_exists="replace", index=False)
        candidates_df.to_sql("candidates", con=connection, if_exists="replace", index=False)
        votes_df.to_sql("votes", con=connection, if_exists="replace", index=False)

        # 建立檢視表：三張表 JOIN 起來，依村里+候選人分組加總票數
        cur = connection.cursor()
        drop_view_sql = """DROP VIEW IF EXISTS votes_by_village;"""
        create_view_sql = """
        CREATE VIEW votes_by_village AS
        SELECT polling_places.county,
               polling_places.town,
               polling_places.village,
               candidates.id,
               candidates.candidate,
               SUM(votes.votes) AS sum_votes
          FROM votes
          LEFT JOIN polling_places
            ON votes.polling_place_id = polling_places.id
          LEFT JOIN candidates
            ON votes.candidate_id = candidates.id
         GROUP BY polling_places.county,
                  polling_places.town,
                  polling_places.village,
                  candidates.id; 
        """
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()

create_taiwan_presidential_election_2024_db = CreateTaiwanPresidentialElection2024DB()
create_taiwan_presidential_election_2024_db.create_database()