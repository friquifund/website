import pandas as pd
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_eligible_profiles(
        df_spreadsheet_members: pd.DataFrame,
        df_csv_web: pd.DataFrame,
        max_profiles_update: int) -> pd.DataFrame:


    df = df_spreadsheet_members[["name", "linkedin"]]
    df = pd.merge(df, df_csv_web, on=["linkedin", "name"], how="left")
    df["top_profiles"] = ((df["title"].isna()) | (df["picfile"].isna()) | (df["last_updated"].isna())) & (~df["linkedin"].isna())
    df = df.sort_values(by=["top_profiles", "last_updated"], ascending=[False, True])
    df = df.drop("top_profiles", axis=1)
    df = df.head(max_profiles_update)

    return df
