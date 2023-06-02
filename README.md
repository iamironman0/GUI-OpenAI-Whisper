# OpenAI Whisper GUI with PyQt5

This is a simple GUI application that utilizes OpenAI's Whisper to transcribe audio files. The app is built using PyQt5 framework.

## Preview
![1](https://github.com/iamironman0/openai-whisper-gui-pyqt5/assets/63475761/0fa3de8d-fc8a-4bd7-9a04-93d3e74b46f6)


## Features
* Models: Tiny, Base, Small, Medium, Large
* Languages: Arabic, English
* Task: Transcribe, Translate
* Save transcription results to a text file
* Clear output text
* Utilizes multiprocessing (QThread)

## Setup

### Requirements
* Python version 3.9
* Torch with Cuda
* Nvidia GPU
* ffmpeg
* PyQt5 

> For more information please visit OpenAI Wishper github: https://github.com/openai/whisper

1. Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```
On macOS and Linux, use pip3 instead:
```
pip3 install -r requirements.txt
```

2. Run the application by executing the following command:

```
python main.py 
```
On macOS and Linux, use python3 instead:

```
python3 main.py
