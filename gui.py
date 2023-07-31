from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QCheckBox, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from functools import partial
import pyperclip
import webbrowser

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('The Hub Helper')
        self.setWindowIcon(QIcon('https://www.clayton.edu/themes/custom/clayton_state/logo.png'))

        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #e5e5e5;")  # Light grey
        central_widget.setFont(font)

        vbox = QVBoxLayout(central_widget)

        id_lookup_button = QPushButton('Visit ID lookup', self)
        id_lookup_button.clicked.connect(self.open_id_lookup)
        id_lookup_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        vbox.addWidget(id_lookup_button)

        jk_team_button = QPushButton('J&K Team', self)
        jk_team_button.clicked.connect(self.open_jk_team)
        jk_team_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        vbox.addWidget(jk_team_button)

        self.labels = ["First name:", "Last name:", "Username:", "Laker ID:", "DOB:", "Last 4 SSN:", "Old Number:", "New Number:"]
        self.entries = {label: QLineEdit() for label in self.labels}
        self.buttons = {label: QPushButton('Copy', self) for label in self.labels}
        self.clear_buttons = {label: QPushButton('Clear', self) for label in self.labels}

        for label, entry in self.entries.items():
            vbox.addWidget(QLabel(label))
            hbox = QHBoxLayout()
            hbox.addWidget(entry)
            entry.setStyleSheet("""
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: white;
            """)
            button = self.buttons[label]
            button.clicked.connect(partial(self.copy_one, label))
            button.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                    background: #e0e0e0;
                }
                QPushButton:hover {
                    background: #d0d0d0;
                }
                QPushButton:pressed {
                    background: #c0c0c0;
                }
            """)
            hbox.addWidget(button)
            clear_button = self.clear_buttons[label]
            clear_button.clicked.connect(partial(self.clear_one, label))
            clear_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                    background: #e0e0e0;
                }
                QPushButton:hover {
                    background: #d0d0d0;
                }
                QPushButton:pressed {
                    background: #c0c0c0;
                }
            """)
            hbox.addWidget(clear_button)
            vbox.addLayout(hbox)

        grid_bottom = QGridLayout()
        vbox.addLayout(grid_bottom)

        self.verified_checkbox = QCheckBox('Verified', self)
        grid_bottom.addWidget(self.verified_checkbox, 0, 0)

        copy_all_button = QPushButton('MFA', self)
        copy_all_button.clicked.connect(self.copy_all)
        copy_all_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(copy_all_button, 0, 1)

        reset_button = QPushButton('Password Reset', self)
        reset_button.clicked.connect(self.copy_reset)
        reset_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(reset_button, 0, 2)

        clear_all_button = QPushButton('Clear All', self)
        clear_all_button.clicked.connect(self.clear_all)
        clear_all_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(clear_all_button, 0, 3)

        find_by_id_button = QPushButton('Find by ID (Service Now)', self)
        find_by_id_button.clicked.connect(self.find_by_id)
        find_by_id_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(find_by_id_button, 1, 0)

        find_by_phone_button = QPushButton('Find by Phone (Service Now)', self)
        find_by_phone_button.clicked.connect(self.find_by_phone)
        find_by_phone_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(find_by_phone_button, 1, 1)

        paste_button = QPushButton('Paste', self)
        paste_button.clicked.connect(self.paste_from_clipboard)
        paste_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 5px;
                background: #e0e0e0;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: #c0c0c0;
            }
        """)
        grid_bottom.addWidget(paste_button, 1, 2)

        self.resize(600, 600)  # Default size to be larger
        self.show()

    def copy_one(self, label):
        pyperclip.copy(self.entries[label].text())

    def copy_all(self):
        result = "MFA Change\n"
        for label, entry in self.entries.items():
            result += f"{label} {entry.text()}\n"
        if self.verified_checkbox.isChecked():
            result += "Verified\n"
        pyperclip.copy(result)

    def copy_reset(self):
        result = "Password Reset\n"
        for label, entry in self.entries.items():
            if label not in ["Old Number:", "New Number:"]:
                result += f"{label} {entry.text()}\n"
        if self.verified_checkbox.isChecked():
            result += "Verified\n"
        pyperclip.copy(result)

    def paste_from_clipboard(self):
        text = pyperclip.paste()
        lines = text.split("\n")
        for line in lines:
            if not line:
                continue
            input_label, _, value = line.partition(':')
            input_label = input_label.strip().lower()  # Convert to lowercase for case-insensitive match
            value = value.strip()
            # Check for label match ignoring case and extra words at the end
            for gui_label in self.entries:
                if gui_label.lower().startswith(input_label):
                    self.entries[gui_label].setText(str(value))  # Always treat value as string
                    break  # Exit the loop once a match is found

    def clear_one(self, label):
        self.entries[label].clear()

    def clear_all(self):
        for label, entry in self.entries.items():
            entry.clear()

    def find_by_id(self):
        url = "https://service.clayton.edu/nav_to.do?uri=%2F$sn_global_search_results.do%3Fsysparm_search%3D"
        laker_id = self.entries["Laker ID:"].text()
        webbrowser.open(url + laker_id)

    def find_by_phone(self):
        url = "https://service.clayton.edu/nav_to.do?uri=%2F$sn_global_search_results.do%3Fsysparm_search%3D"
        phone = self.entries["New Number:"].text()
        webbrowser.open(url + phone)

    def open_id_lookup(self):
        webbrowser.open('https://apps.clayton.edu/lakerid-lookup')

    def open_jk_team(self):
        webbrowser.open('https://teams.microsoft.com/_#/conversations/19:a9742c1d736844f889d9a504c1436815@thread.v2?ctx=chat')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
