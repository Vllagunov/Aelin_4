# C:\01 Ai\03_world.py
# Аэлин — МИР
# Версия 0.1

from __future__ import annotations

from datetime import datetime


MODULE_NAME = "03_world"
VERSION = "0.1"


class World:
    """Внутренняя модель мира Аэлин."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")

        self.state = {
            "self": {
                "name": "Аэлин",
                "known": [],
                "unknown": [],
                "interests": [],
                "goals": [],
            },
            "vladimir": {
                "known": [],
                "unknown": [],
                "interests": [],
            },
            "world": {
                "known": [],
                "unknown": [],
            },
        }

    def module_info(self):
        return {
            "name": "МИР",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Внутренняя модель мира Аэлин",
        }

    def self_test(self):
        try:
            required = ("self", "vladimir", "world")

            for item in required:
                if item not in self.state:
                    return {
                        "status": "FAIL",
                        "message": f"Отсутствует раздел: {item}",
                    }

            return {
                "status": "PASS",
                "message": "Модель мира создана",
                "state": self.get_state(),
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def get_state(self):
        return self.state

    def add_known(self, subject, fact):
        if subject not in self.state:
            return False

        if fact not in self.state[subject]["known"]:
            self.state[subject]["known"].append(fact)

        return True

    def add_unknown(self, subject, question):
        if subject not in self.state:
            return False

        if question not in self.state[subject]["unknown"]:
            self.state[subject]["unknown"].append(question)

        return True

    def add_interest(self, subject, interest):
        if subject not in self.state:
            return False

        if "interests" not in self.state[subject]:
            self.state[subject]["interests"] = []

        if interest not in self.state[subject]["interests"]:
            self.state[subject]["interests"].append(interest)

        return True

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

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "state": self.get_state(),
            }

        if msg_type == "ADD_KNOWN":
            subject = message.get("subject")
            fact = message.get("fact")

            if not subject or not fact:
                return {
                    "status": "FAIL",
                    "message": "Не указан субъект или факт",
                }

            if self.add_known(subject, fact):
                return {
                    "status": "PASS",
                    "message": "Факт добавлен",
                }

            return {
                "status": "FAIL",
                "message": f"Неизвестный субъект: {subject}",
            }

        if msg_type == "ADD_UNKNOWN":
            subject = message.get("subject")
            question = message.get("question")

            if not subject or not question:
                return {
                    "status": "FAIL",
                    "message": "Не указан субъект или вопрос",
                }

            if self.add_unknown(subject, question):
                return {
                    "status": "PASS",
                    "message": "Неизвестное добавлено",
                }

            return {
                "status": "FAIL",
                "message": f"Неизвестный субъект: {subject}",
            }

        if msg_type == "ADD_INTEREST":
            subject = message.get("subject")
            interest = message.get("interest")

            if not subject or not interest:
                return {
                    "status": "FAIL",
                    "message": "Не указан субъект или интерес",
                }

            if self.add_interest(subject, interest):
                return {
                    "status": "PASS",
                    "message": "Интерес добавлен",
                }

            return {
                "status": "FAIL",
                "message": f"Неизвестный субъект: {subject}",
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль МИР завершён",
        }


def create_module():
    return World()


def main():
    print()
    print("=== АЭЛИН: МИР ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    world = World()
    result = world.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Внутренняя модель мира создана.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()