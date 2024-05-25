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

print(config["LOGS"]["LOG_CREATE"])

# Delete Source
should_delete = True if config["SETTINGS"]["DELETE_SOURCE_PDF"] == "True" else False

# Monitor Directory Location
monitor_path = str(config["PATHS"]["MONITOR_DIRECTORY"])

settings_dict = {
    "Delete Date": logs_delete_date,
    "Log Creates": log_create_events,
    "Log Deletes": log_delete_events,
    "Log Errors": log_error_events,
    "Log Modifies": log_modify_events,
    "Log Moves": log_move_events,
    "Log PNG": log_png_events,
    "Delete Source": should_delete,
    "Monitor Path": monitor_path,
    "Text Logs": text_logs
}