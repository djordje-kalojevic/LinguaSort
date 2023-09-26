"""This module provides functions for detecting the language of given text."""

from lingua import Language, LanguageDetectorBuilder
from pandas import Series
from alive_progress import alive_bar


def detect_language(text_to_check: Series, languages: list[Language]) -> Series:
    """Performs the language detection process on the given text.

    Args:
        - text_to_check (Series): Strings to perform the check on
        - languages(list[str]): Languages selected by the user,
        representing the languages selected by the user.

    Returns:
        - Series: Containing all language predictions"""

    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    predictions = []

    with alive_bar(total=len(text_to_check),
                   spinner="classic",
                   title="Language detection:") as progress_bar:
        for text in text_to_check:
            predictions.append(str(detector.detect_language_of(text)))
            progress_bar()  # pylint: disable=not-callable

    return Series(map(_format_prediction_output, predictions))


def _format_prediction_output(prediction: str):
    """Language predictions by Lingua Language Detector use the following format
    "Language.ENGLISH" this function removes the "Language." prefix."""

    if prediction.startswith("Language."):
        prediction = prediction.split(".")[1]

    return prediction
