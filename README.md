LinguaSort is a Python library designed to simplify text extraction from various file formats. Additionally it can organize the extracted text based on its language. This is done on a segment by segment basis. Segments are smaller chunks of text, typically sentences, or text otherwise separated by new lines, such as titles and list items.

## Features

- Text extraction from a variety of file formats, including:
  - Word files (.docx and .doc)<sup>1</sup>
  - PDF files
  - Plain Text files (.txt)
  - Comma-Separated Values (.csv)
  - Tab-Separated Values (.tsv)
  - Excel files (.xls, .xlsx, and .xlsm)
  - OpenDocument Spreadsheet (.ods)
  - XML and HTML files<sup>2</sup>
  - Subtitles files (.srt)

- Automatic language-based text sorting:
  The extracted text is sorted and grouped based on the language it is written in.

<sup>1</sup>Requires MS Word or WPS Kingsoft suite. Additionally, .doc files are considerably slower to process so it is recommended to convert them to .docx first

<sup>2</sup>tags are not extracted, only the text between them is

## Supported Languages

LinguaSort utilizes the power of the [Lingua language detector](https://github.com/pemistahl/lingua-py) to provide accurate language detection. As a result, LinguaSort supports a wide range of languages, 75 languages currently, enabling efficient sorting across diverse text content.

## Usage

There are two ways of accessing LinguaSort:

1. **Install LinguaSort by cloning or downloading this repository**

2. **Import the library and use it to process your files:**

   ```python
   from linguasort import lingua_sorter

   lingua_sorter()
   ```

## Real-world application

As part of my job responsibilities, I was assigned the task of extracting and sorting text from ~6,200 pages of PDF files and ~150 pages of Word files for a specific project. Typically, undertaking such a task would require the entire department's efforts and over three weeks time. However, utilizing a prior version of this script, I managed to complete this task independently in less than 1.5 hours. This timeframe also included an additional quality check to ensure that the script produced error-free results.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit an issue or pull request right here on GitHub!

---
*Disclaimer: LinguaSort utilizes the Lingua language detector to support a wide range of languages. For more information about Lingua and its supported languages, please visit the [Lingua GitHub repository]((https://github.com/pemistahl/lingua-py)).*