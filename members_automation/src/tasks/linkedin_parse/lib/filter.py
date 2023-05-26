import pandas as pd
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_eligible_profiles(
        df_spreadsheet_members: pd.DataFrame,
        df_csv_web: pd.DataFrame,
        max_profiles_update: int) -> pd.DataFrame:

    df = df_spreadsheet_members[["Name", "LinkedIn", "In Web Page", "status"]]
    df_csv_web = df_csv_web.drop(columns=["In Web Page", "status"])
    df = pd.merge(df, df_csv_web, on=["LinkedIn", "Name"], how="left")
    df["top_profiles"] = ((df["Title"].isna()) | (df["picfile"].isna()) | (df["last_updated"].isna())) & (~df["LinkedIn"].isna())
    df = df[df["top_profiles"]]
    #df = df.sort_values(by=["top_profiles", "last_updated"], ascending=[False, True])
    df = df.drop("top_profiles", axis=1)
    df = df.head(max_profiles_update)

    return df
