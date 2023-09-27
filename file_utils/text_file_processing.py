"""This module provides functions to extract text from text files.
The module currently supports files with the extensions "txt", ".csv", and ".tsv"."""

from csv import reader
from chardet import detect_all
from xml.etree.ElementTree import parse as parse_xml
import pysrt
from nltk.data import load
from nltk.tokenize.punkt import PunktSentenceTokenizer
from bs4 import BeautifulSoup
from file_utils.pdf_file_processing import tokenize_text


def process_text_files(text_files: list[str]) -> list[str]:
    """Extracts the text from text files.
    The function supports files with the extensions ".txt", ".csv", and ".tsv".

    Args:
        - text_file (str): The path of the text file to extract text from.

    Returns:
        - list[str]: Extracted text."""

    extracted_text: list[str] = []

    for text_file in text_files:
        if text_file.endswith(".csv"):
            extracted_text.extend(_process_csv(text_file))

        elif text_file.endswith(".tsv"):
            extracted_text.extend(_process_tsv(text_file))

        elif text_file.endswith(".xml"):
            extracted_text.extend(_process_xml(text_file))

        elif text_file.endswith(".html"):
            extracted_text.extend(_process_html(text_file))

        elif text_file.endswith(".srt"):
            tokenizer = load("tokenizers/punkt/english.pickle")
            extracted_text.extend(_process_srt(text_file, tokenizer))

        else:
            extracted_text.extend(_default_file_process(text_file))

    return extracted_text


def _default_file_process(file: str) -> list[str]:
    """Default extractor for text files. 

    Args:
        - file (str): File to be processed.

    Returns:
        - list[str]: Extracted text."""

    with open(file, "rb") as f:
        file_data = detect_all(f.read())

    for data in file_data:
        try:
            with open(file, "r", encoding=data["encoding"]) as f:
                extracted_text = f.readlines()
                return extracted_text

        except UnicodeDecodeError:
            continue

    return []


def _process_csv(file: str) -> list[str]:
    """Extracts text from .csv files using stream processing.

    Args:
        - file (str): .csv file to be processed.

    Returns:
        - list[str]: Extracted text."""

    extracted_text: list[str] = []

    with open(file, "r", newline="") as csv_file:
        csv_reader = reader(csv_file)
        for row in csv_reader:
            extracted_text.extend(row)

    return extracted_text


def _process_tsv(file: str) -> list[str]:
    """Extracts text from .tsv files using stream processing.

    Args:
        - file (str): .tsv file to be processed.

    Returns:
        - list[str]: Extracted text."""

    extracted_text: list[str] = []

    with open(file, "r", newline="") as tsv_file:
        tsv_reader = reader(tsv_file, delimiter="\t")
        for row in tsv_reader:
            extracted_text.extend(row)

    return extracted_text


def _process_xml(file: str) -> list[str]:
    """Extracts text from an XML file and removes tags.

    Args:
        - file (str): XML file to be processed.

    Returns:
        - str: Extracted text."""

    tree = parse_xml(file)
    root = tree.getroot()

    return [element.text for element in root.iter() if element.text]


def _process_html(file: str) -> list[str]:
    """Extracts text from an HTML file and removes tags.

    Args:
        - file (str): HTML file to be processed.

    Returns:
        - list[str]: Extracted text."""

    with open(file, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    return soup.get_text(separator="\n").split("\n")


def _process_srt(file: str, tokenizer: PunktSentenceTokenizer) -> list[str]:
    """Extracts and tokenizes text into sentences from an .srt file.

    Args:
        - file (str): .srt file to be processed.

    Returns:
        - list[str]: Extracted and tokenizes subtitle content."""

    srt_file = pysrt.open(file)
    subtitles: list[str] = [(sub.text).replace("\n", " ") for sub in srt_file]

    return tokenize_text(subtitles, tokenizer)
