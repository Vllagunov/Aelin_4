# C:\01 Ai\00_monitor.py
# Аэлин — МОНИТОР
# Версия 0.7
#
# Назначение:
# Загрузка модулей Аэлин.
# Самотестирование.
# Проверка связей.
# Подключение интерпретатора.
# Запуск сценария.
#
# Версия 0.7:
# - запуск двух циклов сценария;
# - после 7 секунд информация обновляется;
# - Ctrl+C останавливает программу;
# - результат эксперимента записывается в журнал и отчёт.

from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path


VERSION = "0.7"

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"


MODULES = [
    ("01_core", "01_core.py"),
    ("02_memory", "02_memory.py"),
    ("03_world", "03_world.py"),
    ("04_prediction", "04_prediction.py"),
    ("05_learning", "05_learning.py"),
    ("06_perception", "06_perception.py"),
    ("07_questions", "07_questions.py"),
    ("08_voice", "08_voice.py"),
    ("09_speech_to_text", "09_speech_to_text.py"),
    ("10_scenario", "10_scenario.py"),
    ("11_interpreter", "11_interpreter.py"),
]


MODULE_NAMES_RU = {
    "01_core": "ЯДРО",
    "02_memory": "ПАМЯТЬ",
    "03_world": "МИР",
    "04_prediction": "ПРОГНОЗ",
    "05_learning": "ОБУЧЕНИЕ",
    "06_perception": "ВОСПРИЯТИЕ",
    "07_questions": "ВОПРОСЫ",
    "08_voice": "ГОЛОС",
    "09_speech_to_text": "СЛУХ",
    "10_scenario": "СЦЕНАРИЙ",
    "11_interpreter": "ИНТЕРПРЕТАТОР",
}


