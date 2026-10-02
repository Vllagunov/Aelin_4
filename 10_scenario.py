# C:\01 Ai\10_scenario.py
# Аэлин — СЦЕНАРИЙ
# Версия 0.2
#
# Назначение:
# Загрузка исходных условий эксперимента из scenario.txt.
#
# Модуль НЕ интерпретирует параметры
# и НЕ принимает решения.
#
# Он только загружает и передаёт:
#   - условия сценария;
#   - потребности;
#   - шаблон действий.
#
# Интерпретацией шаблона занимается 11_interpreter.py.

from __future__ import annotations

from pathlib import Path


MODULE_NAME = "10_scenario"
VERSION = "0.2"

BASE_DIR = Path(__file__).resolve().parent
SCENARIO_FILE = BASE_DIR / "scenario.txt"

SECTIONS = [
    "ВРОЖДЕННЫЕ_СПОСОБНОСТИ",
    "ВНЕШНИЙ_МИР",
    "ОБЪЕКТЫ_МИРА",
    "ПОТРЕБНОСТИ",
    "ШАБЛОН",
    "СТЕПЕНЬ_АНАЛИЗА",
    "СТЕПЕНЬ_ОБУЧЕНИЯ",
]


class Scenario:

    def __init__(self):
        self.data = {}
        self.loaded = False

        self.load()

    # ------------------------------------------------------------------
    # ИНФОРМАЦИЯ О МОДУЛЕ
    # ------------------------------------------------------------------

    def module_info(self):
        return {
            "name": "СЦЕНАРИЙ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": (
                "Загрузка условий эксперимента, "
                "потребности и шаблона из scenario.txt"
            ),
        }

    # ------------------------------------------------------------------
    # ЗАГРУЗКА СЦЕНАРИЯ
    # ------------------------------------------------------------------

    def load(self):

        self.data = {
            section: []
            for section in SECTIONS
        }

        if not SCENARIO_FILE.exists():
            self.loaded = False
            return

        current_section = None

        with open(
            SCENARIO_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            for raw_line in f:

                line = raw_line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):

                    section = line[1:-1].strip()

                    if section in SECTIONS:
                        current_section = section
                    else:
                        current_section = None

                    continue

                if current_section is not None:
                    self.data[current_section].append(line)

        self.loaded = True

    # ------------------------------------------------------------------
    # САМОТЕСТ
    # ------------------------------------------------------------------

    def self_test(self):

        if not SCENARIO_FILE.exists():
            return {
                "status": "FAIL",
                "message": "Файл scenario.txt не найден",
            }

        missing = [
            section
            for section in SECTIONS
            if section not in self.data
        ]

        if missing:
            return {
                "status": "FAIL",
                "message": "Отсутствуют разделы: "
                           + ", ".join(missing),
            }

        return {
            "status": "PASS",
            "message": "Сценарий загружен",
        }

    # ------------------------------------------------------------------
    # ПОЛУЧИТЬ ВЕСЬ СЦЕНАРИЙ
    # ------------------------------------------------------------------

    def get_scenario(self):

        return {
            section: list(values)
            for section, values in self.data.items()
        }

    # ------------------------------------------------------------------
    # ПОЛУЧИТЬ ПОТРЕБНОСТЬ
    # ------------------------------------------------------------------

    def get_needs(self):

        return list(
            self.data.get("ПОТРЕБНОСТИ", [])
        )

    # ------------------------------------------------------------------
    # ПОЛУЧИТЬ ШАБЛОН
    # ------------------------------------------------------------------

    def get_template(self):

        return list(
            self.data.get("ШАБЛОН", [])
        )

    # ------------------------------------------------------------------
    # ОБРАБОТКА СООБЩЕНИЙ
    # ------------------------------------------------------------------

    def handle(self, message):

        if not isinstance(message, dict):
            return {
                "status": "FAIL",
                "message": "Сообщение должно быть словарём",
            }

        msg_type = message.get("type")

        # --------------------------------------------------------------
        # ПРОВЕРКА СВЯЗИ
        # --------------------------------------------------------------

        if msg_type == "TEST":

            return {
                "status": "PASS",
                "module": MODULE_NAME,
                "message": "PONG",
            }

        # --------------------------------------------------------------
        # ЗАГРУЗКА
        # --------------------------------------------------------------

        if msg_type == "LOAD":

            self.load()

            return {
                "status": "PASS" if self.loaded else "FAIL",
                "message": (
                    "Сценарий загружен"
                    if self.loaded
                    else "Файл scenario.txt не найден"
                ),
            }

        # --------------------------------------------------------------
        # ПОЛУЧИТЬ ВЕСЬ СЦЕНАРИЙ
        # --------------------------------------------------------------

        if msg_type == "GET":

            return {
                "status": "PASS",
                "scenario": self.get_scenario(),
            }

        # --------------------------------------------------------------
        # ПОЛУЧИТЬ ПОТРЕБНОСТЬ
        # --------------------------------------------------------------

        if msg_type == "GET_NEEDS":

            return {
                "status": "PASS",
                "needs": self.get_needs(),
            }

        # --------------------------------------------------------------
        # ПОЛУЧИТЬ ШАБЛОН
        # --------------------------------------------------------------

        if msg_type == "GET_TEMPLATE":

            return {
                "status": "PASS",
                "template": self.get_template(),
            }

        # --------------------------------------------------------------
        # СОСТОЯНИЕ
        # --------------------------------------------------------------

        if msg_type == "STATE":

            return {
                "status": "PASS",
                "loaded": self.loaded,
                "file": str(SCENARIO_FILE),
                "scenario": self.get_scenario(),
                "needs": self.get_needs(),
                "template": self.get_template(),
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    # ------------------------------------------------------------------
    # ЗАВЕРШЕНИЕ
    # ------------------------------------------------------------------

    def shutdown(self):

        return {
            "status": "PASS",
            "message": "Модуль СЦЕНАРИЙ завершён",
        }


# ----------------------------------------------------------------------
# СОЗДАНИЕ МОДУЛЯ
# ----------------------------------------------------------------------

def create_module():

    return Scenario()


# ----------------------------------------------------------------------
# ЗАПУСК МОДУЛЯ ОТДЕЛЬНО
# ----------------------------------------------------------------------

def main():

    print()
    print("=== АЭЛИН: СЦЕНАРИЙ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print(f"Файл: {SCENARIO_FILE}")
    print("Статус: ЗАПУЩЕН")
    print()

    module = Scenario()

    result = module.self_test()

    print(f"Самотест: {result['status']}")
    print(result.get("message", ""))

    if result["status"] == "PASS":

        print()
        print("Загруженные параметры:")

        for section, values in module.data.items():

            print()
            print(f"[{section}]")

            for value in values:
                print(value)

        print()
        print("Потребности:")

        for need in module.get_needs():
            print(f"  {need}")

        print()
        print("Шаблон:")

        for command in module.get_template():
            print(f"  {command}")

        print()
        print("Состояние: READY")

    else:

        print("Состояние: ERROR")


if __name__ == "__main__":
    main()