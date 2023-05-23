import pandas as pd
from typing import List


def preprocess_members(df_spreadsheet_members: pd.DataFrame) -> pd.DataFrame:

    dict_rename = {"LinkedIn": "linkedin", "Name": "name", "City": "city"}
    df = df_spreadsheet_members.rename(columns=dict_rename, inplace=False)

    return df


def postprocess_web_data(df_csv_web: pd.DataFrame, df_team_parsed: pd.DataFrame, leadership_members: List[str]) -> pd.DataFrame:

    df_team = pd.concat([df_csv_web[~df_csv_web["linkedin"].isin(df_team_parsed["linkedin"])], df_team_parsed], axis=0)
    df_team["leadership"] = int(0)
    df_team.loc[df_team["name"].isin(leadership_members), "leadership"] = int(1)
    return df_team


def get_default_csv_web() -> pd.DataFrame:
    df_csv_web = pd.DataFrame({"linkedin": [], "last_updated": [], "city": [], "name": []})
    df_csv_web["linkedin"] = df_csv_web["linkedin"].astype(str)
    df_csv_web["last_updated"] = df_csv_web["last_updated"].astype(str)
    return df_csv_web
