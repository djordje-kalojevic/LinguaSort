"""Extracts text from various file formats, and divides that text based on language.

The following file formats are currently supported:
- Word (.docx, and .doc)
- PDF (.pdf)
- Text (.txt, .csv, and .tsv)
- Excel (.xls, .xlsx, and .xlsm)
- OpenDocument Spreadsheet format (.ods)
- XML and HTML (.xml and .html)
- Subtitles (.srt)"""

from gui import settings_selection
from file_utils.file_processing import browse_files, process_files
from text_processing import process_text, save_report
from language_detect import detect_language


def lingua_sorter():
    """GUI-based library LinguaSort is a Python library designed to simplify text extraction
    from various file formats and/or organize the extracted text based on language."""

    selected_languages, options, operation_type = settings_selection()

    if not operation_type:
        return

    files = browse_files()
    extracted_text = process_files(files)
    processed_text = process_text(extracted_text, options)

    if operation_type == "language_check":
        predictions = detect_language(processed_text, selected_languages)

    elif operation_type == "text_extraction":
        predictions = None

    save_report(processed_text, predictions)


if __name__ == "__main__":
    lingua_sorter()
