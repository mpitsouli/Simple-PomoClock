import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QHBoxLayout, QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QMessageBox
)


class PomodoroSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Pomodoro Settings')
        self.setFixedSize(400, 150)

        self.pomodoro_spinbox = QSpinBox(self)
        self.pomodoro_spinbox.setMinimum(1)
        self.pomodoro_spinbox.setMaximum(120)
        self.pomodoro_spinbox.setSuffix(' minutes')

        self.short_break_spinbox = QSpinBox(self)
        self.short_break_spinbox.setMinimum(1)
        self.short_break_spinbox.setMaximum(60)
        self.short_break_spinbox.setSuffix(' minutes')

        self.long_break_spinbox = QSpinBox(self)
        self.long_break_spinbox.setMinimum(1)
        self.long_break_spinbox.setMaximum(60)
        self.long_break_spinbox.setSuffix(' minutes')

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)

        button_box = QDialogButtonBox(Qt.Horizontal)
        button_box.addButton(self.ok_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(self.cancel_button, QDialogButtonBox.RejectRole)

        layout = QFormLayout(self)
        layout.addRow('Pomodoro Duration:', self.pomodoro_spinbox)
        layout.addRow('Short Break Duration:', self.short_break_spinbox)
        layout.addRow('Long Break Duration:', self.long_break_spinbox)
        layout.addRow(button_box)

        self.old_pomodoro_duration = 0
        self.old_short_break_duration = 0
        self.old_long_break_duration = 0

    def update_durations(self, pomodoro_duration, short_break_duration, long_break_duration):
        self.pomodoro_spinbox.setValue(pomodoro_duration)
        self.short_break_spinbox.setValue(short_break_duration)
        self.long_break_spinbox.setValue(long_break_duration)
        self.old_pomodoro_duration = pomodoro_duration
        self.old_short_break_duration = short_break_duration
        self.old_long_break_duration = long_break_duration

    def get_durations(self):
        return (
            self.pomodoro_spinbox.value(),
            self.short_break_spinbox.value(),
            self.long_break_spinbox.value()
        )

    def reject(self):
        self.pomodoro_spinbox.setValue(self.old_pomodoro_duration)
        self.short_break_spinbox.setValue(self.old_short_break_duration)
        self.long_break_spinbox.setValue(self.old_long_break_duration)
        super().reject()


class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.time_remaining = 25 * 60  # Initial time is set to 25 minutes
        self.is_running = False

        # Set the window icon
        self.app_icon = QIcon('C:\\Python\\pythonProject2\\time.ico')
        self.setWindowIcon(self.app_icon)
        self.continue_plotting = True

        self.setWindowTitle('Simple PomoClock')
        self.setFixedSize(500, 300)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout(self.main_widget)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Add stretchable space before the buttons

        self.pomodoro_button = QPushButton('Pomodoro', self)
        self.pomodoro_button.clicked.connect(self.start_pomodoro)
        self.pomodoro_button.setStyleSheet(
            "QPushButton {color: #FFFFFF; font-size: 15px; height: 25px; "
            "margin: 10px; border-radius: 50px; border: none; } "
            "QPushButton:hover {color: #c2e6ff; }")
        button_layout.addWidget(self.pomodoro_button)

        self.short_break_button = QPushButton('Short Break', self)
        self.short_break_button.clicked.connect(self.short_break)
        self.short_break_button.setStyleSheet(
            "QPushButton {color: #FFFFFF; font-size: 15px; height: 25px; "
            "margin: 10px; border-radius: 50px; border: none; } "
            "QPushButton:hover {color: #c2e6ff; }")
        button_layout.addWidget(self.short_break_button)

        self.long_break_button = QPushButton('Long Break', self)
        self.long_break_button.clicked.connect(self.long_break)
        self.long_break_button.setStyleSheet(
            "QPushButton {color: #FFFFFF; font-size: 15px; height: 25px; "
            "margin: 10px; border-radius: 50px; border: none; } "
            "QPushButton:hover {color: #c2e6ff; }")
        button_layout.addWidget(self.long_break_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setStyleSheet(
            "QPushButton {color: #FFFFFF; font-size: 15px; height: 25px; "
            "margin: 10px; border-radius: 50px; border: none; } "
            "QPushButton:hover {color: #c2e6ff; }")
        button_layout.addWidget(self.reset_button)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setStyleSheet(
            "QPushButton {color: #FFFFFF; font-size: 15px; height: 25px; "
            "margin: 10px; border-radius: 50px; border: none; } "
            "QPushButton:hover {color: #c2e6ff; }")
        button_layout.addWidget(self.settings_button)

        button_layout.addStretch(1)  # Add stretchable space after the buttons

        layout.addLayout(button_layout)  # Add button layout to the main layout

        self.timer_label = QLabel(self.format_time(self.time_remaining))
        self.timer_label.setStyleSheet(
            "QLabel { color: #FFFFFF; font-size: 80px; qproperty-alignment: AlignCenter; }"
        )
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()  # Horizontal layout for start and reset buttons
        button_layout.addStretch(1)  # Add stretchable space before the start button

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_pause_timer)
        self.start_button.setStyleSheet("QPushButton {background-color: #7795b4; color: #FFFFFF; font-size: 15px; "
                                        "border-radius: 20px; border: none; padding: 10px 20px; }"
                                        "QPushButton:hover { background-color: #46637f; }"
                                        "QPushButton:pressed { background-color: #3d566e; }")
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        button_layout.addStretch(1)  # Add stretchable space after the buttons

        layout.addLayout(button_layout)

        self.pomodoro_duration = 25
        self.short_break_duration = 5
        self.long_break_duration = 15

        self.update_style()

    def start_pause_timer(self):
        if not self.is_running:
            self.start_timer()
            self.start_button.setText('Pause')
            self.is_running = True
        else:
            self.pause_timer()
            self.start_button.setText('Start')
            self.is_running = False

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # Timer updates every second

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def reset_timer(self):
        self.pause_timer()
        self.time_remaining = self.pomodoro_duration * 60
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.start_button.setText('Start')
        self.is_running = False

    def short_break(self):
        self.pause_timer()
        self.time_remaining = self.short_break_duration * 60
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.start_button.setText('Start')
        self.is_running = False

    def long_break(self):
        self.pause_timer()
        self.time_remaining = self.long_break_duration * 60
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.start_button.setText('Start')
        self.is_running = False

    def start_pomodoro(self):
        self.pause_timer()
        self.time_remaining = self.pomodoro_duration * 60
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.start_button.setText('Start')
        self.is_running = False

    def open_settings(self):
        settings_dialog = PomodoroSettings(self)
        settings_dialog.update_durations(self.pomodoro_duration, self.short_break_duration, self.long_break_duration)

        if settings_dialog.exec_() == QDialog.Accepted:
            self.pomodoro_duration, self.short_break_duration, self.long_break_duration = \
                settings_dialog.get_durations()
            self.reset_timer()

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(self.format_time(self.time_remaining))

        if self.time_remaining == 0:
            self.timer.stop()
            # Perform action when timer finishes (e.g., display a message, play a sound)

    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02d}:{seconds:02}'

    def update_style(self):
        style_sheet = """
            QMainWindow {
                background-color: #4f6f8f;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """
        self.setStyleSheet(style_sheet)

    def closeEvent(self, event):
        confirmation = QMessageBox.question(
            self, "Confirmation", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No
        )
        if confirmation == QMessageBox.No:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    pomodoro_timer = PomodoroTimer()
    pomodoro_timer.show()

    sys.exit(app.exec_())
