# C:\01 Ai\07_questions.py
# Аэлин — АВТОНОМНЫЕ ВОПРОСЫ
# Версия 0.1

from __future__ import annotations

from datetime import datetime


MODULE_NAME = "07_questions"
VERSION = "0.1"


class Questions:
    """Формирование вопросов из обнаруженных неизвестных."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")
        self.unknowns = []
        self.questions = []
        self.last_question = None

    def module_info(self):
        return {
            "name": "ВОПРОСЫ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Формирование собственных вопросов из неизвестного",
        }

    def self_test(self):
        try:
            if not isinstance(self.unknowns, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище неизвестного недоступно",
                }

            if not isinstance(self.questions, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище вопросов недоступно",
                }

            test_result = self.add_unknown(
                "SELF_TEST",
                "Что необходимо понять?"
            )

            if not test_result:
                return {
                    "status": "FAIL",
                    "message": "Не удалось добавить неизвестное",
                }

            question = self.form_question()

            if question is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось сформировать вопрос",
                }

            self.unknowns.clear()
            self.questions.clear()
            self.last_question = None

            return {
                "status": "PASS",
                "message": "Модуль автономных вопросов работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def add_unknown(self, subject, unknown):
        if not subject or not unknown:
            return False

        item = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "subject": subject,
            "unknown": unknown,
        }

        self.unknowns.append(item)
        return True

    def form_question(self):
        """Формирует вопрос из первого доступного неизвестного."""

        if not self.unknowns:
            return None

        unknown = self.unknowns[-1]

        question = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "subject": unknown["subject"],
            "question": unknown["unknown"],
        }

        self.last_question = question
        self.questions.append(question)

        return question

    def get_unknowns(self, limit=20):
        return self.unknowns[-limit:]

    def get_questions(self, limit=20):
        return self.questions[-limit:]

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

        if msg_type == "ADD_UNKNOWN":
            subject = message.get("subject")
            unknown = message.get("unknown")

            if not self.add_unknown(subject, unknown):
                return {
                    "status": "FAIL",
                    "message": "Не удалось добавить неизвестное",
                }

            return {
                "status": "PASS",
                "message": "Неизвестное добавлено",
            }

        if msg_type == "FORM_QUESTION":
            question = self.form_question()

            if question is None:
                return {
                    "status": "FAIL",
                    "message": "Нет неизвестного для формирования вопроса",
                }

            return {
                "status": "PASS",
                "question": question,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "unknowns_count": len(self.unknowns),
                "questions_count": len(self.questions),
                "last_question": self.last_question,
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль ВОПРОСЫ завершён",
        }


def create_module():
    return Questions()


def main():
    print()
    print("=== АЭЛИН: ВОПРОСЫ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    module = Questions()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Модуль автономных вопросов готов к работе.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()