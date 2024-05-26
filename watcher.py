import os
import sys
import threading
import time

from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from converter import pdfs_to_single_png
from db_functions import add_event_to_database_table, delete_events_from_database_table, initialise_database, write_logs_to_text
from settings import settings_dict

if __name__ == "__main__":
    patterns = ["*.pdf"]
    ignore_patterns = None
    ignore_directories = None
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    sleep_timer = settings_dict["Event Pause"]
    if sleep_timer < 1:
        sleep_timer = 1

    initialise_database()
    delete_events_from_database_table(settings_dict["Delete Date"], "logs")

def on_created(event):
    try:
        abs_path = str(Path(__file__).parent / event.src_path)
        output_file = f"{abs_path[:abs_path.rfind(".")]}.png"
        
        version_counter = 1
        while (os.path.exists(output_file)):
            output_file = f"{output_file[:output_file.rfind(".")]}-{version_counter}.png"
            version_counter += 1

        pdfs_to_single_png(pdf_path=abs_path, output_path=output_file)

        if settings_dict["Delete Source"]:
            if os.path.isfile(output_file):
                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                    if settings_dict["Log Deletes"]:
                        add_event_to_database_table(f"{datetime.today()}", "Delete", f"Delete source pdf: {abs_path}", "logs")
                
    except Exception as err:
        print(f"Watcher error: {err}")
        if settings_dict["Log Errors"]:
            add_event_to_database_table(f"{datetime.today()}", "Error", f"Failed to Convert {event.src_path} - Error: {err}", "logs")

def on_deleted(event):
    try:
        if settings_dict["Log Deletes"]:
            print(f"{event.src_path} has been deleted.")
    except Exception as e:
        print(f"Monitor delete event error: {e}")

def on_modified(event):
    try:
        if settings_dict["Log Modifies"]:
            print(f"{event.src_path} has been modified.")
            add_event_to_database_table(f"{datetime.today()}", "Modify", f"{event.src_path} has been modified.", "logs")
    except Exception as e:
        print(f"Monitor modify event error: {e}")

def on_moved(event):
    try:
        if settings_dict["Log Moves"]:
            print(f"{event.src_path} has been moved to {event.dest_path}.")
            add_event_to_database_table(f"{datetime.today()}", "Modify", f"{event.src_path} has been moved to {event.dest_path}.", "logs")
    except Exception as e:
        print(f"Monitor move event error: {e}")

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = fr"{settings_dict["Monitor Path"]}"

# Modify relative path if .exe
if path == ".":
    if getattr(sys, "frozen", False):
        path = fr"{os.path.dirname(sys.executable)}"
    elif __file__:
        path = fr"{os.path.dirname(__file__)}"

def periodic_log_writer(interval):
    while True:
        time.sleep(interval)
        write_logs_to_text("logs")
        print(f"{datetime.today()} - Synced database to logs.txt")

startup_message = f"""
    PDF to PNG Converter v1.5
    -------------------------
    Monitoring {path} for pdfs
    Interval between pdf conversions: {sleep_timer} seconds
    Delete source .pdf files is {"ON" if settings_dict["Delete Source"] else "OFF"}
"""

print(startup_message)

go_recursively = False # Whether to convert and potentially DELETE pdfs in child directories
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()

if settings_dict["Text Logs"]:
    write_logs_to_text("logs")
    print(f"Created log text file, toggle this in config.ini")
    log_writer_interval = settings_dict["Log Interval"]
    log_writer_thread = threading.Thread(target=periodic_log_writer, args=(log_writer_interval,))
    log_writer_thread.daemon = True
    log_writer_thread.start()

try:
    while True:
        time.sleep(sleep_timer)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()