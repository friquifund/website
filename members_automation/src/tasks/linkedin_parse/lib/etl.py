import pandas as pd
from src.utils.pandas.transformations import transform_float_to_ints


def preprocess_members(df_spreadsheet_members: pd.DataFrame) -> pd.DataFrame:

    df = df_spreadsheet_members.copy()
    df.loc[df["Name"] == "", "Name"] = pd.NA
    df = df[~df["Name"].isna()]

    df["Name"] = df["Name"].str.title()
    df["LinkedIn"] = clean_url(df["LinkedIn"])

    df = df[df.columns[~df.columns.str.contains("Unnamed")]]

    df = transform_float_to_ints(df)

    return df


def clean_url(col_linkedin: pd.Series):

    col_linkedin[~(col_linkedin.str.startswith("http").astype(bool))] = "https://" + col_linkedin
    col_linkedin = col_linkedin.str.strip().str.replace(" ", "")
    col_linkedin = col_linkedin.str.replace("https://es.linkedin.com", "https://www.linkedin.com", regex=False)
    col_linkedin = col_linkedin.str.replace("https://linkedin.com", "https://www.linkedin.com", regex=False)
    col_linkedin[col_linkedin == ""] = pd.NA
    return col_linkedin


def preprocess_csv_web(df_csv_web: pd.DataFrame):

    df_csv_web.loc[df_csv_web["Name"] == "", "Name"] = pd.NA
    df_csv_web = df_csv_web[~df_csv_web["Name"].isna()]
    df_csv_web["Name"] = df_csv_web["Name"].str.title()

    df_csv_web["LinkedIn"] = clean_url(df_csv_web["LinkedIn"])

    df_csv_web["timestamp_creation"] = df_csv_web["Year"].astype(str) + "-" + df_csv_web["Start Date"]
    df_csv_web["timestamp_creation"] = pd.to_datetime(df_csv_web["timestamp_creation"]).astype(str)

    if "last_updated" not in df_csv_web.columns:
        df_csv_web["last_updated"] = pd.NA

    df_csv_web.loc[df_csv_web["last_updated"].isna(), "last_updated"] = df_csv_web["timestamp_creation"]
    df_csv_web = df_csv_web.drop(columns="timestamp_creation")

    df_csv_web = df_csv_web[df_csv_web.columns[~df_csv_web.columns.str.contains("Unnamed")]]

    df_csv_web = transform_float_to_ints(df_csv_web)

    return df_csv_web


def postprocess_web_data(df_team_parsed: pd.DataFrame) -> pd.DataFrame:

    df_team_parsed["Title"] = df_team_parsed["Title"].str.replace("-", "|")
    df_team_parsed["Title"] = df_team_parsed["Title"].str.split("|").str[1:].str.join("|").str.replace("Linkedin", "")

    return df_team_parsed


def append_new_profiles(df_csv_web: pd.DataFrame, df_team_parsed: pd.DataFrame):

    df_team = pd.concat([df_csv_web[~df_csv_web["LinkedIn"].isin(df_team_parsed["LinkedIn"])], df_team_parsed], axis=0)
    df_team = df_team.sort_values("Membership Number", ascending=True)
    return df_team
