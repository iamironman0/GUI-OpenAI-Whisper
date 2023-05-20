# OpenAi Whisper GUI PyQt5
Simple GUI app that transcribe audio files with OpenAI Wishper and PyQt5

## Preview
![1](https://github.com/iamironman0/openai-whisper-gui-pyqt5/assets/63475761/0fa3de8d-fc8a-4bd7-9a04-93d3e74b46f6)


## Features
* Models: Tiny, Base, Small, Medium, Large
* Languages: Arabic, English
* Task: Transcribe, Translate
* Save result to a txt file
* Clear output text

* Using multiprocessing (QThread)

## Setup

### Requirements
* Python version 3.9
* Torch with Cuda
* Nvidia GPU
* ffmpeg
* PyQt5 

> For more information please visit OpenAI Wishper github: https://github.com/openai/whisper

1. Run this command
```
pip install -r requirements.txt
```
on mac and linux
```
pip3 install -r requirements.txt
```

2. Run the file

```
python main.py 
```
on mac and linux
```
python3 main.py
