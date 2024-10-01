import os
import wave
import json
import srt
import subprocess
import sys
from vosk import Model as VoskModel, KaldiRecognizer

# تعریف مسیر مدل Vosk
vosk_model_path = "vosk-models/vosk-model-fa-0.5"

def video_to_audio(video_path, audio_path=None):
    if audio_path is None:
        # استخراج نام فایل و تبدیل پسوند به .wav
        base_name = os.path.splitext(video_path)[0]
        audio_path = f"{base_name}.wav"

    # استفاده از ffmpeg برای تبدیل ویدئو به فایل صوتی
    command = f"ffmpeg -y -i \"{video_path}\" -vn -acodec pcm_s16le -ar 16000 -ac 1 \"{audio_path}\""
    subprocess.run(command, shell=True, check=True)
    return audio_path

def transcribe_audio_to_srt_vosk(audio_path, model_path=vosk_model_path):
    # بارگذاری مدل Vosk
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return

    model = VoskModel(model_path)

    # باز کردن فایل صوتی
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("Audio file must be WAV format mono PCM.")
        return

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    subs = []
    words_buffer = []
    start_time = 0
    total_frames = wf.getnframes()

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'result' in result:
                for item in result['result']:
                    word = item['word']
                    end_time = item['end']

                    # ذخیره کلمه در بافر
                    words_buffer.append(word)

                    # اگر تعداد کلمات در بافر به 5 یا بیشتر رسید
                    if len(words_buffer) == 1:
                        start_time = item['start']  # زمان شروع اولین کلمه

                    # اگر تعداد کلمات به 5 رسید، زیرنویس ایجاد کن
                    if len(words_buffer) == 5:
                        subs.append(
                            srt.Subtitle(
                                index=len(subs) + 1,
                                start=srt.timedelta(seconds=start_time),
                                end=srt.timedelta(seconds=end_time),
                                content=' '.join(words_buffer),
                            )
                        )
                        words_buffer = []  # خالی کردن بافر کلمات
                        start_time = 0  # بازنشانی زمان شروع

        # نمایش پیشرفت
        current_frame = wf.tell()
        progress = (current_frame / total_frames) * 100
        sys.stdout.write(f"\rProcessing audio: {progress:.2f}% completed")
        sys.stdout.flush()

    # بررسی و اضافه کردن زیرنویس باقی‌مانده
    if len(words_buffer) > 0:
        subs.append(
            srt.Subtitle(
                index=len(subs) + 1,
                start=srt.timedelta(seconds=start_time),
                end=srt.timedelta(seconds=end_time),
                content=' '.join(words_buffer),
            )
        )

    wf.close()
    return subs

def write_srt_file(subtitles, output_path):
    with open(output_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt.compose(subtitles))

def generate_srt_from_video(video_path, vosk_model_path=vosk_model_path):
    # استخراج نام فایل ویدیویی بدون پسوند
    base_name = os.path.splitext(video_path)[0]
    output_srt = f"{base_name}.srt"

    audio_path = video_to_audio(video_path)

    # Transcribe with Vosk
    subtitles_vosk = transcribe_audio_to_srt_vosk(audio_path, vosk_model_path)
    if subtitles_vosk:
        write_srt_file(subtitles_vosk, output_srt)
        print(f"\nSRT file generated with Vosk: {output_srt}")
    else:
        print("No subtitles generated with Vosk.")
