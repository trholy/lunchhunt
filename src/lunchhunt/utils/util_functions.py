import json
import logging
import subprocess
import sys
from datetime import datetime, time, timedelta
from typing import Optional, Union


def default_mensa_dict() -> dict[str, tuple[str, str]]:
    """
    Provides a default mapping of Mensa codes to locations
     and URL identifiers.

    :return: Dictionary mapping Mensa codes to (location, URL slug).
    """
    return {
        # Erfurt
        "MNS": ("erfurt", "mensa-nordhaeuser-strasse"),
        "MAS": ("erfurt", "mensa-altonaer-strasse"),
        "CH7": ("erfurt", "cafeteria-hoersaal-7"),
        "GBX": ("erfurt", "glasbox"),
        "CSL": ("erfurt", "cafeteria-schlueterstrasse"),
        "CLS": ("erfurt", "cafeteria-leipziger-strasse"),
        # Jena
        "EAP": ("jena", "mensa-ernst-abbe-platz"),
        "CZP": ("jena", "mensa-carl-zeiss-promenade"),
        "PW": ("jena", "mensa-philosophenweg"),
        "UHG": ("jena", "mensa-uni-hauptgebaeude"),
        "MVRS": ("jena", "moritz-von-rohr-strasse"),
        "CCZ": ("jena", "cafeteria-carl-zeiss-strasse-3"),
        "CZR": ("jena", "cafeteria-zur-rosen"),
        "CBIB": ("jena", "cafeteria-bibliothek"),
        # Weimar
        "MAP": ("weimar", "mensa-am-park"),
        "CAH": ("weimar", "cafeteria-am-horn"),
        "CMP": ("weimar", "cafeteria-mensa-am-park"),
        # Ilmenau
        "MEH": ("ilmenau", "mensa-ehrenberg"),
        "CME": ("ilmenau", "cafeteria-mensa-ehrenberg"),
        "CMI": ("ilmenau", "cafeteria-mini"),
        "NANO": ("ilmenau", "nanoteria"),
        "TWC": ("ilmenau", "tower-cafe"),
        "CRB": ("ilmenau", "cafeteria-roentgenbau"),
        # Schmalkalden
        "MBH": ("schmalkalden", "mensa-blechhammer"),
        "CMB": ("schmalkalden", "cafeteria-mensa-blechhammer"),
        # Gera
        "MWF": ("gera", "mensa-weg-der-freundschaft"),
        # Eisenach
        "MAW": ("eisenach", "mensa-am-wartenberg"),
        # Nordhausen
        "MWH": ("nordhausen", "mensa-weinberghof"),
    }


def load_settings(
        path: str
) -> Optional[tuple[dict, dict, dict]]:
    """
    Loads configuration settings for the scraper and notifier from a JSON file.
    Expects the JSON to contain 'scraper_settings' and 'gotify_settings' keys.

    param: path: The file path to the JSON settings file to be loaded.

    :return: A tuple containing two dictionaries (scraper_settings,
     gotify_settings) if successful. Exits the program if the file is not found,
     the JSON is invalid, or required keys are missing.
    """
    logging.info("Loading settings from %s...", path)
    try:
        with open(path, encoding='utf-8') as file:
            settings = json.load(file)

        scraper_settings = settings['scraper_settings']
        schedule_settings = settings['schedule_settings']
        gotify_settings = settings['gotify_settings']

        logging.info("Settings loaded successfully.")
        return scraper_settings, schedule_settings, gotify_settings

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.error("Failed to load settings: %s", e)
        sys.exit(1)


def update_menu_categories(
        categories: list,
        timetable: dict[str, time] | None = None,
        offset: Union[int, float] = 30
) -> Optional[list]:
    """
    Filters out menu categories based on the current time and an optional
     timetable. Categories whose mealtime (adjusted by an offset) has already
     passed are removed from the list.

    param: categories: List of category names (e.g., ['Mittagessen',
     'Abendmensa']) to be evaluated.
    param: timetable: Dictionary mapping category names to specific times
     (default: uses internal default timetable if None).
    param: offset: Number of minutes to subtract from each mealtime to define
     the cutoff time (default: 30 minutes).

    :return: List of remaining valid categories after time filtering. Returns
     None if no categories remain.
    """
    now = datetime.now()
    offset = timedelta(minutes=offset)

    # Default timetable
    timetable = timetable or {
        'Frühstück': time(10, 0),
        'Mittagessen': time(14, 0),
        'Zwischenversorgung': time(16, 30),
        'Abendmensa': time(19, 30),
    }

    updated = []
    for category in categories:
        base_datetime = datetime.combine(now, timetable.get(category, time(0, 0)))
        base_datetime = base_datetime - offset
        end_time = base_datetime.time()

        if end_time and now.time() >= end_time:
            logging.info(
                "Removing category '%s' because time %s has passed.",
                category, end_time
            )
        else:
            updated.append(category)
    return updated if updated else None


