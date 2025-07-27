# Redhouse Tutor - Launch Window
# This file handles the startup screen where users pick a topic and difficulty

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QComboBox
)
from gui import TutorWindow  # make sure gui.py has TutorWindow class exposed

# This is the first window that shows up
# It asks the user to type a topic and pick a difficulty before starting
class IntroWindow(QWidget):
    # Sets up the window title and size, then builds the UI
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eric and Redhouse Tutor – Choose Topic")
        self.setGeometry(200, 200, 400, 200)
        self.init_ui()

    def init_ui(self):
        # Layout container for all widgets
        layout = QVBoxLayout()

        # Welcome message
        self.label = QLabel("Welcome to Eric and Redhouse AI Tutor!\n\nWhat topic would you like to be quizzed on?")
        layout.addWidget(self.label)

        # Text box where user types in a topic
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g., Biology, U.S. History, Python")
        layout.addWidget(self.topic_input)

        # Label above the difficulty dropdown
        self.difficulty_label = QLabel("Select difficulty level:")
        layout.addWidget(self.difficulty_label)

        # Dropdown menu to pick difficulty level
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Moderate", "Hard"])
        layout.addWidget(self.difficulty_combo)

        # Start button that launches the quiz
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.launch_quiz)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    # When Start button is clicked, launch the main quiz window if topic is valid
    def launch_quiz(self):
        # Get topic from user input
        topic = self.topic_input.text().strip()
        # If topic is entered, get selected difficulty and open quiz window
        if topic:
            difficulty = self.difficulty_combo.currentText().lower()
            self.quiz_window = TutorWindow(topic=topic, difficulty=difficulty)
            self.quiz_window.show()
            self.close()
        # Otherwise, show warning to enter a topic
        else:
            QMessageBox.warning(self, "Input Required", "Please enter a topic to begin.")
