"""This module provides functions for processing PDF files.
Specifically, it includes a function for extracting all text from a PDF file
and another function for tokenizing the extracted text into sentences."""

from re import sub
from typing import Generator
from nltk.data import load
from nltk.tokenize.punkt import PunktSentenceTokenizer
from fitz import Document


def process_pdf_files(files: list[str]) -> list[str]:
    """Processes a list of PDF files, extracting all text and tokenizing it into sentences.

    Args:
        - pdf_file (str): File paths for the PDF file to be processed.

    Returns:
        - list[str]: A list of all sentences extracted from the PDF files."""

    tokenizer = load("tokenizers/punkt/english.pickle")

    extracted_text = []
    for file in files:
        extracted_text.extend(_process_pdf_file(file))

    sentences = tokenize_text(extracted_text, tokenizer)

    return sentences


def _process_pdf_file(file: str) -> list[str]:
    return list(_extract_text_from_pdf(file))


def _extract_text_from_pdf(pdf_file: str) -> Generator[str, None, None]:
    """Extracts all text from a given PDF file.

    Args:
        - pdf_file (str): A file path for the PDF file to be processed.

    Returns:
        - list[str]: All text extracted from the PDF file."""

    with Document(pdf_file) as pdf:
        for page in pdf:
            page_text = page.get_text(sort=True)
            yield page_text


def tokenize_text(text: list[str], tokenizer: PunktSentenceTokenizer) -> list[str]:
    """Tokenizes provided text into sentences.
    Note: currently this uses data for English language and may not work perfectly for others.

    Args:
        - text (list[str]): Text to be tokenized.

    Returns:
        - list[str]: List of sentences extracted from the text."""

    extracted_text = " ".join(text)
    extracted_text = sub(r"\s+", " ", extracted_text)

    return tokenizer.tokenize(extracted_text)
