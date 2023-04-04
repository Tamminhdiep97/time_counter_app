import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import QTimer, QTime, Qt
from loguru import logger


class WorkTimeCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clock")

        # Initialize variables
        self.working_time = QTime(0, 0, 0)
        self.paused = False
        self.stop = False

        # Create UI components
        self.setStyleSheet("""
            background-color: #1c1c1c;
            color: #ffffff;
            font-family: Arial;
        """)

        self.label = QLabel("00:00:00", self)
        self.label.setGeometry(40, 20, 500, 80)
        self.label.setStyleSheet("""
            font-size: 54px;
            padding: 10px;
            border: 3px solid #ffffff;
            border-radius: 20px;
            text-align: center;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start/Resume", self)
        self.start_button.setGeometry(40, 120, 150, 40)
        self.start_button.setStyleSheet("""
            background-color: #4caf50;
            color: #ffffff;
            border-radius: 5px;
            font-size: 16px;
        """)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setGeometry(210, 120, 150, 40)
        self.pause_button.setStyleSheet("""
            background-color: #2196f3;
            color: #ffffff;
            border-radius: 5px;
            font-size: 16px;
        """)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(380, 120, 150, 40)
        self.stop_button.setStyleSheet("""
            background-color: #f44336;
            color: #ffffff;
            border-radius: 5px;
            font-size: 16px;
        """)

        self.hour_label = QLabel("", self)
        self.hour_label.setGeometry(40, 180, 300, 60)
        self.hour_label.setStyleSheet("""
            font-size: 18px;
            padding: 5px;
        """)

        # Connect signals to slots
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)

        # Connect signals to button style update slot
        self.start_button.clicked.connect(self.update_button_stylesheets)
        self.pause_button.clicked.connect(self.update_button_stylesheets)
        self.stop_button.clicked.connect(self.update_button_stylesheets)

    def resizeEvent(self, event):
        # Calculate new position and size for UI components based on the new window size
        width = event.size().width()
        height = event.size().height()

        label_width = min(width - 10, 500)
        label_height = min(height - 150, 180)
        self.label.setGeometry(int((width - label_width) / 2), 20, label_width, label_height)

        button_width = int((width - 120) / 3)
        self.start_button.setGeometry(40, height - 100, button_width, 40)
        self.pause_button.setGeometry(40 + button_width + 20, height - 100, button_width, 40)
        self.stop_button.setGeometry(40 + 2 * button_width + 40, height - 100, button_width, 40)

        self.hour_label.setGeometry(40, height - 50, width - 80, 30)

    def update_button_stylesheets(self):
        sender = self.sender() # Get the button that emitted the signal
        buttons = [self.start_button, self.pause_button, self.stop_button]
        for button in buttons:
            if button == sender: # Update style for clicked button
                button.setStyleSheet("""
                    background-color: #F1E0C5;
                    color: #010101;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    border: 3px solid #dbe2ef;
                """)
            else: # Update style for other buttons
                button.setStyleSheet("""
                    background-color: {};
                    color: #ffffff;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: normal;
                """.format("#4caf50" if button == self.start_button else "#2196f3" if button == self.pause_button else "#f44336"))


    def start_timer(self):
        if self.paused:
            self.paused = False
            self.stop = False
        if self.stop:
            self.label.setText("00:00:00")
            self.stop = False
            self.working_time = QTime(0, 0, 0)
        self.timer.start(1000)  # Update every 1 second

    def pause_timer(self):
        self.paused = True

    def stop_timer(self):
        self.stop = True
        self.timer.stop()
        total_time = self.working_time.toString("hh:mm:ss")
        total_hour = round(self.working_time.msecsSinceStartOfDay() / (3600 * 1000), 2)
        self.hour_label.setText(f"Total working time: {total_hour:.2f} hours")
        logger.info("Total working time: {}".format(total_time))

    def update_label(self):
        if not self.paused:
            self.working_time = self.working_time.addSecs(1)
            elapsed_secs = self.working_time.msecsSinceStartOfDay() / 1000
            elapsed_hours = round(elapsed_secs / (3600), 2)
            self.label.setText(self.working_time.toString("hh:mm:ss"))
            self.hour_label.setText(f"Total working time: {elapsed_hours:.2f} hours")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('background-color: white;')
    calculator = WorkTimeCalculator()
    calculator.show()
    sys.exit(app.exec())
