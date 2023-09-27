"""This module provides functions to process a list of Word files and extract their text.
The module currently supports files with the extensions ".docx", ".doc".

Note: .doc files are supported but they are not recommended
as they are significantly slower to process than .docx files.
Additionally, further testing is required to conclude
whether all text is successfully extracted.
Thus, it is recommended to convert them to .docx before processing."""

from docx2txt import process
from winreg import OpenKey, CloseKey, HKEY_CLASSES_ROOT
from win32com.client import Dispatch


def process_docx_files(files: list[str]) -> list[str]:
    """Processes docx files by extracting all text from them.

    Args:

        - docx_file (str): Files for processing.

    Returns:
        - list[str]: Extracted text from files."""

    text = []
    for file in files:
        text.extend(process(file).split("\n"))

    return text


def process_doc_files(doc_files: list[str]) -> list[str]:
    """Processes the given .doc file by extracting all text from it.

    Args:
        - doc_file (str): File for processing.

    Returns:
        - list[str]: Extracted text."""

    if _is_word_installed():
        program = Dispatch("Word.Application")

    elif _is_wps_installed():
        program = Dispatch("kwps.Application")

    else:
        print("No compatible program found to process .doc files, "
              "please convert them to .docx before continuing.")
        return []

    extracted_text: list[str] = []

    for doc_file in doc_files:
        extracted_text.extend(_process_doc_file(program, doc_file))

    return extracted_text


def _process_doc_file(program, doc_file: str) -> list[str]:
    doc = program.Documents.Open(doc_file)

    return [paragraph.Range.Text for paragraph in doc.Paragraphs]


def _is_word_installed() -> bool:
    """Checks whether MS Word is installed on the machine.

    Returns:
        - bool: True if MS Word is installed, False if not."""

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, "Word.Application")
        CloseKey(key)
        return True

    except WindowsError:
        return False


def _is_wps_installed() -> bool:
    """Checks whether Kingsoft WPS is installed on the machine.

    Returns:
        - bool: True if Kingsoft WPS is installed, False if not."""

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, "Kwps.Application")
        CloseKey(key)
        return True

    except WindowsError:
        return False
