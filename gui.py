from dataclasses import dataclass
import pickle
from typing import Optional
from PyQt6.QtWidgets import (QApplication, QWidget, QListWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QCheckBox,
                             QLabel, QListWidgetItem, QStyle,
                             QFormLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QSize
from lingua import Language
from qdarktheme import setup_theme
from darkdetect import isDark


ADVANCED_OPTIONS = {
    "Remove repetitions":
    ("Can greatly speed up the process by removing repetitions from extracted text. "
     "Recommended unless repetitions are truly needed."),
    "Remove untranslatables":
    "Can speed up the process by removing untranslatables from extracted text.",
    "Remove measurements":
    "Can speed up the process by removing SI units and measurements from extracted text.",
    "Remove hyperlinks":
    "Can speed up the process by removing hyperlinks from extracted text."
}


class _MainWindow(QWidget):
    """Custom searchable widget for displaying and selecting multiple languages."""

    def __init__(self, languages: list[str]) -> None:
        super().__init__()
        self.setWindowTitle("LinguaSort")
        self.selected_languages: list[str] = []
        self.checkboxes: list[QCheckBox] = []
        self.selected_settings: dict[str, bool] = {}
        self.operation_type: Optional[str] = None

        self.language_listbox = QListWidget(self)
        self.language_listbox.addItems(languages)
        self.language_listbox.sortItems()
        self.language_listbox.itemClicked.connect(self._select_language)
        self.language_listbox.itemClicked.connect(self._enable_buttons)

        self.selection_listbox = QListWidget(self)
        self.selection_listbox.itemClicked.connect(self._deselect_language)
        self.selection_listbox.itemClicked.connect(self._enable_buttons)

        buttons = QHBoxLayout()
        self.extract_button = QPushButton("Extract text only", self)
        self.extract_button.clicked.connect(self._extract_text_only)
        self.extract_button.setEnabled(True)
        self.confirm_button = QPushButton("Confirm Selection", self)
        self.confirm_button.clicked.connect(self._confirm_selection)
        self.confirm_button.setEnabled(False)

        buttons.addWidget(self.extract_button)
        buttons.addWidget(self.confirm_button)

        self.checkboxes_layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.language_listbox)
        horizontal_layout.addWidget(self.selection_listbox)

        self._add_checkboxes()

        vertical_layout = QVBoxLayout()
        self.search_bar = _SearchBar(self)
        vertical_layout.addWidget(self.search_bar)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addLayout(self.checkboxes_layout)
        vertical_layout.addLayout(buttons)
        self.setLayout(vertical_layout)

    def _select_language(self, language: QListWidgetItem) -> None:
        """Check if language already exists in the selection listbox,
        if not moves the clicked language to it."""

        self.language_listbox.takeItem(self.language_listbox.row(language))
        self.selection_listbox.addItem(language.text())
        self.selection_listbox.sortItems()

    def _deselect_language(self, language: QListWidgetItem) -> None:
        """Removes the clicked language from the selection listbox."""

        self.selection_listbox.takeItem(self.selection_listbox.row(language))
        self.language_listbox.addItem(language.text())
        self.language_listbox.sortItems()

    def _enable_buttons(self):
        """Enables/disables buttons for either text extraction,
        or text extraction + language detection,
        based on the number of selected languages,
        as at least two languages are needed for language detection."""

        selected_items = self.selection_listbox.findItems("",
                                                          Qt.MatchFlag.MatchStartsWith)
        if len(selected_items) > 1:
            self.confirm_button.setEnabled(True)
            self.extract_button.setEnabled(False)

        else:
            self.confirm_button.setEnabled(False)
            self.extract_button.setEnabled(True)

    def _extract_text_only(self):
        self.selected_languages = []
        self.selected_settings = self._get_selected_settings()
        self.operation_type = "text_extraction"
        self.close()

    def _confirm_selection(self) -> None:
        """Confirms the selection from the selection listbox and checkboxes."""

        selected_items = self.selection_listbox.findItems("",
                                                          Qt.MatchFlag.MatchStartsWith)
        self.selected_languages = [item.text() for item in selected_items]
        self.selected_settings = self._get_selected_settings()
        self.operation_type = "language_check"
        self.close()

    def _add_checkboxes(self) -> None:
        """Adds a checkbox with the given label and tooltip text to the checkboxes layout."""

        self.checkbox_data = ADVANCED_OPTIONS
        for label, tooltip_text in self.checkbox_data.items():
            checkbox = _CheckBox(self, label, tooltip_text)
            self.checkboxes_layout.addWidget(checkbox)

    def _get_selected_settings(self) -> dict[str, bool]:
        """Returns a list of the text of the checked checkboxes."""

        for box in self.checkboxes:
            self.selected_settings[box.text()] = box.isChecked()

        return self.selected_settings


