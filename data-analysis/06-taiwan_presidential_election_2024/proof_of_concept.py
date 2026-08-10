import sqlite3
import pandas as pd
import numpy as np



connection = sqlite3.connect("data/taiwan_presidential_election_2024.db")
votes_by_village = pd.read_sql("""SELECT * FROM votes_by_village;""", con=connection)
connection.close()

# ========== 計算全國得票率向量 →a ==========
total_votes = votes_by_village["sum_votes"].sum()  # 全國總得票數

# 每位候選人的全國得票率 = 依候選人id分組加總得票數，再除以全國總得票數
country_percentage = votes_by_village.groupby("id")["sum_votes"].sum() / total_votes

vector_a = country_percentage.values  # 轉成純數字陣列，供後續向量運算使用


# ========== 計算村鄰里得票率向量 →bi ==========

groupby_variables = ["county", "town", "village"]

# 每個村里的總得票數（所有候選人加總）
village_total_votes = votes_by_village.groupby(groupby_variables)["sum_votes"].sum().reset_index()

# 把「候選人在村里的得票數」與「村里總得票數」合併
merged = pd.merge(votes_by_village, village_total_votes, left_on=groupby_variables, right_on=groupby_variables,
                   how="left")

# 候選人得票率 = 候選人在村里的得票數 ÷ 村里總得票數
merged["village_percentage"] = merged["sum_votes_x"] / merged["sum_votes_y"]

merged = merged[["county", "town", "village", "id", "village_percentage"]]
print(merged)

# ========== 轉置資料框：長格式轉寬格式 ==========
# 每一列即為一個村里的得票率向量 →bi
pivot_df = merged.pivot(index=["county", "town", "village"], columns="id", values="village_percentage").reset_index()
pivot_df = pivot_df.rename_axis(None, axis=1)  # 移除多餘欄位軸標籤

# ========== 計算餘弦相似度 SC(→a, →bi) ==========
cosine_similarities = []
for row in pivot_df.iterrows():
    vector_bi = np.array([row[1][1], row[1][2], row[1][3]]) # 該村里三候選人得票率向量

    vector_a_dot_vector_bi = np.dot(vector_a, vector_bi)   # 內積：→a · →bi
    length_vector_a = pow((vector_a**2).sum(), 0.5)        # 向量長度：||→a||
    length_vector_bi = pow((vector_bi**2).sum(), 0.5)      # 向量長度：||→bi||

    # 餘弦相似度 = 內積 ÷ (兩向量長度相乘)，越接近1代表越相似
    cosine_similarity = vector_a_dot_vector_bi / (length_vector_a * length_vector_bi)
    cosine_similarities.append(cosine_similarity)

# ========== 建立最終結果資料框：依相似度排序並建立排名 ==========

cosine_similarity_df = pivot_df.iloc[:, :]
cosine_similarity_df["cosine_similarity"] = cosine_similarities

# 依餘弦相似度遞減排序，同分則依地名排序
cosine_similarity_df = cosine_similarity_df.sort_values(
    ["cosine_similarity", "county", "town", "village"],
    ascending=[False, True, True, True]
)

# 排序後重整索引，並轉成排名欄位（從1開始
cosine_similarity_df = cosine_similarity_df.reset_index(drop=True).reset_index()
cosine_similarity_df["index"] = cosine_similarity_df["index"] + 1  

# 改名：index→rank，候選人id(1,2,3)→易讀欄位名
column_names_to_revise = {
    "index": "rank",
    1: "candidate_1",
    2: "candidate_2",
    3: "candidate_3"
}
cosine_similarity_df = cosine_similarity_df.rename(columns=column_names_to_revise)

# ========== 篩選指定縣市/鄉鎮/村里 ==========
def filter_county_town_village(df, county_name: str, town_name: str, village_name: str):
    county_condition = df["county"] == county_name
    town_condition = df["town"] == town_name
    village_condition = df["village"] == village_name
    # 三個條件同時符合（且），才回傳該列
    return df[county_condition & town_condition & village_condition]
print(filter_county_town_village(cosine_similarity_df, county_name="臺北市", town_name="士林區", village_name="天玉里"))