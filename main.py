from functions.query import ElecRoomQuery
from functions.record import CSVRecordHandler
from functions.sender import (
    EmailSender,
    PushplusSender,
    MockSender,
    WxpusherSender,
    TelegramSender,
)
from functions.utils import Config, get_logger

logger = get_logger(__name__)


def get_sender():
    sender_type = Config.get(
        "SENDER_TYPE", "mock"
    ).lower()  # Default to mock for debugging
    if sender_type == "email":
        return EmailSender()
    elif sender_type == "pushplus":
        return PushplusSender()
    elif sender_type == "wxpusher":
        return WxpusherSender()
    elif sender_type == "telegram":
        return TelegramSender()
    elif sender_type == "mock":
        return MockSender()
    else:
        raise ValueError(f"Unsupported sender type: {sender_type}")


if __name__ == "__main__":
    # Query Logic
    query = ElecRoomQuery()
    balance_data = query.query_balance()

    # Optional Record Storage
    record_enabled = (
        Config.get("ENABLE_RECORD_STORAGE", "False").lower() == "true"
    )  # Default is False
    if record_enabled:
        csv_handler = CSVRecordHandler(
            Config.get("CSV_FILE_PATH", "./data/records.csv")
        )
        if balance_data:
            csv_handler.record(balance_data)

    # Balance Monitoring and Notification
    sender = get_sender()

    # Thresholds from environment variables
    thresholds = {
        "water": int(Config.get("THRESHOLD_WATER_BALANCE", 5)),
        "electricity": int(Config.get("THRESHOLD_ELECTRICITY_BALANCE", 5)),
        "air_conditioner": int(Config.get("THRESHOLD_AIR_CONDITIONER_BALANCE", 5)),
    }

    alerts = []
    if balance_data:
        if balance_data["water_balance"] < thresholds["water"]:
            alerts.append(
                f"Water balance is below {thresholds['water']}. Current: {balance_data['water_balance']}"
            )
        if balance_data["electricity_balance"] < thresholds["electricity"]:
            alerts.append(
                f"Electricity balance is below {thresholds['electricity']}. Current: {balance_data['electricity_balance']}"
            )
        if balance_data["air_conditioner_balance"] < thresholds["air_conditioner"]:
            alerts.append(
                f"Air Conditioner balance is below {thresholds['air_conditioner']}. Current: {balance_data['air_conditioner_balance']}"
            )

    # Send notification if there are any alerts
    if alerts:
        sender.send(subject="Balance Alerts", message="\n".join(alerts))
