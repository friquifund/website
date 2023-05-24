import pandas as pd
from typing import List


def preprocess_members(df_spreadsheet_members: pd.DataFrame, dict_rename) -> pd.DataFrame:

    df = df_spreadsheet_members.rename(columns=dict_rename, inplace=False)
    df.loc[df["linkedin"] == "", "linkedin"] = pd.NA
    df.loc[df["name"] == "", "name"] = pd.NA
    df = df[~df["linkedin"].isna()]
    df = df[~df["name"].isna()]

    df["name"] = df["name"].str.title()
    df["linkedin"] = update_url(df["linkedin"])

    return df


def postprocess_web_data(df_csv_web: pd.DataFrame, df_team_parsed: pd.DataFrame, leadership_members: List[str]) -> pd.DataFrame:

    df_team = pd.concat([df_csv_web[~df_csv_web["linkedin"].isin(df_team_parsed["linkedin"])], df_team_parsed], axis=0)
    df_team = df_team.sort_values("id_member", ascending=True)
    #df_team["leadership"] = int(0)
    #df_team.loc[df_team["name"].isin(leadership_members), "leadership"] = int(1)
    return df_team


def update_url(col_linkedin: pd.Series):

    col_linkedin[~col_linkedin.str.startswith("http")] = "https://" + col_linkedin
    col_linkedin = col_linkedin.str.strip().str.replace(" ", "")
    col_linkedin = col_linkedin.str.replace("https://es.linkedin.com", "https://www.linkedin.com", regex=False)
    col_linkedin = col_linkedin.str.replace("https://linkedin.com", "https://www.linkedin.com", regex=False)
    return col_linkedin


def preprocess_csv_web(df_csv_web: pd.DataFrame):
    df_csv_web = df_csv_web[~df_csv_web["linkedin"].isna()]
    df_csv_web = df_csv_web[~df_csv_web["name"].isna()]

    df_csv_web["name"] = df_csv_web["name"].str.title()
    df_csv_web.loc[df_csv_web["linkedin"] == "", "linkedin"] = pd.NA
    df_csv_web.loc[df_csv_web["name"] == "", "name"] = pd.NA
    df_csv_web["linkedin"] = update_url(df_csv_web["linkedin"])
    return df_csv_web
