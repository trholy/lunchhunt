## Util Functions documentation

## `default_mensa_dict`

Provides a default mapping of Mensa codes to locations and URL identifiers.

### Function Signature

```python
def default_mensa_dict() -> dict[str, tuple[str, str]]:
```

### Returns

- `dict[str, tuple[str, str]]`: A dictionary where keys are Mensa codes and values are tuples containing the location and URL slug.

### Example Usage

```python
mensa_dict = default_mensa_dict()
print(mensa_dict["MNS"])  # Output: ('erfurt', 'mensa-nordhaeuser-strasse')
```

## `load_settings`

Loads configuration settings for the scraper and notifier from a JSON file. Expects the JSON to contain 'scraper_settings', 'schedule_settings', and 'gotify_settings' keys.

### Function Signature

```python
def load_settings(path: str) -> Optional[tuple[dict, dict, dict]]:
```

### Parameters

- `path` (str): The file path to the JSON settings file to be loaded.

### Returns

- `Optional[tuple[dict, dict, dict]]`: A tuple containing three dictionaries (`scraper_settings`, `schedule_settings`, `gotify_settings`) if successful. Returns `None` if the file is not found, the JSON is invalid, or required keys are missing.

### Example Usage

```python
scraper_settings, schedule_settings, gotify_settings = load_settings("settings.json")
print(scraper_settings)
```

## `update_menu_categories`

Filters out menu categories based on the current time and an optional timetable. Categories whose mealtime (adjusted by an offset) has already passed are removed from the list.

### Function Signature

```python
def update_menu_categories(
        categories: list,
        timetable: Optional[dict[str, time]] = None,
        offset: Union[int, float] = 30
) -> Optional[list]:
```

### Parameters

- `categories` (list): List of category names (e.g., ['Mittagessen', 'Abendmensa']) to be evaluated.
- `timetable` (Optional[dict[str, time]]): Dictionary mapping category names to specific times (default: uses internal default timetable if None).
- `offset` (Union[int, float], optional): Number of minutes to subtract from each mealtime to define the cutoff time (default: 30 minutes).

### Returns

- `Optional[list]`: List of remaining valid categories after time filtering. Returns `None` if no categories remain.

### Example Usage

```python
categories = ['Mittagessen', 'Abendmensa']
updated_categories = update_menu_categories(categories)
print(updated_categories)
```

## `create_cronjob`

Adds a cron job to the specified user's crontab based on the provided schedule settings. The job runs a Python script at specified times and days, optionally within a conda environment.

### Function Signature

```python
def create_cronjob(
        schedule_settings: dict,
        settings_name: Optional[str] = None,
        conda_env_path: Optional[str] = None,
        log_path: Optional[str] = None,
        script_path: Optional[str] = None,
        cron_command: Optional[str] = None,
        user: Optional[str] = None
) -> None:
```

### Parameters

- `schedule_settings` (dict): Dictionary with 'hour', 'minute', and 'alarm_days' keys to configure schedule.
- `settings_name` (Optional[str]): Optional setting name passed to the script as an argument.
- `conda_env_path` (Optional[str]): Optional path to the conda Python interpreter to use.
- `log_path` (Optional[str]): Optional path for logging stdout and stderr.
- `script_path` (Optional[str]): Optional path to the Python script to execute.
- `cron_command` (Optional[str]): Optional full cron command string to override automatic construction.
- `user` (Optional[str]): Optional system username whose crontab will be modified. Defaults to current user.

### Returns

- `None`. Modifies the crontab for the specified user.

### Example Usage

```python
schedule_settings = {
    "hour": 12,
    "minute": 0,
    "alarm_days": {
        "monday": True,
        "tuesday": True,
        "wednesday": True,
        "thursday": True,
        "friday": True
    }
}
create_cronjob(schedule_settings, settings_name="default", script_path="/path/to/script.py")
```
## delete_cron_job

The `delete_cron_job` function deletes the specified cron jobs for the user 'lunchhunt'. It reads the current cron jobs for the user, filters out the jobs specified in the `selected_jobs` list, and then updates the cron jobs with the remaining entries.

### Function Signature

```python
def delete_cron_job(selected_jobs: list) -> None:
```

#### Parameters

- `selected_jobs` (list[str]): A list of strings representing the full cron job strings to be deleted.

#### Returns

- `None`: This function does not return any value.

### Example Usage

```python
# Example cron jobs to delete
jobs_to_delete = [
    "0 12 * * * /usr/bin/python3 /path/to/script.py",
    "30 11 * * * /usr/bin/python3 /path/to/another_script.py"
]

# Delete the specified cron jobs
delete_cron_job(jobs_to_delete)
```
