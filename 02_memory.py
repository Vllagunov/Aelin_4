# 02_memory.py
# Аэлин — модуль 02: Постоянная память
# Версия 0.2

import json
from pathlib import Path
from datetime import datetime


MODULE_NAME = "02_memory"
VERSION = "0.2"

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory.json"


class Memory:
    """Постоянная память Аэлин."""

    def __init__(self):
        self.memory_file = MEMORY_FILE

        self.data = {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "dialogue": [],
            "facts": [],
            "questions": [],
        }

        self.load()

    # ---------------------------------------------------------
    # ИНФОРМАЦИЯ О МОДУЛЕ
    # ---------------------------------------------------------

    def module_info(self):
        return {
            "name": "ПАМЯТЬ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Постоянная память Аэлин",
        }

    # ---------------------------------------------------------
    # ЗАГРУЗКА
    # ---------------------------------------------------------

    def load(self):
        if not self.memory_file.exists():
            self.save()
            return

        try:
            with self.memory_file.open(
                "r",
                encoding="utf-8"
            ) as file:
                loaded = json.load(file)

            if isinstance(loaded, dict):
                self.data.update(loaded)

        except Exception:
            # При повреждённой памяти начинаем с пустой структуры.
            self.data = {
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "dialogue": [],
                "facts": [],
                "questions": [],
            }

    # ---------------------------------------------------------
    # СОХРАНЕНИЕ
    # ---------------------------------------------------------

    def save(self):
        self.data["updated"] = datetime.now().isoformat()

        with self.memory_file.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2,
            )

    # ---------------------------------------------------------
    # ДИАЛОГ
    # ---------------------------------------------------------

    def add_message(self, role, text):
        record = {
            "time": datetime.now().isoformat(),
            "role": role,
            "text": str(text),
        }

        self.data["dialogue"].append(record)
        self.save()

        return record

    def get_dialogue(self, limit=20):
        return self.data["dialogue"][-limit:]

    # ---------------------------------------------------------
    # ФАКТЫ
    # ---------------------------------------------------------

    def add_fact(self, fact):
        fact = str(fact).strip()

        if not fact:
            return False

        if fact not in self.data["facts"]:
            self.data["facts"].append(fact)
            self.save()

        return True

    def get_facts(self):
        return list(self.data["facts"])

    # ---------------------------------------------------------
    # ВОПРОСЫ АЭЛИН
    # ---------------------------------------------------------

    def add_question(self, question):
        question = str(question).strip()

        if not question:
            return False

        record = {
            "time": datetime.now().isoformat(),
            "question": question,
        }

        self.data["questions"].append(record)
        self.save()

        return True

    def get_questions(self, limit=20):
        return self.data["questions"][-limit:]

    # ---------------------------------------------------------
    # ПОИСК
    # ---------------------------------------------------------

    def search(self, text):
        query = str(text).lower().strip()

        if not query:
            return []

        results = []

        for record in self.data["dialogue"]:
            if query in record.get("text", "").lower():
                results.append(record)

        for fact in self.data["facts"]:
            if query in fact.lower():
                results.append({
                    "type": "fact",
                    "text": fact,
                })

        for record in self.data["questions"]:
            if query in record.get("question", "").lower():
                results.append({
                    "type": "question",
                    **record,
                })

        return results

    # ---------------------------------------------------------
    # СОСТОЯНИЕ
    # ---------------------------------------------------------

    def get_state(self):
        return {
            "dialogue": len(self.data["dialogue"]),
            "facts": len(self.data["facts"]),
            "questions": len(self.data["questions"]),
        }

    # ---------------------------------------------------------
    # САМОТЕСТ
    # ---------------------------------------------------------

    def self_test(self):
        required = (
            "dialogue",
            "facts",
            "questions",
        )

        for key in required:
            if key not in self.data:
                return {
                    "status": "FAIL",
                    "error": f"Отсутствует раздел: {key}",
                }

        try:
            self.save()

            return {
                "status": "PASS",
                "message": "Память доступна",
                "state": self.get_state(),
            }

        except Exception as error:
            return {
                "status": "FAIL",
                "error": str(error),
            }

    # ---------------------------------------------------------
    # ОБЩИЙ ИНТЕРФЕЙС
    # ---------------------------------------------------------

    def handle(self, message):
        if not isinstance(message, dict):
            return {
                "status": "FAIL",
                "error": "Некорректное сообщение",
            }

        message_type = message.get("type")

        # Проверка связи с Monitor
        if message_type == "TEST":
            return {
                "status": "PASS",
                "module": MODULE_NAME,
                "message": "PONG",
            }

        # Добавление сообщения
        if message_type == "ADD_MESSAGE":
            role = message.get("role", "unknown")
            text = message.get("text", "")

            record = self.add_message(role, text)

            return {
                "status": "PASS",
                "record": record,
            }

        # Получение последних сообщений
        if message_type == "GET_DIALOGUE":
            limit = message.get("limit", 20)

            return {
                "status": "PASS",
                "dialogue": self.get_dialogue(limit),
            }

        # Добавление факта
        if message_type == "ADD_FACT":
            fact = message.get("fact", "")

            return {
                "status": "PASS"
                if self.add_fact(fact)
                else "FAIL",
                "fact": fact,
            }

        # Добавление вопроса Аэлин
        if message_type == "ADD_QUESTION":
            question = message.get("question", "")

            return {
                "status": "PASS"
                if self.add_question(question)
                else "FAIL",
                "question": question,
            }

        # Состояние памяти
        if message_type == "STATE":
            return {
                "status": "PASS",
                "state": self.get_state(),
            }

        return {
            "status": "FAIL",
            "error": f"Неизвестный тип сообщения: {message_type}",
        }

    # ---------------------------------------------------------
    # ЗАВЕРШЕНИЕ
    # ---------------------------------------------------------

    def shutdown(self):
        self.save()


# -------------------------------------------------------------
# ФАБРИКА ДЛЯ MONITOR
# -------------------------------------------------------------

def create_module():
    return Memory()


# -------------------------------------------------------------
# САМОСТОЯТЕЛЬНЫЙ ЗАПУСК
# -------------------------------------------------------------

def main():
    print()
    print("=== АЭЛИН: ПАМЯТЬ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    memory = create_module()

    result = memory.self_test()

    print(
        f"Самотест: {result.get('status', 'FAIL')}"
    )

    if result.get("status") == "PASS":
        print("Состояние: READY")

        state = memory.get_state()

        print()
        print("Память готова к работе.")
        print(
            f"Диалогов: {state['dialogue']} | "
            f"Фактов: {state['facts']} | "
            f"Вопросов: {state['questions']}"
        )
    else:
        print("Состояние: ERROR")
        print(
            f"Причина: {result.get('error', 'неизвестная ошибка')}"
        )


if __name__ == "__main__":
    main()