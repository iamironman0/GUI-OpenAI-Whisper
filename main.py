from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QPushButton, 
    QComboBox, 
    QFileDialog, 
    QLabel, 
    QTextEdit
)
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread
import whisper
import torch

ui = "./ui.ui"
logo_file = "./logo.ico"
app_name = "Transcriber"

class Worker(QThread):
    resultReady = pyqtSignal(str)
    errorOccurred = pyqtSignal(str)

    def __init__(self, audioFile, getModel, getLanguage, getTask):
        super(Worker, self).__init__()
        self.audioFile = audioFile
        self.getModel = getModel
        self.getLanguage = getLanguage
        self.getTask = getTask
        self.model = None

    def loadModel(self):
        if self.model is None:
            self.model = whisper.load_model(self.getModel)

    def run(self):
        try:
            self.loadModel()
            text = self.model.transcribe(self.audioFile, language=self.getLanguage, task=self.getTask, fp16=torch.cuda.is_available())
            format_text = text["text"].strip().capitalize()
            self.resultReady.emit(format_text)

        except Exception as e:
            error_message = "Error: Unable to load audio data. Please check that the file exists and is in a compatible format"
            self.errorOccurred.emit(error_message)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi(ui, self)

        self.setWindowTitle(app_name)
        self.setWindowIcon(QIcon(logo_file))

        self.model = self.findChild(QComboBox, "modelOption")
        self.language = self.findChild(QComboBox, "languageOption")
        self.task = self.findChild(QComboBox, "taskOption")
        
        self.openFileButton = self.findChild(QPushButton, "selectfileButton")
        self.startButton = self.findChild(QPushButton, "startButton")
        self.saveButton = self.findChild(QPushButton, "saveButton")
        self.clearButton = self.findChild(QPushButton, "clearButton")

        self.outputText = self.findChild(QTextEdit, "outputBox")
        self.messageLabel = self.findChild(QLabel, "statusLabel")

        self.openFileButton.clicked.connect(self.get_audio_path)
        self.saveButton.clicked.connect(self.save_text)
        self.startButton.clicked.connect(self.start_task)
        self.clearButton.clicked.connect(self.clear_text)

        self.startButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        self.outputText.setReadOnly(True)
        self.outputText.setEnabled(True)

        self.messageLabel.setText("Status: Ready")

        self.audioFile = None

    def get_audio_path(self):
        options = QFileDialog.Options()
        audioFile, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav)", options=options)

        if audioFile:
            self.audioFile = audioFile
            self.messageLabel.setText(f"Info: Selected File: {audioFile}")
            self.startButton.setEnabled(True)
        else:
            self.messageLabel.setText("Info: No Audio File Selected")
            self.startButton.setEnabled(False)

    def save_text(self):
        text = self.outputText.toPlainText()
        fileDialog = QFileDialog()
        fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        fileDialog.setNameFilters(['Text Files (*.txt)', 'All Files (*.*)'])
        fileDialog.setDefaultSuffix('txt')

        if fileDialog.exec_() == QFileDialog.Accepted:
            filePath = fileDialog.selectedFiles()[0]
            try:
                with open(filePath, "w", encoding="utf-8") as file:
                    file.write(text)
                self.messageLabel.setText(f"Info: File Saved As: {filePath}")
            except IOError:
                self.messageLabel.setText("Error: Failed to save the file.")
        else:
            self.messageLabel.setText("Info: File saving canceled.")

    def start_task(self):
        if self.audioFile:
            self.openFileButton.setEnabled(False)
            self.startButton.setEnabled(False)
            self.saveButton.setEnabled(False)

            self.messageLabel.setText("Status: Transcribing Started")

            self.worker = Worker(self.audioFile, self.model.currentText().lower(), self.language.currentText().lower(), self.task.currentText().lower())
            self.worker.resultReady.connect(self.update_text)
            self.worker.errorOccurred.connect(self.handle_error_message)
            self.worker.start()
        else:
            self.messageLabel.setText("Info: No Audio File Selected To Start The Task.")

    def update_text(self, text):
        self.outputText.setText(text)

        self.openFileButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.saveButton.setEnabled(True)

        self.messageLabel.setText("Status: Transcribing Completed")

    def handle_error_message(self, error_message):
        self.messageLabel.setText(error_message)

        self.openFileButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def clear_text(self):
        self.outputText.clear()

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
