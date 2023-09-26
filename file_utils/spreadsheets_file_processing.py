"""This module provides functions to extract text from Excel files.
The module currently supports files with the extensions ".xls", ".xlsx", ".xlsm", and ".ods"."""

from pandas import read_excel, concat


def process_excel_files(excel_files: list[str]) -> list[str]:
    """Extracts text from Excel files.
    The function supports files with the extensions ".xls", ".xlsx", ".xlsm", and ".ods".
    Engine is automatically determined based on the input file. 

    Args:
        - excel_file (str): Excel file to be processed.

    Returns:
        - list[str]: Extracted text from all Excel files."""

    extracted_text: list[str] = []

    for excel_file in excel_files:
        extracted_text.extend(_process_excel_file(excel_file))

    return extracted_text


def _process_excel_file(excel_file: str) -> list[str]:
    """Extracts text from an Excel file.
    The function supports files with the extensions ".xls", ".xlsx", ".xlsm", and ".ods".
    Engine is automatically determined based on the input file type. 

    Args:
        - excel_file (str): Excel file to be processed.

    Returns:
        - list[str]: Extracted text from file."""

    sheet_dfs = read_excel(excel_file,
                           header=None,
                           sheet_name=None,
                           engine=None,
                           dtype_backend="pyarrow")

    combined_df = concat(sheet_dfs.values(), ignore_index=True)
    extracted_text = concat([combined_df[c] for c in combined_df.columns])

    return extracted_text.tolist()