class Monitor:

    def __init__(self):
        self.modules = {}
        self.events = []
        self.experiment_result = None

        LOG_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.log_file = LOG_DIR / f"monitor_{timestamp}.jsonl"
        self.report_file = LOG_DIR / f"monitor_{timestamp}_report.txt"

    def log(self, event, data=None):
        record = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "event": event,
            "data": data,
        }

        self.events.append(record)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    def load_module(self, module_id, filename):
        path = BASE_DIR / filename

        if not path.exists():
            return False, "Файл не найден"

        try:
            spec = importlib.util.spec_from_file_location(
                module_id,
                path,
            )

            if spec is None or spec.loader is None:
                return False, "Не удалось создать загрузчик"

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if not hasattr(module, "create_module"):
                return False, "Нет create_module()"

            instance = module.create_module()

            required = [
                "module_info",
                "self_test",
                "handle",
                "shutdown",
            ]

            for name in required:
                if not hasattr(instance, name):
                    return False, f"Нет метода {name}()"

            self.modules[module_id] = instance

            info = instance.module_info()

            self.log(
                "MODULE_LOADED",
                {
                    "module": module_id,
                    "info": info,
                },
            )

            return True, info

        except Exception as e:

            self.log(
                "MODULE_LOAD_ERROR",
                {
                    "module": module_id,
                    "error": str(e),
                },
            )

            return False, str(e)

    def self_test_module(self, module_id, instance):

        try:
            result = instance.self_test()

            self.log(
                "SELF_TEST",
                {
                    "module": module_id,
                    "result": result,
                },
            )

            return result

        except Exception as e:

            result = {
                "status": "FAIL",
                "message": str(e),
            }

            self.log(
                "SELF_TEST_ERROR",
                {
                    "module": module_id,
                    "error": str(e),
                },
            )

            return result

    def connection_test(self, module_id, instance):

        try:

            result = instance.handle(
                {
                    "type": "TEST",
                    "source": "MONITOR",
                    "test": "connection",
                    "payload": "PING",
                }
            )

            self.log(
                "CONNECTION_TEST",
                {
                    "module": module_id,
                    "result": result,
                },
            )

            if isinstance(result, dict):
                return result.get("status") == "PASS"

            return False

        except Exception as e:

            self.log(
                "CONNECTION_ERROR",
                {
                    "module": module_id,
                    "error": str(e),
                },
            )

            return False

    def connect_interpreter(self):

        interpreter = self.modules.get("11_interpreter")

        if interpreter is None:
            self.log(
                "INTERPRETER_CONNECTION_ERROR",
                {
                    "message": "Интерпретатор не загружен",
                },
            )

            return False

        try:

            interpreter.scenario = self.modules.get("10_scenario")
            interpreter.voice = self.modules.get("08_voice")
            interpreter.speech_to_text = self.modules.get(
                "09_speech_to_text"
            )
            interpreter.learning = self.modules.get(
                "05_learning"
            )

            self.log(
                "INTERPRETER_CONNECTED",
                {
                    "scenario": "10_scenario",
                    "voice": "08_voice",
                    "speech_to_text": "09_speech_to_text",
                    "learning": "05_learning",
                },
            )

            return True

        except Exception as e:

            self.log(
                "INTERPRETER_CONNECTION_ERROR",
                {
                    "error": str(e),
                },
            )

            return False

    def run_experiment(self):

        interpreter = self.modules.get("11_interpreter")

        if interpreter is None:

            result = {
                "status": "FAIL",
                "message": "Интерпретатор не загружен",
            }

            self.experiment_result = result

            return result

        print()
        print("=== ПЕРВЫЙ ЦИКЛ АЭЛИН ===")
        print()

        print("Шаблон сценария:")

        template = interpreter.get_template()

        for line in template:
            print(f"  {line}")

        print()

        print("Запуск сценария.")
        print("Для остановки нажмите Ctrl+C.")
        print()

        try:

            result = interpreter.run(cycles=2)

        except KeyboardInterrupt:

            print()
            print("Получен Ctrl+C.")
            print("Остановка Аэлин...")

            interpreter.shutdown()

            result = {
                "status": "STOPPED",
                "message": "Остановлено пользователем через Ctrl+C",
                "cycles_completed": interpreter.cycle_count,
            }

        self.experiment_result = result

        self.log(
            "EXPERIMENT_RESULT",
            {
                "module": "11_interpreter",
                "result": result,
            },
        )

        print()

        status = result.get("status")

        if status == "PASS":

            print("=== СЦЕНАРИЙ ЗАВЕРШЁН ===")
            print(
                f"Выполнено циклов: "
                f"{result.get('cycles_completed', 0)}"
            )

        elif status == "STOPPED":

            print("=== АЭЛИН ОСТАНОВЛЕНА ===")

        else:

            print("=== ОШИБКА СЦЕНАРИЯ ===")

            print(
                result.get(
                    "message",
                    result,
                )
            )

        return result

    def write_report(self, ready):

        with open(
            self.report_file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write("АЭЛИН — ОТЧЁТ МОНИТОРА\n")
            f.write("=" * 60 + "\n")

            f.write(
                f"Версия монитора: {VERSION}\n"
            )

            f.write(
                "Время: "
                f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
            )

            f.write("\nМОДУЛИ:\n")

            for module_id, filename in MODULES:

                name = MODULE_NAMES_RU.get(
                    module_id,
                    module_id,
                )

                if module_id in self.modules:

                    f.write(
                        f"{name:20} ЗАГРУЖЕН\n"
                    )

                else:

                    f.write(
                        f"{name:20} НЕ НАЙДЕН\n"
                    )

            f.write("\n")

            if ready:
                f.write(
                    "СТАТУС АЭЛИН: READY\n"
                )
            else:
                f.write(
                    "СТАТУС АЭЛИН: NOT READY\n"
                )

            if self.experiment_result is not None:

                f.write("\n")
                f.write("ЭКСПЕРИМЕНТ:\n")

                f.write(
                    json.dumps(
                        self.experiment_result,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

                f.write("\n")

    def run(self):

        print()
        print("=== ЗАПУСК АЭЛИН ===")
        print()

        print(
            f"[00] МОНИТОР v{VERSION}        ЗАГРУЖЕН"
        )

        print()

        self.log(
            "MONITOR_START",
            {
                "version": VERSION,
            },
        )

        loaded = []

        for index, (module_id, filename) in enumerate(
            MODULES,
            start=1,
        ):

            name = MODULE_NAMES_RU.get(
                module_id,
                module_id,
            )

            ok, result = self.load_module(
                module_id,
                filename,
            )

            if ok:

                print(
                    f"[{index:02}] "
                    f"{name:16} ЗАГРУЖЕН"
                )

                loaded.append(module_id)

            else:

                print(
                    f"[{index:02}] "
                    f"{name:16} НЕ НАЙДЕН"
                )

                self.log(
                    "MODULE_NOT_LOADED",
                    {
                        "module": module_id,
                        "reason": result,
                    },
                )

        print()

        print("=== САМОТЕСТ МОДУЛЕЙ ===")

        self_tests_ok = True

        for module_id in loaded:

            name = MODULE_NAMES_RU.get(
                module_id,
                module_id,
            )

            result = self.self_test_module(
                module_id,
                self.modules[module_id],
            )

            status = result.get(
                "status",
                "FAIL",
            )

            print(
                f"{name:20} {status}"
            )

            if status != "PASS":
                self_tests_ok = False

        print()

        print("=== ПОДКЛЮЧЕНИЕ ИНТЕРПРЕТАТОРА ===")

        interpreter_connected = self.connect_interpreter()

        if interpreter_connected:

            print(
                "ИНТЕРПРЕТАТОР       CONNECTED"
            )

        else:

            print(
                "ИНТЕРПРЕТАТОР       FAILED"
            )

        print()

        print("=== ПРОВЕРКА СВЯЗЕЙ ===")

        connections_ok = True

        for module_id in loaded:

            name = MODULE_NAMES_RU.get(
                module_id,
                module_id,
            )

            ok = self.connection_test(
                module_id,
                self.modules[module_id],
            )

            status = "PASS" if ok else "FAIL"

            print(
                f"МОНИТОР → "
                f"{name:12} {status}"
            )

            if not ok:
                connections_ok = False

        print()

        all_loaded = (
            len(loaded) == len(MODULES)
        )

        ready = (
            all_loaded
            and self_tests_ok
            and connections_ok
            and interpreter_connected
        )

        if ready:

            print("=== АЭЛИН ГОТОВА ===")

            self.log(
                "AELIN_READY",
                {
                    "status": "READY",
                },
            )

        else:

            print("=== АЭЛИН НЕ ГОТОВА ===")

            self.log(
                "AELIN_NOT_READY",
                {
                    "status": "NOT_READY",
                    "loaded": loaded,
                    "all_loaded": all_loaded,
                    "self_tests": self_tests_ok,
                    "connections": connections_ok,
                    "interpreter_connected": interpreter_connected,
                },
            )

        self.write_report(ready)

        if ready:

            self.run_experiment()

            self.write_report(True)

        print()

        print(
            f"Журнал: {self.log_file}"
        )

        print(
            f"Отчёт : {self.report_file}"
        )


def main():

    monitor = Monitor()

    try:

        monitor.run()

    except KeyboardInterrupt:

        print()
        print("Аэлин остановлена пользователем.")


if __name__ == "__main__":
    main()