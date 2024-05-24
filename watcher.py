import configparser
import os
import sys
import time

from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from converter import pdfs_to_single_png

config = configparser.ConfigParser()

config.read('config.ini')

if __name__ == "__main__":
    patterns = ["*.pdf"]
    ignore_patterns = None
    ignore_directories = None
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        abs_path = str(Path(__file__).parent / event.src_path)
        output_file = f"{abs_path[:abs_path.rfind(".")]}.png"
        pdfs_to_single_png(pdf_path=abs_path, output_path=output_file)

        should_delete = config["SETTINGS"]["DELETE_SOURCE_PDF"]

        if should_delete == "True":
            if os.path.isfile(output_file):
                if os.path.isfile(abs_path):
                    os.remove(abs_path)
                log = open("logs.txt", "a")
                log.write(f'\n{datetime.today()} - Delete source pdf: {abs_path}')
    except Exception as err:
        print(f"Watcher error: {err}")
        log = open("logs.txt", "a")
        log.write(f'\n{datetime.today()} - Failed to Convert {event.src_path} - Error: {err}')

def on_deleted(event):
    print(f"{event.src_path} has been deleted.")

def on_modified(event):
    print(f"{event.src_path} has been modified.")

def on_moved(event):
    print(f"{event.src_path} has been moved to {event.dest_path}.")

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

path = str(config["PATHS"]["MONITOR_DIRECTORY"])

# Modify relative path if .exe
if path == ".":
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)

go_recursively = False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()