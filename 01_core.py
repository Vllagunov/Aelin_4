"""
Аэлин — модуль 01: Ядро.

Назначение:
    Базовый познавательный модуль Аэлин.
    Принимает сообщения, формирует внутреннее состояние
    текущего взаимодействия и возвращает результат.

На этом этапе:
    - без сложного динамического вычислителя;
    - без постоянной памяти;
    - без модели мира;
    - без самостоятельного обучения.

Ядро является центральной точкой обработки сообщений.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


VERSION = "0.1"


class Core:
    def __init__(self) -> None:
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.message_count = 0
        self.last_message: dict[str, Any] | None = None
        self.state = "READY"

    # ------------------------------------------------------------------
    # ИНФОРМАЦИЯ О МОДУЛЕ
    # ------------------------------------------------------------------

    def module_info(self) -> dict[str, Any]:
        return {
            "name": "Ядро",
            "version": VERSION,
            "module": "01_core",
            "description": "Центральный модуль обработки взаимодействия Аэлин",
            "status": self.state,
        }

    # ------------------------------------------------------------------
    # САМОТЕСТ
    # ------------------------------------------------------------------

    def self_test(self) -> dict[str, Any]:
        checks = {
            "state": self.state == "READY",
            "counter": self.message_count >= 0,
            "interface": all(
                callable(getattr(self, name, None))
                for name in (
                    "module_info",
                    "self_test",
                    "handle",
                    "shutdown",
                )
            ),
        }

        passed = all(checks.values())

        return {
            "status": "PASS" if passed else "FAIL",
            "module": "01_core",
            "checks": checks,
        }

    # ------------------------------------------------------------------
    # ОБРАБОТКА СООБЩЕНИЙ
    # ------------------------------------------------------------------

    def handle(self, message: Any) -> dict[str, Any]:
        self.message_count += 1

        # Проверка связи от Monitor.
        if isinstance(message, dict):
            if (
                message.get("type") == "TEST"
                and message.get("test") == "connection"
                and message.get("payload") == "PING"
            ):
                return {
                    "status": "PASS",
                    "module": "01_core",
                    "response": "PONG",
                }

        # Нормальное сообщение.
        if isinstance(message, dict):
            self.last_message = message

            return {
                "status": "PASS",
                "module": "01_core",
                "type": "CORE_RESPONSE",
                "message_count": self.message_count,
                "received": message,
            }

        # Защита от некорректного входа.
        return {
            "status": "FAIL",
            "module": "01_core",
            "error": "Сообщение должно быть словарём",
        }

    # ------------------------------------------------------------------
    # ЗАВЕРШЕНИЕ
    # ------------------------------------------------------------------

    def shutdown(self) -> None:
        self.state = "STOPPED"


# ----------------------------------------------------------------------
# ТОЧКА СОЗДАНИЯ МОДУЛЯ
# ----------------------------------------------------------------------

def create_module() -> Core:
    return Core()