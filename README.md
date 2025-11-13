# VideoDecoder

Скрипт для распознавания речи из видео с Vosk.

## Установка
- git clone https://github.com/namestnikoff/VideoDecoder.git
- pip install -r requirements.txt
- Скачайте модель: https://alphacephei.com/vosk/models (vosk-model-ru-0.42 в C:\Scripts\model\)

## Запуск
python main/decoding.py

Обрабатывает .wav/.webm/.mp4 из input_folder, сохраняет .txt в output_folder.