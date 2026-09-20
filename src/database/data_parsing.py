import typing
from datetime import date, datetime
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
    parsed_year["date"] = [
        date(
            year=int(row.year),
            month=datetime.strptime(row.month, "%B").month,
            day=int(row.day),
        )
        for row in parsed_year.itertuples()
    ]
    return parsed_year


def _extract_month_chunks(df_year: pd.DataFrame, year: str) -> list[pd.DataFrame]:
    index_column = df_year.iloc[:, 0]
    month_matches = index_column.astype("string").str.match(
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
        + rf"(?:\s+{year})?\s*$",
        case=False,
        na=False,
    )
    month_block_positions = [
        position for position, is_month in enumerate(month_matches) if is_month
    ]
    # dump the first chunk as it contains no data
    month_blocks = [
        pd.DataFrame(month) for month in np.split(df_year, month_block_positions)[1:]
    ]
    parsed_year: list[pd.DataFrame] = []
    for month in month_blocks:
        # below is trustworthy given top left entry guaranteed to be
        # MONTH YYYY by construction
        month_name = month.iloc[0, 0].split(" ")[0]
        coerced_month = _coerce_month_to_expected_database_shape(month)
        coerced_month["month"] = month_name
        parsed_year.append(coerced_month)
    return parsed_year


def _coerce_month_to_expected_database_shape(month: pd.DataFrame) -> pd.DataFrame:
    day_label_row = month.iloc[0].iloc[1:]
    if not pd.to_numeric(day_label_row, errors="coerce").notna().any():
        day_label_row = month.iloc[1].iloc[1:]
    day_labels = pd.Series(
        pd.to_numeric(day_label_row, errors="coerce").to_numpy(),
        index=month.columns[1:],
    )
    reservation_rows = month[month.iloc[:, 0].str.contains("-")]

    parsed_rows: list[pd.DataFrame] = []
    for i, row in reservation_rows.iterrows():
        dock_name, dock_size = [item.strip() for item in str(row[0]).split("-")]
        # TODO: a lot of this should really use named types better for
        #       easier reading of the various parsing ops
        # day: int, reserved_by: str
        dates_reserved = row.iloc[1:].dropna()
        dates_reserved.index = day_labels.loc[dates_reserved.index]
        dates_reserved = dates_reserved[dates_reserved.index.notna()].to_dict()
        df_parsed_row = pd.DataFrame(
            {
                "day": [int(key) for key in dates_reserved],
                "reserved_by": dates_reserved.values(),
            }
        )
        df_parsed_row["dock_name"] = dock_name
        df_parsed_row["dock_size"] = dock_size.strip("'")
        df_parsed_row["dock_size_metric"] = "ft"
        parsed_rows.append(df_parsed_row)

    return pd.concat(parsed_rows)
