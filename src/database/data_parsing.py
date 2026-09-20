import typing
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from database.helper import get_color_key


def parse_legacy_data(path: Path) -> pd.DataFrame:
    measurement_years = [
        str(i) for i in range(1970, datetime.now(ZoneInfo("America/New_York")).year)
    ]
    sheets_in_excel = pd.ExcelFile(path).sheet_names
    years_with_data = [sheet for sheet in sheets_in_excel if sheet in measurement_years]
    parsed_years: list[pd.DataFrame] = []
    for year in years_with_data:
        df_sheet_data = pd.read_excel(path, sheet_name=year, header=None)
        df_filled_in_sheet_data = _fill_in_sheet_using_color(
            worksheet=load_workbook(path, data_only=True)[year],
            sheet_data=df_sheet_data,
        )
        parsed_years.append(_parse_year(df_filled_in_sheet_data, year))
    return pd.concat(parsed_years)


def _fill_in_sheet_using_color(
    worksheet: Worksheet, sheet_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Maintaners of the input excel used a coloring scheme of the following form:
        1. The first day a berth is rented, the cell for that day is filled in with
           the renters name.
        2. Following days still under renters name are colored in matching color of
           the first cell.

    This function flattens that to just just have the renter name in each day-berth name combo
    """
    color_grid = [
        [get_color_key(cell) for cell in row] for row in worksheet.iter_rows()
    ]
    rows_containing_rental_info = sheet_data.loc[
        sheet_data.iloc[:, 0].str.contains("-")
    ]
    for i, row in rows_containing_rental_info.iterrows():
        i = typing.cast(int, i)
        row_coloring = color_grid[i]
        sheet_data.loc[i] = _fill_row_using_color(row, row_coloring)

    return sheet_data


def _fill_row_using_color(row: pd.Series, row_coloring: list) -> list[str]:
    result = row.tolist()
    current_text = None
    current_color = None

    for i, (value, color) in enumerate(zip(row, row_coloring)):
        has_text = pd.notna(value) and str(value) != ""
        is_colored = color is not None

        if has_text and is_colored:
            current_text = value
            current_color = color
        elif current_text is not None and color == current_color:
            result[i] = current_text
        else:
            current_text = None
            current_color = None

    return result


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
