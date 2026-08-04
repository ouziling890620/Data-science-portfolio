import pandas as pd
import string
import sqlite3


class CreateKaggleSurveyDB:
    def __init__(self):
        survey_years = [2020, 2021, 2022]
        df_dict = dict()
        for survey_year in survey_years:
            file_path = f"data/kaggle_survey_{survey_year}_responses.csv"

            # 讀取填答資料，跳過題目敘述那一行，只保留真正的填答內容
            df = pd.read_csv(file_path, low_memory=False, skiprows=[1])
            df = df.iloc[:, 1:]  # 刪除第一欄（填答時間），保留其餘欄位
            df_dict[survey_year, "responses"] = df

            # 只讀取第一行（欄位名稱+題目敘述），取得每題的完整題目描述
            df = pd.read_csv(file_path, nrows=1)
            question_descriptions = df.values.ravel()   # 攤平成一維陣列
            question_descriptions = question_descriptions[1:]  # 去除第一欄（填答時間對應的說明）
            df_dict[survey_year, "question_descriptions"] = question_descriptions
        self.survey_years = survey_years
        self.df_dict = df_dict

    # ========== 整理 2020 年的題目資訊（題號、題型、敘述） ==========
    def tidy_2020_2021_data(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []

        column_names = self.df_dict[survey_year, "responses"].columns # 欄位代碼，如 Q1, Q7_A...
        descriptions = self.df_dict[survey_year, "question_descriptions"]   # 對應的題目完整敘述

        for column_name, question_description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")    # 依底線切割欄位代碼
            question_description_split = question_description.split(" - ")  # 依"-"切割題目敘述

            if len(column_name_split) == 1:
                # 欄位代碼沒有底線，如 "Q1" → 單選題
                question_index = column_name_split[0]
                question_indexes.append(question_index)
                question_types.append("Multiple choice") #單選題
                question_descriptions.append(question_description_split[0])
            else:
                # 欄位代碼有底線，如 "Q7_A" 或 "Q7_Part1" → 多選題
                if column_name_split[1] in string.ascii_uppercase: 
                    # 第二段是單一大寫字母（如 A, B, C），代表子選項，併入題號
                    question_index = column_name_split[0] + column_name_split[1]
                    question_indexes.append(question_index)
                else:
                    # 第二段不是大寫字母，題號維持原本的主題號
                    question_index = column_name_split[0]
                    question_indexes.append(question_index)
                question_types.append("Multiple selection") #多選題
                question_descriptions.append(question_description_split[0])
        # ========== 建立題目 DataFrame ==========
        # 把題號、題型、題目敘述三個 list 組成表格；
        # 因複選題會有多個欄位對應同一題，用 groupby 去除重複，只保留獨一的題目資訊
        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
        # ========== 建立回覆 DataFrame ==========
        # 原始資料一列代表一位受訪者、一欄代表一題；
        # 用 melt 轉成長格式，讓「每位受訪者對每一題的回答」變成一筆觀測值，
        # 並捨棄未作答（NaN）的紀錄
        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes # 重新命名欄位代碼，讓欄位名稱與題號一致
        response_df_reset_index = response_df.reset_index()  # 取得受訪者流水編號
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        response_df_melted
        return question_df, response_df_melted
    
    # ========== 整理 2022 年的題目資訊（題號、題型、敘述） ==========
    def tidy_2022_data(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []
        column_names = self.df_dict[survey_year, "responses"].columns
        descriptions = self.df_dict[survey_year, "question_descriptions"]
        for column_name, question_description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")    # 依底線切割欄位代碼
            question_description_split = question_description.split(" - ")  # 依"-"切割題目敘述

            if len(column_name_split) == 1:
                question_types.append("Multiple choice") #單選題
            else:
                question_types.append("Multiple selection") #多選題
            question_index = column_name_split[0]
            question_indexes.append(question_index)
            question_descriptions.append(question_description_split[0])
        # ========== 建立 2022 年題目 DataFrame ==========
        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()
        # ========== 建立 2022 年回覆 DataFrame ==========
        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes
        response_df_reset_index = response_df.reset_index()
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index", value_name="response")
        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index": "respondent_id"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        return question_df, response_df_melted

    # ========== 建立 資料庫 ==========

    def create_database(self):
        question_df = pd.DataFrame()
        response_df = pd.DataFrame()
        for survey_year in self.survey_years:
            if survey_year == 2022:
                q_df, r_df = self.tidy_2022_data(survey_year)
            else:
                q_df, r_df = self.tidy_2020_2021_data(survey_year)
            question_df = pd.concat([question_df, q_df], ignore_index = True)
            response_df = pd.concat([response_df, r_df], ignore_index = True)
        connection = sqlite3.connect("data/kaggle_survey.db")
        question_df.to_sql("questions", con=connection, if_exists="replace", index=False)
        response_df.to_sql("responses", con=connection, if_exists="replace", index=False)
        
        # 建立彙總檢視表：把題目與回覆兩張表 JOIN 起來，
        # 並依「年份、題號、回覆選項」計算出現次數，方便後續統計分析
        cur = connection.cursor() 
        drop_view_sql = """DROP VIEW IF EXISTS aggregated_responses;"""
        create_view_sql = """
        CREATE VIEW aggregated_responses AS
        SELECT questions.surveyed_in,
               questions.question_index,
               questions.question_type,
               questions.question_description,
               responses.response,
               COUNT(responses.respondent_id) AS response_count
          FROM responses
          JOIN questions
            ON responses.question_index = questions.question_index AND
               responses.responded_in = questions.surveyed_in
         GROUP BY questions.surveyed_in,
                  questions.question_index,
                  responses.response; 
        """
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()

create_kaggle_survey_db = CreateKaggleSurveyDB()
create_kaggle_survey_db.create_database()