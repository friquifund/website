import gspread
import pandas as pd
from typing import Dict, List


class Gspread:
    def __init__(self, dict_credentials: Dict[str, str]):
        #self.gc = gspread.service_account_from_dict(dict_credentials)
        self.gc = gspread.service_account_from_dict(dict_credentials)

    def read_spreadsheet(self, url: str, columns: List[str] = None) -> pd.DataFrame:
        records = self.gc.open_by_url(url).get_worksheet(0).get_all_values()

        if columns is None:
            columns = [records[0][i] for i in range(len(records[0]))]
            columns = [x for x in columns if x != ""]

        cols_index = [index for index, value in enumerate(records[0]) if value in set(columns)]

        data_values = [[row[i] for i in cols_index] for row in records[1:]]
        column_fields = [records[0][i] for i in cols_index]

        df = pd.DataFrame.from_records(data_values, columns=column_fields)
        return df

    def write_spreadsheet(self, df: pd.DataFrame, url: str):
        # Open the spreadsheet by URL
        spreadsheet = self.gc.open_by_url(url)

        # Select the desired worksheet
        worksheet = spreadsheet.get_worksheet(0)

        # Clear the existing data in the sheet
        worksheet.clear()

        # Write the DataFrame header as the first row
        worksheet.append_row(df.columns.tolist())

        # Write the DataFrame rows
        worksheet.append_rows(df.values.tolist())

        return None
