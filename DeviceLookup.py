# Corrected code to add lookup functionality to the Hub Helper in a new tab

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QCheckBox, QAction, QMenu, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser
import pyperclip
import re

# Base URL for Service Now queries
base_url = "https://service.clayton.edu/nav_to.do?uri=%2Fcmdb_ci_computer_list.do%3Fsysparm_clear_stack%3Dtrue%26sysparm_userpref_module%3D9eb351b24a362314003336f86d01f9fb%26sysparm_list_mode%3Dgrid%26sysparm_query%3D"

class LookupWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.labels = [
            "Hub ID",
            "Serial Number",
            "Assigned to",
            "CS Location"
        ]

        self.entries = {label: QLineEdit() for label in self.labels}

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        for i, label in enumerate(self.labels):
            grid.addWidget(QLabel(label + ":"), i, 0)
            grid.addWidget(self.entries[label], i, 1)
            button = QPushButton("Lookup")
            button.clicked.connect(lambda _, x=label: self.lookup(x))
            grid.addWidget(button, i, 2)

        # Add button for multi-query lookup
        multi_query_button = QPushButton("Multi-Query Lookup")
        multi_query_button.clicked.connect(self.multi_query_lookup)
        grid.addWidget(multi_query_button, len(self.labels), 0, 1, 3)

    def lookup(self, label):
        if label == "Hub ID":
            prefix = "u_hub_idSTARTSWITH"
        elif label == "Serial Number":
            prefix = "nameSTARTSWITH"
        elif label == "Assigned to":
            prefix = "assigned_to.nameSTARTSWITH"
        elif label == "CS Location":
            prefix = "u_cs_location.nameSTARTSWITH"
        
        value = self.entries[label].text()
        webbrowser.open(base_url + prefix + value)

    def multi_query_lookup(self):
        query_parts = []
        for label in self.labels:
            value = self.entries[label].text()
            if value:
                if label == "Hub ID":
                    prefix = "u_hub_idSTARTSWITH"
                elif label == "Serial Number":
                    prefix = "nameSTARTSWITH"
                elif label == "Assigned to":
                    prefix = "assigned_to.nameSTARTSWITH"
                elif label == "CS Location":
                    prefix = "u_cs_location.nameSTARTSWITH"
                query_parts.append(prefix + value)
        
        multi_query = "%255E".join(query_parts)
        webbrowser.open(base_url + multi_query)

class HubHelperWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.labels = [
            "First Name",
            "Last Name",
            "Username",
            "Laker ID",
            "DoB",
            "SSN",
            "Old",
            "New"
        ]

        self.entries = {label: QLineEdit() for label in self.labels}

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        for i, label in enumerate(self.labels):
            grid.addWidget(QLabel(label + ":"), i, 0)
            grid.addWidget(self.entries[label], i, 1)

        self.verified = QCheckBox("Verified")
        grid.addWidget(self.verified, 8, 0, 1, 2)

        copy_all_button = QPushButton("Copy All", clicked=self.copy_all)
        grid.addWidget(copy_all_button, 9, 0, 1, 2)

        paste_all_button = QPushButton("Paste All", clicked=self.paste_all)
        grid.addWidget(paste_all_button, 10, 0, 1, 2)

        for i, label in enumerate(self.labels):
            copy_button = QPushButton("Copy", clicked=lambda x=label: self.copy_one(x))
            grid.addWidget(copy_button, i, 2)

        reset_button = QPushButton("Reset", clicked=self.reset)
        grid.addWidget(reset_button, 11, 0, 1, 2)

        # Add lookup button to find by ID
        find_by_id_button = QPushButton("Find by ID", clicked=self.find_by_id)
        grid.addWidget(find_by_id_button, 12, 0, 1, 2)

        # Add lookup button to find by Phone
        find_by_phone_button = QPushButton("Find by Phone", clicked=self.find_by_phone)
        grid.addWidget(find_by_phone_button, 13, 0, 1, 2)

    def copy_one(self, label):
        pyperclip.copy(self.entries[label].text())

    def copy_all(self):
        lines = [f"{label}: {self.entries[label].text()}" for label in self.labels]
        if self.verified.isChecked():
            lines.append("Verified")
        pyperclip.copy("\n".join(lines))

    def paste_all(self):
        text = pyperclip.paste()
        lines = text.split("\n")

        for line in lines:
            match = re.match(r"(.*?): (.*)", line)
            if match and match.group(1) in self.entries:
                self.entries[match.group(1)].setText(match.group(2))

    def reset(self):
        for entry in self.entries.values():
            entry.clear()
        self.verified.setChecked(False)

    def find_by_id(self):
        webbrowser.open("https://service.clayton.edu/nav_to.do?uri=%2F$sn_global_search_results.do%3Fsysparm_search%3D" + self.entries["Laker ID"].text())

    def find_by_phone(self):
        webbrowser.open("https://service.clayton.edu/nav_to.do?uri=%2F$sn_global_search_results.do%3Fsysparm_search%3D" + self.entries["New"].text())

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hub Helper')

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        hub_helper_widget = HubHelperWidget()
        tab_widget.addTab(hub_helper_widget, "Hub Helper")

        lookup_widget = LookupWidget()
        tab_widget.addTab(lookup_widget, "Lookup")

        self.show()

app = QApplication([])
ex = MyApp()
sys.exit(app.exec_())

