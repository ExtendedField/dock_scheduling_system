from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


def parse_legacy_data(path: Path) -> pd.DataFrame:
    measurement_years = [
        str(i) for i in range(1970, datetime.now(ZoneInfo("America/New_York")).year)
    ]
    sheets_in_excel = pd.ExcelFile(path).sheet_names
    years_with_data = [sheet for sheet in sheets_in_excel if sheet in measurement_years]
    parsed_years: list[pd.DataFrame] = []
    for year in years_with_data:
        parsed_years.append(_parse_year(pd.read_excel(path, sheet_name=year)))
    return pd.concat(parsed_years)


def _parse_year(df_year_sheet: pd.DataFrame) -> pd.DataFrame:
    df_year_sheet.dropna(inplace=True, how="all")
    print(df_year_sheet.head())
    print(df_year_sheet.columns)
    # chunk sheets by month
    # loop through month and extract reservation history
    return pd.DataFrame()
