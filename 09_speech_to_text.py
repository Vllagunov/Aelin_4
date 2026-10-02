
# C:\01 Ai\09_speech_to_text.py
# Аэлин — СЛУХ
# Версия 0.6
#
# Назначение:
# Запись речи с микрофона и распознавание через Whisper.
#
# Версия 0.6:
# - запись 5 секунд;
# - тестовый WAV сохраняется в C:\01 Ai\test_microphone.wav;
# - диагностика уровня сигнала;
# - вывод результата распознавания.

from __future__ import annotations

import os
from datetime import datetime

import sounddevice as sd
import soundfile as sf
import whisper


MODULE_NAME = "09_speech_to_text"
VERSION = "0.6"

SAMPLE_RATE = 16000
LISTEN_SECONDS = 5

TEST_WAV = r"C:\01 Ai\test_microphone.wav"


class SpeechToText:
    """Модуль распознавания речи через микрофон."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")
        self.model = None
        self.last_text = None

        print("=" * 60)
        print("Загрузка Whisper...")
        print("=" * 60)

        self.model = whisper.load_model("base")

        print("Whisper готов.")
        print("=" * 60)

    def module_info(self):
        return {
            "name": "СЛУХ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Распознавание речи через микрофон",
        }

    def self_test(self):
        try:
            if self.model is None:
                return {
                    "status": "FAIL",
                    "message": "Whisper не загружен",
                }

            return {
                "status": "PASS",
                "module": MODULE_NAME,
                "message": "Модуль слуха работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def record(self, seconds=LISTEN_SECONDS):
        """Записывает звук с микрофона."""

        print()
        print(f"Говорите... Запись {seconds} секунд.")

        audio = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        signal_max = float(abs(audio).max())
        signal_mean = float(abs(audio).mean())
        samples = len(audio)

        print()
        print("[МИКРОФОН] Запись завершена.")
        print(f"[МИКРОФОН] Отсчётов: {samples}")
        print(f"[МИКРОФОН] Максимальный сигнал: {signal_max:.6f}")
        print(f"[МИКРОФОН] Средний сигнал: {signal_mean:.6f}")

        if signal_max == 0:
            print("[МИКРОФОН] ВНИМАНИЕ: сигнал отсутствует.")
        elif signal_max < 0.001:
            print("[МИКРОФОН] ВНИМАНИЕ: сигнал очень слабый.")
        else:
            print("[МИКРОФОН] Сигнал с микрофона получен.")

        # Сохраняем тестовую запись.
        sf.write(
            TEST_WAV,
            audio,
            SAMPLE_RATE,
        )

        print()
        print("[МИКРОФОН] Тестовая запись сохранена:")
        print(TEST_WAV)

        return TEST_WAV

    def recognize(self, filename):
        """Распознаёт WAV через Whisper."""

        audio, samplerate = sf.read(
            filename,
            dtype="float32",
        )

        if samplerate != SAMPLE_RATE:
            raise ValueError(
                f"Неверная частота дискретизации: {samplerate}"
            )

        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)

        result = self.model.transcribe(
            audio,
            language="ru",
        )

        text = result.get("text", "").strip()

        self.last_text = text

        print()
        print(f"[WHISPER] Распознано: {text}")

        if not text:
            print("[WHISPER] Текст не распознан.")

        return text

    def listen(self):
        """Записывает и распознаёт речь."""

        filename = self.record()

        return self.recognize(filename)

    def handle(self, message):
        if not isinstance(message, dict):
            return {
                "status": "FAIL",
                "message": "Сообщение должно быть словарём",
            }

        msg_type = message.get("type")

        if msg_type == "TEST":
            return {
                "status": "PASS",
                "module": MODULE_NAME,
                "message": "PONG",
            }

        if msg_type == "LISTEN":
            text = self.listen()

            return {
                "status": "PASS",
                "text": text,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "last_text": self.last_text,
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль СЛУХ завершён",
        }


def create_module():
    return SpeechToText()


def main():
    print()
    print("=== АЭЛИН: СЛУХ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")

    module = SpeechToText()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()

