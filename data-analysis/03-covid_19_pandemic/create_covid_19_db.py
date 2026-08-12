import pandas as pd
import sqlite3

class CreateCovid19DB:

    def create_time_series(self):
        """讀取 confirmed、deaths、vaccine 三份時間序列資料，
        整理成寬轉長格式並合併成一份以「國家+日期」彙總的時間序列表。"""

        confirmed = pd.read_csv("data/time_series_covid19_confirmed_global.csv")   # 全球確診數時間序列（寬格式）
        deaths = pd.read_csv("data/time_series_covid19_deaths_global.csv")         # 全球死亡數時間序列（寬格式）
        vaccine = pd.read_csv("data/time_series_covid19_vaccine_global.csv")       # 全球疫苗接種時間序列

        # ========== 轉置 confirmed 與 deaths：寬格式轉長格式 ==========
        # id_vars 保持不變，其餘所有日期欄位自動轉置成 Date + 對應數值
        id_variables = ["Province/State", "Country/Region", "Lat", "Long"]
        melted_confirmed = pd.melt(confirmed, id_vars=id_variables, var_name="Date", value_name="Confirmed")
        melted_deaths = pd.melt(deaths, id_vars=id_variables, var_name="Date", value_name="Deaths")

        # 原始日期為文字字串（如 "1/22/20"），轉換為ISO8601格式
        melted_confirmed["Date"] = pd.to_datetime(melted_confirmed["Date"], format="%m/%d/%y")
        melted_deaths["Date"] = pd.to_datetime(melted_deaths["Date"], format="%m/%d/%y")

        # ========== 調整 vaccine 欄位 ==========
        vaccine["Province_State"] = vaccine["Province_State"].astype(object)  # 確保資料型態一致
        vaccine["Date"] = pd.to_datetime(vaccine["Date"])                      # 轉換為日期型態
        vaccine = vaccine.rename(columns={
            "Province_State": "Province/State",
            "Country_Region": "Country/Region"
        })  # 統一欄位名稱格式（底線→斜線）

        # ========== 篩選需要的欄位 ==========
        melted_confirmed = melted_confirmed.drop(labels=["Lat", "Long"], axis=1)
        melted_deaths = melted_deaths.drop(labels=["Lat", "Long"], axis=1)
        vaccine = vaccine.drop(labels=["UID", "People_at_least_one_dose"], axis=1)

        # ======= 連接資料框：合併三份時間序列資料 =======
        # 以省州+國家+日期為比對依據合併
        join_keys = ["Province/State", "Country/Region", "Date"]
        time_series = pd.merge(melted_confirmed, melted_deaths, left_on=join_keys, right_on=join_keys, how="left")
        time_series = pd.merge(time_series, vaccine, left_on=join_keys, right_on=join_keys, how="left")

        # Province/State 僅用於精準合併，之後要以「國家+日期」彙總，不再需要
        time_series = time_series.drop(labels="Province/State", axis=1)

        # 依國家+日期分組，加總確診、死亡、疫苗劑數
        time_series = time_series.groupby(["Country/Region", "Date"])[["Confirmed", "Deaths", "Doses_admin"]].sum().reset_index()

        # ========== 調整欄位名稱與資料型別 ==========
        time_series.columns = ["country", "reported_on", "confirmed", "deaths", "doses_administered"]
        time_series["doses_administered"] = time_series["doses_administered"].astype(int)

        return time_series
    
    def create_daily_report(self):
        """讀取單日（2023/3/9，資料停止更新前最後一天）各國病例概況，
        整理成僅保留核心欄位、統一命名的 DataFrame。"""

        daily_report = pd.read_csv("data/03-09-2023.csv") 

        # ========== 選擇需要的欄位、統一欄位命名 ==========
        daily_report = daily_report[["Country_Region", "Province_State", "Admin2", "Confirmed", "Deaths", "Lat", "Long_"]]
        daily_report.columns = ["country", "province", "county", "confirmed", "deaths", "latitude", "longitude"]

        return daily_report

def create_database(self):
    """整合 time_series 與 daily_report，寫入 SQLite 資料庫。"""

    time_series = self.create_time_series()
    # SQLite 不支援直接儲存 datetime64 型態，轉成字串格式（YYYY-MM-DD）才能正確寫入
    time_series["reported_on"] = time_series["reported_on"].map(lambda x: x.strftime("%Y-%m-%d"))

    daily_report = self.create_daily_report()

    connection = sqlite3.connect("data/covid_19.db")
    time_series.to_sql("time_series", con=connection, if_exists="replace", index=False)
    daily_report.to_sql("daily_report", con=connection, if_exists="replace", index=False)
    connection.close()

create_covid_19_db = CreateCovid19DB()
create_covid_19_db.create_database()