class _CheckBox(QWidget):
    """A custom widget for displaying a checkbox with tooltip."""

    def __init__(self, parent: _MainWindow, label: str,
                 tooltip_text: str, checked=True, icon_size=QSize(16, 16)) -> None:
        super().__init__(parent)

        form_layout = QFormLayout()
        self.checkbox = QCheckBox(label)
        parent.checkboxes.append(self.checkbox)
        self.checkbox.setChecked(checked)
        self.tooltip = QLabel()

        pixmap_name = QStyle.StandardPixmap.SP_MessageBoxQuestion
        pixmap = parent.style().standardPixmap(pixmap_name)
        resized_pixmap = pixmap.scaled(icon_size,
                                       Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
        self.tooltip.setPixmap(resized_pixmap)
        self.tooltip.setToolTip(tooltip_text)

        form_layout.addRow(self.checkbox, self.tooltip)
        self.setLayout(form_layout)


class _SearchBar(QWidget):
    """A custom search bar widget."""

    def __init__(self, parent: _MainWindow) -> None:
        super().__init__(parent)
        self.all_items = parent.language_listbox.findItems("",
                                                           Qt.MatchFlag.MatchStartsWith)

        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedWidth(200)
        self.search_bar.setPlaceholderText("Search languages")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.textChanged.connect(self._search)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.search_bar)
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(horizontal_layout)

    def _search(self, search_text: str) -> None:
        """Filters languages based on the input."""

        for item in self.all_items:
            if search_text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)


def _configure_theme(theme: Optional[str] = None) -> None:
    """Configures the program's theme based on the OS theme or an explicit overwrite value.
    Includes fixes for barely visible tooltip text in the dark theme.

    Args:
        - theme_overwrite (str): Use "dark" or "light" to explicitly set the theme,
                         regardless of the OS theme."""

    if isDark() or theme == "dark":
        setup_theme("dark",
                    additional_qss="QToolTip {color: black; font-size: 14px}")
    else:
        setup_theme("light", additional_qss="QToolTip {font-size: 14px}")


def settings_selection(theme: Optional[str] = None) -> tuple[list[Language], dict[str, bool], Optional[str]]:
    """Provides GUI which allows the user to select languages, as well as advanced options.
    Configures the program's theme based on the OS theme.
    Use "dark" or "light" to explicitly set the theme, regardless of the OS theme.

    Returns:
        - selected_languages (list[Language]): Selected languages
        - selected_settings (dict[str, bool]): Selected advanced settings."""

    with open("resources/supported_languages.pickle", "rb") as data:
        languages_data: dict[str, Language] = pickle.load(data)

    languages_labels = list(languages_data.keys())

    app = QApplication([])
    _configure_theme(theme)
    window = _MainWindow(languages_labels)
    window.show()
    app.exec()

    selected_languages = [languages_data[l] for l in window.selected_languages]

    return selected_languages, window.selected_settings, window.operation_type


@dataclass
class InfoDialog(QDialog):

    def __init__(self, message, title: str = " "):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(400, 150)

        self.message_label = QLabel(message, self)
        self.message_label.setWordWrap(True)

        self.message_box = QMessageBox(self)
        self.message_box.setIcon(QMessageBox.Icon.Information)
        self.message_box.setText(message)
        self.message_box.setWindowTitle(title)

        self.message_box.exec()
