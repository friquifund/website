import pandas as pd
from typing import List


def preprocess_members(df_spreadsheet_members: pd.DataFrame) -> pd.DataFrame:

    df = df_spreadsheet_members.copy()#.rename(columns=dict_rename, inplace=False)
    df.loc[df["LinkedIn"] == "", "LinkedIn"] = pd.NA
    df.loc[df["Name"] == "", "Name"] = pd.NA
    df = df[~df["LinkedIn"].isna()]
    df = df[~df["Name"].isna()]

    df["Name"] = df["Name"].str.title()
    df["LinkedIn"] = update_url(df["LinkedIn"])

    return df


def postprocess_web_data(df_csv_web: pd.DataFrame, df_team_parsed: pd.DataFrame) -> pd.DataFrame:

    df_team = pd.concat([df_csv_web[~df_csv_web["LinkedIn"].isin(df_team_parsed["LinkedIn"])], df_team_parsed], axis=0)
    df_team = df_team.sort_values("Membership Number", ascending=True)
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

    df_csv_web.loc[df_csv_web["Name"] == "", "Name"] = pd.NA
    df_csv_web = df_csv_web[~df_csv_web["Name"].isna()]
    df_csv_web["Name"] = df_csv_web["Name"].str.title()

    df_csv_web.loc[df_csv_web["LinkedIn"] == "", "LinkedIn"] = pd.NA
    df_csv_web = df_csv_web[~df_csv_web["LinkedIn"].isna()]
    df_csv_web["LinkedIn"] = update_url(df_csv_web["LinkedIn"])

    df_csv_web["timestamp_creation"] = df_csv_web["Year"].astype(str) + "-" + df_csv_web["Start Date"]
    df_csv_web["timestamp_creation"] = pd.to_datetime(df_csv_web["timestamp_creation"]).astype(str)

    if "last_updated" not in df_csv_web.columns:
        df_csv_web["last_updated"] = pd.NA

    df_csv_web.loc[df_csv_web["last_updated"].isna(), "last_updated"] = df_csv_web["timestamp_creation"]
    df_csv_web = df_csv_web.drop(columns="timestamp_creation")

    return df_csv_web
