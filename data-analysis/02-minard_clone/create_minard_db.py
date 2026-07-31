import pandas as pd
import sqlite3

class CreateMinarDB:
    def __init__(self):
        # ========== 讀取原始文字檔 ==========
        with open("data/minard.txt") as f:
            lines = f.readlines()

        # 第3行是欄位名稱，用空白切割
        column_names = lines[2].split()

        # ========== 清理欄位名稱 ==========
        # 原始欄位名稱夾雜統計軟體的特殊符號，需要清除
        patterns_to_be_replaced = {"(", ")", "$", ","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")
            adjusted_column_names.append(column_name)

        self.lines = lines

        # 依照欄位性質，分成三組
        self.column_names_city = adjusted_column_names[:3]         # 城市：經度、緯度、城市名
        self.column_names_temperature = adjusted_column_names[3:7] # 氣溫：經度、溫度、天數、日期
        self.column_names_troop = adjusted_column_names[7:]        # 軍隊：經度、緯度、存活人數、方向、分隊

    # ========== 載入城市資料（第6~25行、第0~2欄） ==========
    # 城市：經度、緯度、城市名
    def create_city_dataframe(self):
        i = 6
        longitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]  # 每行只取前三個欄位
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1

        city_data = (longitudes, latitudes, cities)
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df

    # ========== 載入氣溫資料（第6~14列、第3~7欄） ==========
    # 氣溫：經度、溫度、天數、日期
    def create_temperature_dataframe(self):
        i = 6
        longitudes, temperatures, days, dates = [], [], [], []
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append("Nov 24") # 第 10 列資料的日期為遺漏值。
            else:
                date_str = lines_split[6] + " " + lines_split[7]
                dates.append(date_str)
            i += 1

        temperature_data = (longitudes, temperatures, days, dates)
        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        return temperature_df
    
    # ==========  載入軍隊資料 (第6~53列、倒數第1~倒數第5欄) ==========
    # 軍隊：軍隊經度、軍隊緯度、存活人數、方向、分隊
    def create_troop_dataframe(self):
        i = 6
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i += 1
        troop_data = (longitudes, latitudes, survivals, directions, divisions)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df

    # ==========  建立資料庫 minard.db ==========
    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        # 把三份整理好的資料表，分別存進資料庫
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities": city_df,
            "temperatures": temperature_df,
            "troops": troop_df
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")

create_minar_db = CreateMinarDB()
create_minar_db.create_database()