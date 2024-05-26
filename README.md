# pdf-to-png
Watches a chosen directory and automatically converts any pdfs to .png

Merges multiple pages into single image file.

Press `Control+C` or close the command prompt/terminal to stop the application.

Make sure config.ini is in the same location as the app.

## Settings
- Change monitored directory in config.ini
  - Enter absolute path of directory you want to monitor. "." will use the directory the app is located in.
  - Don't use quotation marks with file paths
  - Example absolute path: C:\Projects\test
  - Defaults to app location
- Change events to log
  - Logs are stored in a local sqlite database (https://sqlitebrowser.org/).
  - Set `LOGS_TO_TEXT` to True if you want logs duplicated to a logs.txt file on app launch.
  - `LOGS_MAX_AGE` is the maximum age of logs in days, default is 10 days. 
  - Create, delete, modify, and move all log .pdf events.
  - PNG logs the creation of .png files.
  - ERROR logs all errors the app encounters.
- Set interval between file conversions
  - `EVENT_PAUSE` is the pause between each conversion in seconds, default is 1 second.
  - Might make the app more stable with many files, while making the overall process significantly slower.
  - Potentially obsolete with retry attempts / delays, may be worth setting to 1 second if you don't encounter any issues.
- Set how often to sync database to logs.txt
  - `LOGS_UPDATE_INTERVAL` is the time between syncing in minutes, app will always sync on startup.
- Set maximum retry attempts when failing to convert a pdf with `RETRY_COUNTER`
- Set delay in seconds between retry attempts with `RETRY_DELAY`
