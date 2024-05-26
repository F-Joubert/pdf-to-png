import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read("config.ini")

# Log Settings
logs_purge_days = config["LOGS"]["LOGS_MAX_AGE"]
logs_delete_date = str(datetime.today() - timedelta(days=10))
log_create_events = True if config["LOGS"]["LOG_CREATE"] == "True" else False
log_delete_events = True if config["LOGS"]["LOG_DELETE"] == "True" else False
log_error_events = True if config["LOGS"]["LOG_ERROR"] == "True" else False
log_modify_events = True if config["LOGS"]["LOG_MODIFY"] == "True" else False
log_move_events = True if config["LOGS"]["LOG_MOVE"] == "True" else False
log_png_events = True if config["LOGS"]["LOG_PNG"] == "True" else False
text_logs = True if config["LOGS"]["LOGS_TO_TEXT"] == "True" else False

# Delete Source
should_delete = True if config["SETTINGS"]["DELETE_SOURCE_PDF"] == "True" else False

# Monitor Directory Location
monitor_path = str(config["PATHS"]["MONITOR_DIRECTORY"])

# Time between executing events
try:
    event_pause = int(config["SETTINGS"]["EVENT_PAUSE"])
except Exception as e:
    print(f"Event Pause config error: {e}\nDouble check you've used an integer value")
    event_pause = 1

try:
    logs_update_interval = float(config["LOGS"]["LOGS_UPDATE_INTERVAL"]) * 60
except Exception as e:
    print(f"Log update interval config error: {e}\nDouble check you've used a numeric value")
    logs_update_interval = 300

settings_dict = {
    "Delete Date": logs_delete_date,
    "Log Creates": log_create_events,
    "Log Deletes": log_delete_events,
    "Log Errors": log_error_events,
    "Log Modifies": log_modify_events,
    "Log Moves": log_move_events,
    "Log PNG": log_png_events,
    "Log Interval": logs_update_interval,
    "Delete Source": should_delete,
    "Event Pause": event_pause,
    "Monitor Path": monitor_path,
    "Text Logs": text_logs
}