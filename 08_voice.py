from __future__ import annotations

from datetime import datetime

import pyttsx3


MODULE_NAME = "08_voice"
VERSION = "0.3"


class Voice:
    """Модуль голосового ввода и вывода Аэлин."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")

        self.last_input = None
        self.last_output = None

        self.input_history = []
        self.output_history = []

    def module_info(self):
        return {
            "name": "ГОЛОС",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Голосовой ввод и вывод Аэлин",
        }

    def self_test(self):
        try:
            if not isinstance(self.input_history, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище голосового ввода недоступно",
                }

            if not isinstance(self.output_history, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище голосового вывода недоступно",
                }

            test_input = self.receive("тестовый голосовой ввод")

            if test_input is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось обработать голосовой ввод",
                }

            test_output = self.speak("тестовый голосовой вывод")

            if test_output is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось сформировать голосовой вывод",
                }

            self.input_history.clear()
            self.output_history.clear()

            self.last_input = None
            self.last_output = None

            return {
                "status": "PASS",
                "message": "Модуль голоса работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def receive(self, text):
        """Принимает распознанный текст голосового ввода."""

        if text is None:
            return None

        text = str(text).strip()

        if not text:
            return None

        result = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "type": "voice_input",
            "text": text,
        }

        self.last_input = result
        self.input_history.append(result)

        return result

    def speak(self, text):
        """Произносит текст через системный синтезатор."""

        if text is None:
            return None

        text = str(text).strip()

        if not text:
            return None

        result = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "type": "voice_output",
            "text": text,
        }

        self.last_output = result
        self.output_history.append(result)

        engine = None

        try:
            # Движок создаём непосредственно перед озвучиванием.
            # Это повторяет рабочий механизм старого text_to_speech.py.
            engine = pyttsx3.init()

            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)

            engine.say(text)
            engine.runAndWait()

            return result

        finally:
            if engine is not None:
                try:
                    engine.stop()
                except Exception:
                    pass

    def get_last_input(self):
        return self.last_input

    def get_last_output(self):
        return self.last_output

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

        if msg_type == "VOICE_INPUT":
            result = self.receive(message.get("text"))

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Пустой голосовой ввод",
                }

            return {
                "status": "PASS",
                "input": result,
            }

        if msg_type == "VOICE_OUTPUT":
            result = self.speak(message.get("text"))

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Пустой голосовой вывод",
                }

            return {
                "status": "PASS",
                "output": result,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "last_input": self.last_input,
                "last_output": self.last_output,
                "input_count": len(self.input_history),
                "output_count": len(self.output_history),
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль ГОЛОС завершён",
        }


def create_module():
    return Voice()


def main():
    print()
    print("=== АЭЛИН: ГОЛОС ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    module = Voice()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Модуль голоса готов к интеграции.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()