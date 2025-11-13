from vosk import Model, KaldiRecognizer
import wave
import json
import os
from pydub import AudioSegment

# Пути к папкам и модели
input_folder = r"C:\Users\User\Documents\Телемост\video_files_for_text_extraction"
output_folder = r"C:\Users\User\Documents\Телемост\text_from_video_files"
#model_path = r"C:\Scripts\python\VideoDecoder\model\vosk-model-small-ru-0.22"
model_path = r"C:\Scripts\model\vosk-model-ru-0.42"
temp_wav_folder = os.path.join(input_folder, "temp_wav")

# Создание папок
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(temp_wav_folder):
    os.makedirs(temp_wav_folder)

# Проверка модели
if not os.path.exists(model_path):
    print(f"Модель не найдена в {model_path}. Скачайте с https://alphacephei.com/vosk/models")
    exit(1)

model = Model(model_path)

# Конвертация WebM или MP4 в WAV
def convert_to_wav(input_file, output_file, file_format):
    try:
        audio = AudioSegment.from_file(input_file, format=file_format)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(output_file, format="wav")
        print(f"Сконвертирован: {output_file}")
        return True
    except Exception as e:
        print(f"Ошибка конвертации {input_file}: {e}")
        return False

# Проверка формата WAV
def check_wav_format(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            return (wf.getnchannels() == 1 and
                    wf.getsampwidth() == 2 and
                    wf.getframerate() == 16000)
    except Exception as e:
        print(f"Ошибка проверки {file_path}: {e}")
        return False

# Обработка аудио
def process_audio(audio_file, output_text_file, recognizer):
    try:
        with wave.open(audio_file, 'rb') as wf:
            if not check_wav_format(audio_file):
                print(f"Файл {audio_file} должен быть WAV, моно, 16-bit, 16000 Hz")
                return False
            with open(output_text_file, 'w', encoding='utf-8') as txt_file:
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())['text']
                        if result:
                            txt_file.write(result + "\n")
                final_result = json.loads(recognizer.FinalResult())['text']
                if final_result:
                    txt_file.write(final_result + "\n")
            print(f"Результат сохранен: {output_text_file}")
            return True
    except Exception as e:
        print(f"Ошибка обработки {audio_file}: {e}")
        return False

# Обработка файлов
for filename in os.listdir(input_folder):
    if filename.endswith((".wav", ".webm", ".mp4")):
        input_file = os.path.join(input_folder, filename)
        output_text_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        temp_wav_file = os.path.join(temp_wav_folder, f"{os.path.splitext(filename)[0]}_temp.wav")
        print(f"Обработка: {filename}")
        recognizer = KaldiRecognizer(model, 16000)
        if filename.endswith((".webm", ".mp4")):
            file_format = "webm" if filename.endswith(".webm") else "mp4"
            if convert_to_wav(input_file, temp_wav_file, file_format):
                process_audio(temp_wav_file, output_text_file, recognizer)
                try:
                    os.remove(temp_wav_file)
                    print(f"Удален: {temp_wav_file}")
                except Exception as e:
                    print(f"Ошибка удаления {temp_wav_file}: {e}")
            else:
                print(f"Конвертация {filename} не удалась")
        else:
            process_audio(input_file, output_text_file, recognizer)

print("Обработка завершена.")
