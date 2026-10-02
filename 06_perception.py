# C:\01 Ai\06_perception.py
# Аэлин — ВОСПРИЯТИЕ
# Версия 0.1

from __future__ import annotations

from datetime import datetime


MODULE_NAME = "06_perception"
VERSION = "0.1"


class Perception:
    """Модуль восприятия и первичной обработки информации."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")
        self.last_input = None
        self.inputs = []

    def module_info(self):
        return {
            "name": "ВОСПРИЯТИЕ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Получение и первичная обработка входящей информации",
        }

    def self_test(self):
        try:
            if not isinstance(self.inputs, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище входных данных недоступно",
                }

            result = self.process_input("тестовое сообщение")

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Входная информация не обработана",
                }

            self.inputs.clear()
            self.last_input = None

            return {
                "status": "PASS",
                "message": "Модуль восприятия работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def process_input(self, data):
        """Получает входные данные и приводит их к единому виду."""

        if data is None:
            return None

        if isinstance(data, str):
            content = data.strip()
            input_type = "text"

        elif isinstance(data, dict):
            content = data.get("content")

            if content is None:
                return None

            input_type = data.get("source_type", "data")

        else:
            content = str(data)
            input_type = "data"

        if not content:
            return None

        result = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "type": input_type,
            "content": content,
        }

        self.last_input = result
        self.inputs.append(result)

        return result

    def get_last_input(self):
        return self.last_input

    def get_inputs(self, limit=20):
        return self.inputs[-limit:]

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

        if msg_type == "PERCEIVE":
            data = message.get("data")

            result = self.process_input(data)

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось обработать входные данные",
                }

            return {
                "status": "PASS",
                "perception": result,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "last_input": self.last_input,
                "inputs_count": len(self.inputs),
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль ВОСПРИЯТИЕ завершён",
        }


def create_module():
    return Perception()


def main():
    print()
    print("=== АЭЛИН: ВОСПРИЯТИЕ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    module = Perception()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Модуль восприятия готов к работе.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()