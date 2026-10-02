# C:\01 Ai\04_prediction.py
# Аэлин — ПРОГНОЗ
# Версия 0.1

from __future__ import annotations

from datetime import datetime


MODULE_NAME = "04_prediction"
VERSION = "0.1"


class Prediction:
    """Модуль прогнозирования следующего состояния Аэлин."""

    def __init__(self):
        self.created = datetime.now().isoformat(timespec="seconds")
        self.last_prediction = None
        self.predictions = []

    def module_info(self):
        return {
            "name": "ПРОГНОЗ",
            "version": VERSION,
            "module": MODULE_NAME,
            "description": "Формирование возможных следующих состояний и событий",
        }

    def self_test(self):
        try:
            if not isinstance(self.predictions, list):
                return {
                    "status": "FAIL",
                    "message": "Хранилище прогнозов недоступно",
                }

            test_result = self.predict(
                {
                    "current_state": "test",
                    "context": "connection",
                }
            )

            if test_result is None:
                return {
                    "status": "FAIL",
                    "message": "Прогноз не сформирован",
                }

            return {
                "status": "PASS",
                "message": "Модуль прогноза работает",
            }

        except Exception as e:
            return {
                "status": "FAIL",
                "message": str(e),
            }

    def predict(self, context):
        """
        Формирует базовый прогноз.

        На первом этапе это рабочий каркас.
        Сложная модель прогнозирования будет добавлена позже.
        """

        if not isinstance(context, dict):
            return None

        prediction = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "context": context,
            "prediction": "ожидание следующего события",
        }

        self.last_prediction = prediction
        self.predictions.append(prediction)

        return prediction

    def get_last_prediction(self):
        return self.last_prediction

    def get_predictions(self, limit=20):
        return self.predictions[-limit:]

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

        if msg_type == "PREDICT":
            context = message.get("context", {})

            result = self.predict(context)

            if result is None:
                return {
                    "status": "FAIL",
                    "message": "Не удалось сформировать прогноз",
                }

            return {
                "status": "PASS",
                "prediction": result,
            }

        if msg_type == "STATE":
            return {
                "status": "PASS",
                "last_prediction": self.last_prediction,
                "predictions_count": len(self.predictions),
            }

        return {
            "status": "FAIL",
            "message": f"Неизвестный тип сообщения: {msg_type}",
        }

    def shutdown(self):
        return {
            "status": "PASS",
            "message": "Модуль ПРОГНОЗ завершён",
        }


def create_module():
    return Prediction()


def main():
    print()
    print("=== АЭЛИН: ПРОГНОЗ ===")
    print(f"Модуль: {MODULE_NAME}")
    print(f"Версия: {VERSION}")
    print("Статус: ЗАПУЩЕН")

    module = Prediction()
    result = module.self_test()

    print(f"Самотест: {result['status']}")

    if result["status"] == "PASS":
        print("Состояние: READY")
        print("Модуль прогнозирования готов к работе.")
    else:
        print("Состояние: ERROR")
        print(result.get("message", ""))


if __name__ == "__main__":
    main()