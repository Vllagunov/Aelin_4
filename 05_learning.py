from __future__ import annotations

from datetime import datetime


MODULE_NAME = "05_learning"
VERSION = "0.2"


class Learning:
    """Модуль накопления опыта и изменения состояния Аэлин."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")

        self.experiences = []
        self.learned = []

    def module_info(self):
        return {
            "name": "ОБУЧЕНИЕ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Накопление опыта и формирование новых знаний",
        }

    def self_test(self):
        try:
            if not isinstance(self.experiences, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище опыта недоступно",
                }

            if not isinstance(self.learned, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище знаний недоступно",
                }

            test_experience = {
                "source": "SELF_TEST",
                "content": "тестовый опыт",
            }

            result = self.learn(test_experience)

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Опыт не обработан",
                }

            if self.experiences:
                self.experiences.pop()

            if self.learned:
                self.learned.pop()

            return {
                "status": "PASS",
                "message": "Модуль обучения работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def learn(self, experience):
        """
        Обрабатывает новый опыт.

        На первом этапе опыт сохраняется и превращается
        в элемент накопленного знания.
        """

        if not isinstance(experience, dict):
            return None

        content = experience.get("content")

        if not content:
            return None

        record = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "experience": experience,
        }

        self.experiences.append(record)

        knowledge = {
            "time": record["time"],
            "content": content,
            "source": experience.get("source", "UNKNOWN"),
        }

        self.learned.append(knowledge)

        return knowledge

    def get_experiences(self, limit=20):
        return self.experiences[-limit:]

    def get_learned(self, limit=20):
        return self.learned[-limit:]

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

        if msg_type == "LEARN":
            experience = message.get("experience")

            result = self.learn(experience)

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось обработать опыт",
                }

            return {
                "status": "PASS",
                "learned": result,
            }

        if msg_type == "EXPERIENCE":
            experience = {
                "source": "SCENARIO",
                "content": message,
            }

            result = self.learn(experience)

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось сохранить опыт",
                }

            return {
                "status": "PASS",
                "learned": result,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "experiences_count": len(self.experiences),
                "learned_count": len(self.learned),
                "learned": self.get_learned(),
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль ОБУЧЕНИЕ завершён",
        }


def create_module():
    return Learning()


def main():
    print()
    print("=== АЭЛИН: ОБУЧЕНИЕ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    module = Learning()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Модуль обучения готов к работе.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()