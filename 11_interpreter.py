# C:\01 Ai\11_interpreter.py
# Аэлин — ИНТЕРПРЕТАТОР СЦЕНАРИЯ
# Версия 0.5
#
# Назначение:
# Исполнение текстового шаблона сценария.
#
# Версия 0.5:
# - циклическое выполнение сценария;
# - ожидание 7 секунд означает устаревание информации;
# - после ожидания сценарий начинается заново;
# - ограничение количества циклов;
# - команда СТОП;
# - вывод услышанного ответа и результата сравнения;
# - диагностический вывод голосового вывода;
# - диагностический вывод распознанного текста.

from __future__ import annotations

import time
from datetime import datetime


MODULE_NAME = "11_interpreter"
VERSION = "0.5"


class ScenarioInterpreter:

    def __init__(
        self,
        scenario=None,
        voice=None,
        speech_to_text=None,
        learning=None,
    ):
        self.scenario = scenario
        self.voice = voice
        self.speech_to_text = speech_to_text
        self.learning = learning

        self.state = "READY"

        self.command_count = 0
        self.cycle_count = 0

        self.last_command = None
        self.last_answer = None
        self.last_result = None

        self.stop_requested = False

    def module_info(self):
        return {
            "name": "ИНТЕРПРЕТАТОР СЦЕНАРИЯ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Исполнение текстового шаблона сценария Аэлин",
            "status": self.state,
        }

    def self_test(self):
        checks = {
            "interface": all(
                callable(getattr(self, name, None))
                for name in (
                    "module_info",
                    "self_test",
                    "handle",
                    "shutdown",
                )
            ),
            "state": self.state == "READY",
        }

        passed = all(checks.values())

        return {
            "status": "PASS" if passed else "FAIL",
            "module": MODULE_NAME,
            "checks": checks,
        }

    def get_template(self):
        if self.scenario is None:
            return []

        if hasattr(self.scenario, "get_template"):
            return self.scenario.get_template()

        return []

    def execute(self, command, argument=None):
        self.command_count += 1
        self.last_command = command

        if command == "ПРОИЗНЕСТИ":
            return self._speak(argument)

        if command == "ЖДАТЬ_ОТВЕТ":
            return self._wait_answer()

        if command == "СРАВНИТЬ":
            return self._compare(argument)

        if command == "ЗАПИСАТЬ_ОПЫТ":
            return self._save_experience()

        if command == "ЖДАТЬ":
            return self._wait(argument)

        if command == "СТОП":
            self.stop_requested = True
            self.state = "STOPPED"

            return {
                "status": "PASS",
                "command": "СТОП",
                "message": "Остановка запрошена",
            }

        return {
            "status": "FAIL",
            "command": command,
            "message": f"Неизвестная команда: {command}",
        }

    def run_template(self):
        template = self.get_template()

        if not template:
            return {
                "status": "FAIL",
                "message": "Шаблон сценария отсутствует",
            }

        self.cycle_count += 1
        self.last_answer = None
        self.last_result = None

        for line in template:

            if self.stop_requested:
                return {
                    "status": "STOPPED",
                    "cycle": self.cycle_count,
                }

            command, argument = self._parse_command(line)

            if not command:
                continue

            result = self.execute(command, argument)

            if command == "СРАВНИТЬ":
                print()
                print(f"Ответ Аэлин: {self.last_answer}")
                print(
                    f"Результат: "
                    f"{result.get('conclusion', result.get('message', ''))}"
                )
                print()

            if command == "ЖДАТЬ":
                self.last_result = result
                continue

            if result.get("status") != "PASS":
                self.last_result = result

                return {
                    "status": "FAIL",
                    "cycle": self.cycle_count,
                    "command": command,
                    "result": result,
                }

            self.last_result = result

        return {
            "status": "PASS",
            "cycle": self.cycle_count,
            "answer": self.last_answer,
            "result": self.last_result,
        }

    def run(self, cycles=2):
        self.state = "RUNNING"
        self.stop_requested = False

        try:
            while not self.stop_requested:

                if cycles is not None and self.cycle_count >= cycles:
                    break

                result = self.run_template()

                if result.get("status") == "FAIL":
                    self.state = "ERROR"
                    return result

                if result.get("status") == "STOPPED":
                    break

                print(
                    f"Цикл {self.cycle_count} завершён. "
                    f"Ожидание обновления информации..."
                )

        except KeyboardInterrupt:
            print()
            print("Получен Ctrl+C.")
            print("Остановка Аэлин...")

            self.stop_requested = True

        self.state = "STOPPED"

        return {
            "status": "PASS",
            "cycles_completed": self.cycle_count,
            "message": "Работа сценария завершена",
        }

    def _speak(self, text):
        if not text:
            return {
                "status": "FAIL",
                "message": "Отсутствует текст для произнесения",
            }

        if self.voice is None:
            return {
                "status": "FAIL",
                "message": "Модуль ГОЛОС не подключён",
            }

        print()
        print(f"[ГОЛОС] Команда на произнесение: {text}")

        try:
            result = self.voice.speak(text)

            print("[ГОЛОС] Вызов voice.speak() выполнен.")
            print(f"[ГОЛОС] Результат: {result}")

            if isinstance(result, dict):
                if result.get("status") == "FAIL":
                    return result

            print("[ГОЛОС] Команда считается выполненной.")
            print()

            return {
                "status": "PASS",
                "command": "ПРОИЗНЕСТИ",
                "text": text,
            }

        except Exception as e:
            print(f"[ГОЛОС] ОШИБКА: {e}")
            print()

            return {
                "status": "FAIL",
                "message": str(e),
            }

    def _wait_answer(self):
        if self.speech_to_text is None:
            return {
                "status": "FAIL",
                "message": "Модуль СЛУХ не подключён",
            }

        print()
        print("[СЛУХ] Ожидание ответа...")
        print("[СЛУХ] Говорите...")

        try:
            answer = self.speech_to_text.listen()

            self.last_answer = answer

            print()
            print(f"[СЛУХ] Распознано: {answer}")
            print()

            return {
                "status": "PASS",
                "command": "ЖДАТЬ_ОТВЕТ",
                "answer": answer,
            }

        except Exception as e:
            print()
            print(f"[СЛУХ] ОШИБКА: {e}")
            print()

            return {
                "status": "FAIL",
                "message": str(e),
            }

    def _compare(self, expected):
        if self.last_answer is None:
            return {
                "status": "FAIL",
                "message": "Ответ отсутствует",
            }

        expected_text = str(expected).strip().lower()
        answer_text = str(self.last_answer).strip().lower()

        if expected_text in answer_text:
            conclusion = "он здесь"

            return {
                "status": "PASS",
                "command": "СРАВНИТЬ",
                "expected": expected,
                "answer": self.last_answer,
                "match": True,
                "conclusion": conclusion,
            }

        return {
            "status": "PASS",
            "command": "СРАВНИТЬ",
            "expected": expected,
            "answer": self.last_answer,
            "match": False,
            "conclusion": "ответ не соответствует ожидаемому",
        }

    def _save_experience(self):
        experience = {
            "type": "EXPERIENCE",
            "need": "найти Владимира",
            "answer": self.last_answer,
            "result": self.last_result,
            "time": datetime.now().isoformat(timespec="seconds"),
        }

        if self.learning is None:
            return {
                "status": "FAIL",
                "message": "Модуль ОБУЧЕНИЕ не подключён",
            }

        try:
            result = self.learning.handle(experience)

            if isinstance(result, dict):
                if result.get("status") == "FAIL":
                    return result

            return {
                "status": "PASS",
                "command": "ЗАПИСАТЬ_ОПЫТ",
                "experience": experience,
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def _wait(self, seconds):
        try:
            seconds = float(seconds)
        except Exception:
            return {
                "status": "FAIL",
                "message": "Неверное время ожидания",
            }

        if seconds < 0:
            return {
                "status": "FAIL",
                "message": "Время ожидания не может быть отрицательным",
            }

        print(f"Информация считается актуальной ещё {seconds:g} сек.")
        time.sleep(seconds)

        return {
            "status": "PASS",
            "command": "ЖДАТЬ",
            "seconds": seconds,
            "message": "Информация устарела. Требуется обновление.",
        }

    def _parse_command(self, line):
        if not line:
            return None, None

        line = str(line).strip()

        if not line:
            return None, None

        parts = line.split(" ", 1)

        command = parts[0].strip()

        argument = None

        if len(parts) > 1:
            argument = self._extract_argument(parts[1].strip())

        return command, argument

    def _extract_argument(self, argument):
        if argument is None:
            return None

        argument = str(argument).strip()

        if len(argument) >= 2:
            if argument.startswith('"') and argument.endswith('"'):
                return argument[1:-1]

        return argument

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
                "response": "PONG",
            }

        if msg_type == "RUN_TEMPLATE":
            return self.run_template()

        if msg_type == "RUN":
            cycles = message.get("cycles", 2)

            if cycles is None:
                return self.run(None)

            try:
                cycles = int(cycles)
            except Exception:
                return {
                    "status": "FAIL",
                    "message": "Количество циклов должно быть числом",
                }

            if cycles <= 0:
                return {
                    "status": "FAIL",
                    "message": "Количество циклов должно быть больше нуля",
                }

            return self.run(cycles)

        if msg_type == "COMMAND":
            command = message.get("command")
            argument = message.get("argument")

            if command == "СТОП":
                return self.execute("СТОП")

            return self.execute(command, argument)

        if msg_type == "STOP":
            return self.execute("СТОП")

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "state": self.state,
                "cycle_count": self.cycle_count,
                "command_count": self.command_count,
                "last_command": self.last_command,
                "last_answer": self.last_answer,
                "last_result": self.last_result,
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        self.stop_requested = True
        self.state = "STOPPED"

        return {
            "status": "PASS",
            "message": "Интерпретатор остановлен",
        }


def create_module(
    scenario=None,
    voice=None,
    speech_to_text=None,
    learning=None,
):
    return ScenarioInterpreter(
        scenario=scenario,
        voice=voice,
        speech_to_text=speech_to_text,
        learning=learning,
    )


def main():
    print()
    print("=== АЭЛИН: ИНТЕРПРЕТАТОР СЦЕНАРИЯ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")

    module = ScenarioInterpreter()

    result = module.self_test()

    print(f"Самотест: {result['status']}")


if __name__ == "__main__":
    main()