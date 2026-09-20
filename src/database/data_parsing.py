from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import openpyxl as oxl


def parse_legacy_data(path: Path) -> pd.DataFrame:
    measurement_years = [
        str(i) for i in range(1970, datetime.now(ZoneInfo("America/New_York")).year)
    ]
    sheets_in_excel = pd.ExcelFile(path).sheet_names
    years_with_data = [sheet for sheet in sheets_in_excel if sheet in measurement_years]
    parsed_years: list[pd.DataFrame] = []
    for year in years_with_data:
        parsed_years.append(
            _parse_year(pd.read_excel(path, sheet_name=year, header=None), year)
        )
    return pd.concat(parsed_years)


def _parse_year(df_year_sheet: pd.DataFrame, year: str) -> pd.DataFrame:
    df_year_sheet.dropna(inplace=True, how="all")
    month_chunks = _extract_month_chunks(df_year_sheet, year)
    parsed_year = pd.concat(month_chunks)
    parsed_year["year"] = year
    return parsed_year


def _extract_month_chunks(df_year: pd.DataFrame, year: str) -> list[pd.DataFrame]:
    index_column = df_year.iloc[:, 0]
    month_block_indicies = index_column.loc[index_column.str.contains(year)].index
    # dump the first chunk as it contains no data
    month_blocks = [
        pd.DataFrame(month) for month in np.split(df_year, month_block_indicies)[1:]
    ]
    parsed_year: list[pd.DataFrame] = []
    for month in month_blocks:
        coerced_month = _coerce_month_to_expected_database_shape(month)
        coerced_month["month"] = month
        parsed_year.append(coerced_month)
    return parsed_year


def _coerce_month_to_expected_database_shape(month: pd.DataFrame) -> pd.DataFrame:
    print(month)
    print(month.T)
    # day of the month is the index if this works

