import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from tutor_ai import QuizSession

class TutorWindow(QWidget):
    def __init__(self, topic=None, difficulty="easy"):
        super().__init__()
        self.topic = topic
        self.difficulty = difficulty
        self.session = QuizSession(topic=topic, difficulty=difficulty)
        self.setWindowTitle("Eric and Redhouse AI Tutor - Let’s Learn Together!")
        self.setMinimumSize(900, 800)


        self.question_counter_label = QLabel("")
        self.question_counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_counter_label.setStyleSheet("font-size: 16px; color: #444444;")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.question_counter_label)

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Arial', sans-serif;
            }
            QLabel#Header {
                font-size: 28px;
                font-weight: bold;
                color: #1a1a1a;
                padding: 20px;
            }
            QLabel#Question {
                font-size: 18px;
                color: black;
                padding: 10px 20px;
                line-height: 1.6;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                background-color: #007acc;
                color: white;
                border-radius: 6px;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #888888;
            }
            QPushButton:hover {
                background-color: #1e90ff;
            }
            QLineEdit {
                font-size: 15px;
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                background-color: #f9f9f9;
                color: #222;
            }
        """)

        # title area up top
        self.title_label = QLabel("Let’s Learn Together!")
        self.title_label.setObjectName("Header")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # this part holds question and feedback side-by-side
        main_body_layout = QHBoxLayout()
        main_container = QWidget()
        main_container_layout = QHBoxLayout(main_container)
        main_container_layout.setSpacing(20)
        main_container.setContentsMargins(20, 0, 20, 0)

        # left panel = question and choices
        left_layout = QVBoxLayout()

        # show the actual question here
        self.question_label = QLabel("Question: Loading question...")
        self.question_label.setObjectName("Question")
        self.question_label.setStyleSheet("color: black; font-size: 18px;")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.question_label.setContentsMargins(10, 10, 10, 0)
        self.question_label.setTextFormat(Qt.TextFormat.RichText)
        # Removed fixed width to restore original layout symmetry
        # self.question_label.setFixedWidth(500)
        self.question_label.setMinimumHeight(100)
        left_layout.addWidget(self.question_label)

        # make the 4 choice buttons (A–D)
        self.answer_buttons = []
        choices = ["A.", "B.", "C.", "D."]
        for i in range(4):
            btn = QPushButton(f"{choices[i]} Option {i+1}")
            btn.clicked.connect(self.check_answer)
            btn.setMinimumHeight(60)
            # Removed fixed width to restore original layout symmetry
            # btn.setFixedWidth(500)
            btn.setStyleSheet("""
                text-align: left;
                padding-left: 10px;
                white-space: normal;
                word-wrap: break-word;
                font-size: 15px;
            """)
            btn.setToolTip(f"{choices[i]} Option {i+1}")
            self.answer_buttons.append(btn)
            left_layout.addWidget(btn)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        # Removed fixed width to restore original layout symmetry
        # left_widget.setFixedWidth(520)
        main_container_layout.addWidget(left_widget)

        # right panel = ai response + hint stuff
        right_layout = QVBoxLayout()

        self.ai_feedback_static_label = QLabel("AI Feedback (Answer Insights):")
        self.ai_feedback_static_label.setStyleSheet("font-weight: bold; font-size: 18px; color: black;")
        self.ai_feedback_static_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ai_feedback_static_label.setContentsMargins(10, 10, 10, 0)
        right_layout.addWidget(self.ai_feedback_static_label)

        self.answer_label = QLabel("")
        self.answer_label.setWordWrap(True)
        self.answer_label.setStyleSheet("color: black; font-weight: bold; background-color: #f2f2f2; border-radius: 8px; padding: 16px;")
        # placeholder text for now before user answers
        self.answer_label.setText("This space will show explanations and feedback after you answer.")
        self.answer_label.setContentsMargins(12, 12, 12, 12)
        self.answer_label.setFixedHeight(360)
        self.answer_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        right_layout.addWidget(self.answer_label)

        # hint button (only turns on after 1 wrong try)
        self.hint_button = QPushButton("Get Hint")
        self.hint_button.clicked.connect(self.get_hint)
        self.hint_button.setEnabled(False)
        # Removed fixed width to restore original layout symmetry
        # self.hint_button.setFixedWidth(520)
        self.hint_button.setFixedHeight(50)

        self.hint_reveal_layout = QVBoxLayout()
        self.hint_reveal_layout.addWidget(self.hint_button)
        # we don’t show the answer anymore so that part is gone
        right_layout.addLayout(self.hint_reveal_layout)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        # Removed fixed width to restore original layout symmetry
        # right_widget.setFixedWidth(520)
        main_container_layout.addWidget(right_widget)

        self.layout.addSpacing(10)
        self.layout.addWidget(main_container)
        self.layout.addSpacing(10)

        # thin line between main and bottom controls
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(divider)

        # bottom buttons (next + show progress)
        bottom_layout = QHBoxLayout()

        self.retry_button = QPushButton("Next Question")
        self.retry_button.clicked.connect(self.load_question)
        # Removed fixed width to restore original layout symmetry
        # self.retry_button.setFixedWidth(520)
        bottom_layout.addSpacing(40)
        bottom_layout.addWidget(self.retry_button)

        self.score_button = QPushButton("Show Progress")
        self.score_button.clicked.connect(self.show_score)
        # Removed fixed width to restore original layout symmetry
        # self.score_button.setFixedWidth(520)
        bottom_layout.addWidget(self.score_button)
        bottom_layout.addSpacing(40)

        self.layout.addLayout(bottom_layout)
        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        self.session.wrong_attempts = 0
        self.attempts_left = 3
        if self.session.is_finished():
            # Remove emoji from completion and final score message
            final_score = self.session.score_percentage()
            self.question_label.setText(
                f"You’ve completed all {self.session.max_questions} questions.<br><br>"
                f"<b>Final Score:</b> {final_score:.2f}%"
            )
            for btn in self.answer_buttons:
                btn.setDisabled(True)
            self.hint_button.setDisabled(True)
            self.retry_button.setDisabled(True)
            self.retry_button.setStyleSheet("background-color: #666; color: white;")
            final_message = f"<b>Final Score:</b> {final_score:.2f}%<br>" \
                            f"<b>Insights:</b> {self.session.get_score_message()}"
            self.answer_label.setText(final_message)
            return
        self.retry_button.setStyleSheet("")  # Reset to default blue
        self.question_counter_label.setText(
            f"Question {self.session.current_question_number} of {self.session.max_questions}"
        )
        data = self.session.next_question()
        # Remove emoji from topic label
        self.question_label.setText(
            f"<b>Topic:</b> {self.session.topic}<br><br><b>Question:</b> {data['question']}"
        )
        choices = ["A.", "B.", "C.", "D."]
        for i, choice in enumerate(data['choices']):
            self.answer_buttons[i].setText(f"{choices[i]} {choice}")
            self.answer_buttons[i].setToolTip(f"{choices[i]} {choice}")
            self.answer_buttons[i].setEnabled(True)
        # stop old timer if it was still going
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        # clear old feedback before new one starts
        self.answer_label.setText("This space will show explanations and feedback after you answer.")
        self.answer_label.repaint()
        self.hint_button.setEnabled(False)
        self.retry_button.setEnabled(False)

    def check_answer(self):
        clicked = self.sender()
        user_letter = clicked.text()[0]
        self.retry_button.setEnabled(False)
        correct, feedback = self.session.submit_answer(user_letter, self.session.correct_letter)
        if correct:
            for btn in self.answer_buttons:
                btn.setDisabled(True)
            self.retry_button.setStyleSheet("background-color: #28a745; color: white; border: 2px solid #1c7c30;")
            self.animate_typing(feedback, self.answer_label)
            self.hint_button.setEnabled(False)
            self.retry_button.setEnabled(True)
        else:
            self.attempts_left -= 1
            if self.attempts_left == 2:
                self.hint_button.setEnabled(True)
            self.animate_typing(feedback, self.answer_label)
            if self.attempts_left <= 0:
                for btn in self.answer_buttons:
                    btn.setDisabled(True)
                self.hint_button.setEnabled(False)
                self.retry_button.setStyleSheet("background-color: #28a745; color: white; border: 2px solid #1c7c30;")
                self.retry_button.setEnabled(True)

    def show_score(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setTextFormat(Qt.TextFormat.RichText)
        if self.session.total_questions == 0:
            msg.setWindowTitle("Progress")
            msg.setText("<span style='color: black;'>No questions answered yet.</span>")
            msg.exec()
            return
        percent = self.session.score_percentage()
        correct = self.session.correct_count
        total = self.session.total_questions
        msg.setWindowTitle("Your Learning Progress")
        msg.setText(
            f"<span style='color: black;'>"
            f"✅ Correct: {correct}<br>"
            f"📊 Total: {total}<br>"
            f"📈 Score: {percent:.2f}%"
            f"</span>"
        )
        msg.exec()


    # used to show answer, not anymore

    def get_hint(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setTextFormat(Qt.TextFormat.RichText)
        hint = self.session.get_hint()
        msg.setWindowTitle("Hint")
        msg.setText(f"<span style='color: black;'>Hint: {hint}</span>")
        msg.exec()

    def animate_typing(self, full_text, target_label):
        self.current_index = 0
        self.full_text = full_text
        self.target_label = target_label

        # make spacing look better in feedback
        self.target_label.setContentsMargins(0, 8, 0, 8)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_typing)
        self.timer.start(25)

    def update_typing(self):
        if self.current_index < len(self.full_text):
            current_text = self.full_text[:self.current_index + 1]
            self.target_label.setText(current_text)
            self.current_index += 1
        else:
            self.timer.stop()

def run_app(topic=None):
    app = QApplication(sys.argv)
    window = TutorWindow(topic=topic)
    window.show()
    sys.exit(app.exec())