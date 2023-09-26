"""This module provides functions for extracting text from files in PDF, Excel, and Word formats.
The following file formats are currently supported:
- Word (.docx, and .doc)
- PDF (.pdf)
- Text (.txt, .csv, and .tsv)
- Excel (.xls, .xlsx, and .xlsm)
- OpenDocument Spreadsheet format (.ods)
- XML and HTML (.xml and .html)
- Subtitles (.srt)

Note: .doc files are supported but they are not recommended
as they are significantly slower to process than .docx files.
Thus, it is recommended to convert them to .docx before processing."""

from dataclasses import dataclass
from tkinter.filedialog import askopenfilenames
from alive_progress import alive_bar
from file_utils.word_file_processing import process_docx_files, process_doc_files
from file_utils.spreadsheets_file_processing import process_excel_files
from file_utils.text_file_processing import process_text_files
from file_utils.pdf_file_processing import process_pdf_files


SUPPORTED_WORD_FORMATS = [".doc", ".docx"]
SUPPORTED_SPREADSHEET_FORMATS = [".xls", ".xlsx", ".xlsm", ".ods"]
SUPPORTED_TEXT_FORMATS = [".txt", ".csv", ".tsv",
                          ".srt", ".log", ".xml", ".html"]
ALL_SUPPORTED_FORMATS = (SUPPORTED_WORD_FORMATS +
                         SUPPORTED_SPREADSHEET_FORMATS +
                         SUPPORTED_TEXT_FORMATS + [".pdf"])


def browse_files() -> list[str]:
    """Launches a file dialog that allows the user to select one or more files.
    If the user cancels the dialog, the program exits.

    Returns:
        A list of strings representing the paths of the selected files."""

    filetypes = (
        ("All supported filetypes", ALL_SUPPORTED_FORMATS),
        ("Word files", SUPPORTED_WORD_FORMATS),
        ("Excel files", SUPPORTED_SPREADSHEET_FORMATS),
        ("Text files", SUPPORTED_TEXT_FORMATS),
        ("PDF files", ".pdf"),
    )

    files = askopenfilenames(title="Choose files", filetypes=filetypes)

    if not files:
        raise SystemExit

    return [file.lower() for file in files]


def process_files(files: list[str]) -> list[str]:
    """Processes a list of files and extracts text from supported file types.

    Args:
        - files (list[str]): File paths to process.

    Returns:
        - list[str]: Extracted text from the processed files."""

    sorted_files = _FileSorter(files)

    text = []

    with alive_bar(spinner="classic",
                   title="File preprocessing:") as progress_bar:

        if sorted_files.docx_files:
            text.extend(process_docx_files(sorted_files.docx_files))

        if sorted_files.doc_files:
            text.extend(process_doc_files(sorted_files.doc_files))

        if sorted_files.spreadsheets:
            text.extend(process_excel_files(sorted_files.spreadsheets))

        if sorted_files.text_files:
            text.extend(process_text_files(sorted_files.text_files))

        if sorted_files.pdf_files:
            text.extend(process_pdf_files(sorted_files.pdf_files))

        progress_bar()

    return text


@dataclass
class _FileSorter():
    """Sorts files based on their extensions."""

    def __init__(self, files: list[str]) -> None:
        self._sort_files(files)

    def _sort_files(self, files: list[str]):
        self.spreadsheets: list[str] = []
        self.text_files: list[str] = []
        self.pdf_files: list[str] = []
        self.docx_files: list[str] = []
        self.doc_files: list[str] = []

        for file in files:
            extension = "." + file.split(".")[-1]

            if extension == ".docx":
                self.docx_files.append(file)
            elif extension == ".doc":
                self.doc_files.append(file)
            elif extension in SUPPORTED_SPREADSHEET_FORMATS:
                self.spreadsheets.append(file)
            elif extension in SUPPORTED_TEXT_FORMATS:
                self.text_files.append(file)
            elif extension == ".pdf":
                self.pdf_files.append(file)
