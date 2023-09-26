"""This module defines functions used to process text data by filtering out
entries that do not contain any translatable text.

This includes removing:
- hyperlinks,
- non-letter patterns,
- SI units,
- other various untranslatables."""

import re
from os import system
from typing import Optional
from pandas import DataFrame, Series
from numpy import array_split


def process_text(text: list[str], options: dict[str, bool]) -> Series:
    """Processes the extracted text and filters out invalid entries.

    Args:
        - text (list[str]): Extracted text.

    Returns:
        - list[str]: List of filtered text data."""

    series = Series(text).astype('string').str.strip()
    series = series.replace("\s+", " ")

    if options["Remove repetitions"]:
        series = Series(series.unique())

    series = series.replace("", None).dropna(how="any")

    if options["Remove untranslatables"]:
        series = _remove_untranslatables(series)

    if options["Remove measurements"]:
        series = _remove_measurements(series)

    if options["Remove hyperlinks"]:
        series = _remove_hyperlinks(series)

    return series.str.strip().dropna(how="any")


def _remove_untranslatables(series: Series) -> Series:
    """Cleans the given Pandas Series by removing lines that
    only contain numbers, sand other non-translatable text.

    Args:
        - series: Pandas Series.

    Returns:
        - Series: A new Pandas Series object with cleaned text."""

    pattern = re.compile(r"(?i)^[\W\d_xX]*?([A-Z])?(\s|\d)*?[\W\d_xX]*?$")
    series = series.replace(pattern, None, regex=True)

    pattern = re.compile(r"(?i)^(?:[a-z]{,3}\d+[a-z]{,3}\d*)+|"
                         r"(?:\d+[a-z]{,3}\d+[a-z]{,3})+$")

    return series.replace(pattern, None, regex=True)


def _remove_measurements(series: Series) -> Series:
    """Removes SI units and measurements from the given Pandas Series.

    Args:
        - series: Pandas Series.

    Returns:
        - Series: A new Pandas Series with measurements removed."""

    pattern = re.compile(
        r"(?i)^\d+(?:\.\d+)?(?:\s*[eE][+-]?\d+)?\s*"
        r"(?:\b(?:M|k|m|c)?(?:m|g|s|A|Hz|N|Pa|J|W|V|F|Ω|S|T|H|lm|lx)\b)$")

    return series.replace(pattern, None, regex=True)


def _remove_hyperlinks(series: Series) -> Series:
    """Removes hyperlinks from the given Pandas Series.

    Args:
        - series: Pandas Series.

    Returns:
        - Series: A new Pandas Series with hyperlinks removed."""

    pattern = re.compile(r"(?i)^(www\.|https?://)\S+$")

    return series.replace(pattern, None, regex=True)


def save_report(processed_text: Series, predictions: Optional[Series]) -> None:
    """Saves extracted text, along with any language predictions, if there were any.
    Currently this is saved to a Excel file.

    Args:
        - processed_text (Series): Pandas Series representing extracted and processed text.

    Returns:
        - Series: A new Pandas Series with hyperlinks removed."""

    if isinstance(predictions, Series):
        zipped = list(zip(predictions, processed_text))
        df = DataFrame(zipped, columns=["Prediction", "Text"])
    else:
        df = DataFrame(processed_text)

    if len(df) < 750_000:
        df.to_excel("df.xlsx", header=False, index=False, engine="xlsxwriter")
        system("df.xlsx")
        return

    chunks: list[DataFrame] = array_split(df, len(df) // 750_000)
    for i, chunk in enumerate(chunks):
        chunk.to_excel(f"df{i}.xlsx", index=False, engine="xlsxwriter")
