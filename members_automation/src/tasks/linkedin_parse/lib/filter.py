import pandas as pd
from typing import List
from datetime import datetime
import dateutil


def get_eligible_profiles(
        df_spreadsheet_members: pd.DataFrame,
        df_csv_web: pd.DataFrame,
        max_profiles_update: int) -> pd.DataFrame:

    df = df_spreadsheet_members[["name", "linkedin"]]
    df = pd.merge(df, df_csv_web[["linkedin", "last_updated"]], on="linkedin", how="left")
    df = df.sort_values("last_updated", ascending=True, na_position="first")
    df = df.head(max_profiles_update)

    return df
