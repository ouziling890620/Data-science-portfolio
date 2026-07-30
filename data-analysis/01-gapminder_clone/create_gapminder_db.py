import pandas as pd
import sqlite3


class CreateGapminderDB:
    # ========== 讀取資料設定 ==========
    def __init__(self):
        # 讀取資料來源（依序為：每個國家每年的 人均GDP、預期壽命、人口、地理資訊）
        self.file_names = ["ddf--datapoints--gdp_pcap--by--country--time", 
                            "ddf--datapoints--lex--by--country--time", 
                            "ddf--datapoints--pop--by--country--time", 
                            "ddf--entities--geo--country"]         

        # 資料表取名（與上方檔名順序對應）
        self.table_names = ["gdp_per_capita", "life_expectancy", "population", "geography"]

    # ========== 讀取 csv 並存入字典 ==========
    def import_as_dataframe(self):
        df_dict = dict() # 建立空字典

        # 配對「檔名」和「表名」
        for file_name, table_name in zip(self.file_names, self.table_names):
            file_path = f"data/{file_name}.csv"
            df = pd.read_csv(file_path) #讀取這個 csv，存成 DataFrame。
            df_dict[table_name] = df #存進字典，key 為表名(table_name)。
        return df_dict
        
    # ========== 寫入 SQLite 資料庫 ==========
    def create_database(self):

        connection = sqlite3.connect("data/gapminder.db") # 建立資料庫連線
        df_dict = self.import_as_dataframe()
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace") # 逐一寫入資料庫

        # ========== 建立檢視表 ==========
        # 如果之前已經建立過同名的檢視表，先刪除，避免重複建立時報錯
        drop_view_sql = """
        DROP VIEW IF EXISTS plotting;
        """

        # 建立一個叫做 plotting 的檢視表
        # 把四張表依照國家（country）和年份（time）合併成一張整合表
        create_view_sql = """
        CREATE VIEW plotting AS
        SELECT geography.name AS country_name,
               geography.world_4region AS continent,
               gdp_per_capita.time AS dt_year,
               gdp_per_capita.gdp_pcap AS gdp_per_capita,
               life_expectancy.lex AS life_expectancy,
               population.pop AS population
          FROM gdp_per_capita
          JOIN geography
            ON gdp_per_capita.country = geography.country
          JOIN life_expectancy
            ON gdp_per_capita.country = life_expectancy.country AND
               gdp_per_capita.time = life_expectancy.time
          JOIN population
            ON gdp_per_capita.country = population.country AND
               gdp_per_capita.time = population.time
         WHERE gdp_per_capita.time < 2024;
        """

        cur = connection.cursor()
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)

        connection.close() # 關閉資料庫連線，釋放資源

create_gapminder_db = CreateGapminderDB()
create_gapminder_db.create_database()