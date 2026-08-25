import sys
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QFont

class AIDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Hands-Free Control Center")
        self.setGeometry(300, 200, 500, 400)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        self.process = None
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)

        # Title Header
        title = QLabel("AI COMPUTER CONTROL SYSTEM")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00E676; margin-top: 10px;")
        layout.addWidget(title)

        # Status Display Frame
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; padding: 15px;")
        status_layout = QVBoxLayout(status_frame)

        self.status_label = QLabel("System Status: INACTIVE")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #FF5252;")
        status_layout.addWidget(self.status_label)

        layout.addWidget(status_frame)

        # Control Buttons
        btn_layout = QHBoxLayout()

        self.btn_start = QPushButton("START ENGINE")
        self.btn_start.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #00C853; color: white; padding: 12px; 
                border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #00E676; }
        """)
        self.btn_start.clicked.connect(self.start_engine)

        self.btn_stop = QPushButton("STOP ENGINE")
        self.btn_stop.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #D50000; color: white; padding: 12px; 
                border-radius: 8px; border: none;
            }
            QPushButton:hover { background-color: #FF1744; }
        """)
        self.btn_stop.clicked.connect(self.stop_engine)
        self.btn_stop.setEnabled(False)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        # Footer
        footer = QLabel("Powered by MediaPipe & SpeechRecognition")
        footer.setFont(QFont("Segoe UI", 8))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #757575;")
        layout.addWidget(footer)

    def start_engine(self):
        if self.process is None:
            self.process = QProcess()
            # Current Virtual Environment ka exact python path pick karein
            python_path = sys.executable  
            self.process.start(python_path, ["main.py"])
            
            self.status_label.setText("System Status: ACTIVE (Running)")
            self.status_label.setStyleSheet("color: #00E676;")
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)

    def stop_engine(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.status_label.setText("System Status: INACTIVE")
            self.status_label.setStyleSheet("color: #FF5252;")
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIDashboard()
    window.show()
    sys.exit(app.exec())