def create_cronjob(
        schedule_settings: dict,
        settings_name: Optional[str] = None,
        conda_env_path: Optional[str] = None,
        log_path: Optional[str] = None,
        script_path: Optional[str] = None,
        cron_command: Optional[str] = None,
        user: Optional[str] = None
) -> None:
    """
    Adds a cron job to the specified user's crontab based on the provided
     schedule settings. The job runs a Python script at specified times and
     days, optionally within a conda environment.

    param: schedule_settings (dict): Dictionary with 'hour', 'minute', and
     'alarm_days' keys to configure schedule.
    param: settings_name (str | None): Optional setting name passed to the
     script as an argument.
    param: conda_env_path (str | None): Optional path to the conda Python
     interpreter to use.
    param: log_path (str | None): Optional path for logging stdout and stderr.
    param: script_path (str | None): Optional path to the Python script
     to execute.
    param: cron_command (str | None): Optional full cron command string to
     override automatic construction.
    param: user (str | None): Optional system username whose crontab will be
     modified. Defaults to current user.
    :return: None. Modifies the crontab for the specified user.
    """
    hour = schedule_settings.get("hour")
    minute = schedule_settings.get("minute")
    alarm_days = schedule_settings.get("alarm_days", {})

    if hour is None or minute is None:
        raise ValueError("'hour' and 'minute' must be provided.")
    if not any(alarm_days.values()):
        raise ValueError("At least one day must be enabled.")

    DAY_TO_CRON = {
        "monday": "1", "tuesday": "2", "wednesday": "3",
        "thursday": "4", "friday": "5", "saturday": "6", "sunday": "7"
    }
    days_of_week = [
        DAY_TO_CRON[day] for day, enabled in alarm_days.items() if enabled
    ]
    cron_time = f"{minute} {hour} * * {','.join(days_of_week)}"

    script_path = script_path or "/home/lunchhunt/app/run.py"
    conda_env_path = (conda_env_path or
                      "/home/lunchhunt/miniconda/envs/lunchhunt/bin/python")
    log_path = log_path or "/home/lunchhunt/app/lunchhunt.log"
    user = user or "lunchhunt"

    cron_command = cron_command or (f"{cron_time} {conda_env_path}"
                                    f" {script_path} {settings_name or ''}"
                                    f" >> {log_path} 2>&1")

    try:
        result = subprocess.run(
            ["crontab", "-l", "-u", user],
            capture_output=True, text=True
        )
        existing_crontab = result.stdout if result.returncode == 0 else ""
        """
        if cron_command in existing_crontab:
            logging.info("Cron job already exists.")
            return
        """

        new_crontab = existing_crontab.strip() + "\n" + cron_command + "\n"
        subprocess.run(
            ["crontab", "-u", user, "-"],
            input=new_crontab, text=True, check=True
        )
        logging.info("Cron job added successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to update crontab: {e}")


def delete_cron_job(
        selected_jobs: list
) -> None:
    """
    Deletes the specified cron jobs for the user 'lunchhunt'.

    param: selected_jobs; A list of strings representing the full cron
     job strings to be deleted (list[str])
    :return: None.
    """
    result = subprocess.run(
        ["crontab", "-l", "-u", "lunchhunt"],
        capture_output=True, text=True
    )
    existing_crontab = result.stdout if result.returncode == 0 else ""

    # Filter out the jobs based on the full cron job string
    new_lines = [
        line for line in existing_crontab.splitlines()
        if line.strip() not in selected_jobs
    ]

    new_crontab = "\n".join(new_lines) + "\n"
    subprocess.run(
        ["crontab", "-u", "lunchhunt", "-"],
        input=new_crontab, text=True, check=True
    )
