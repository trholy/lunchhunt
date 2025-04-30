import json
import logging
import os
import re
import subprocess
from typing import Any

from dash import Dash, Input, Output, State, dcc, html, no_update

from lunchhunt.utils import create_cronjob, default_mensa_dict


class LunchHuntApp:
    def __init__(
            self,
            settings_dir: str | None = None,
            mensa_dict: dict | None = None,
            default_settings: dict | None = None,
    ):
        self.settings_dir = settings_dir or "settings"
        self.file_type = ".json"

        self.default_settings = default_settings or self._default_settings_dict()
        self.mensa_dict = mensa_dict or default_mensa_dict()

        self.app = Dash(
            __name__,
            assets_folder='/home/lunchhunt/app/assets/'
        )
        self.__setup_layout()
        self.__setup_callbacks()

    @staticmethod
    def _default_settings_dict() -> dict[str, Any]:
        return {
            # Scraper Settings
            "favorite_food": None,
            "menu_category": "Mittagessen",
            "offset": 30,
            "mensa": "EAP",
            # Schedule Settings
            "hour": 9,
            "minute": 0,
            "alarm_days": [
                'monday', 'tuesday', 'wednesday', 'thursday', 'friday'
            ],
            # Gotify Settings
            "server_url": None,
            "token": None,
            "priority": 5,
            "secure": False,
            # Settings File
            "settings_file": "settings.json"
        }

    def __setup_layout(self) -> None:
        self.app.layout = html.Div([
            html.Div([
                html.H1(
                    "LunchHunt",
                    style={
                        "margin": "20px",
                        "color": "#fff",
                        "text-align": "center"
                    }),
                self.__load_profiles_section(),
                self.__favorite_foods_section(),
                self.__menu_categories_section(),
                self.__mensen_dropdown_section(),
                self.__timer_settings_section(),
                self.__gotify_settings_section(),
                self.__save_settings_section(),
                self.__delete_profiles_section(),
                self.__delete_cronjobs_section(),
                html.Div(
                    id="save-output",
                    style={
                        "margin": "10px auto",
                        "text-align": "center",
                        "color": "#fff"
                    })],
                style={
                    "maxWidth": "1200px",
                    "margin": "0 auto",
                    "padding": "20px",
                    "backgroundColor": "#222",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                })])

    def __load_profiles_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Load Profiles",
                style=self.__headline_H2_style()),
            dcc.Dropdown(
                id="load-profiles-dropdown",
                options=[],
                placeholder="Select a profile to load",
                style=self.__dropdown_style()),
            html.Button(
                "Load Profile",
                id="load-profiles-button",
                n_clicks=0,
                style=self.__button_style("#007BFF")),
            html.Div(
                id="load-output",
                style={
                    "margin": "10px auto",
                    "text-align": "center",
                    "color": "#fff"
                })], style=self.__section_style())

    def __favorite_foods_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Favorite Foods",
                style=self.__headline_H2_style()),
            dcc.Input(
                id="favorite-foods",
                type="text",
                value=self.default_settings.get("favorite_food", None),
                placeholder="Enter favorite foods and separate by ';'",
                style=self.__input_style())],
            style=self.__section_style())

    def __menu_categories_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Menu Categories",
                style=self.__headline_H2_style()),
            dcc.Dropdown(
                id="menu-categories-dropdown",
                options=[
                    {'label': 'Frühstück', 'value': 'Frühstück'},
                    {'label': 'Mittagessen', 'value': 'Mittagessen'},
                    {'label': 'Zwischenversorgung', 'value': 'Zwischenversorgung'},
                    {'label': 'Abendessen', 'value': 'Abendessen'}
                ],
                value=self.default_settings.get("menu_category", "Mittagessen"),
                multi=True,
                style=self.__dropdown_style()),
            html.Label(
                "Pick-up Offset: ",
                title="This is the minimum amount of time before closing time"
                      " at which notifications are sent."
                      "\nWarm breakfast: 8:00-10:00"
                      "\nLunch service: 11:00-14:00"
                      "\nSnack in between: 15:00-16:30"
                      "\nDinner canteen 17:30-19:30",
                style=self.__label_style()),
            dcc.Input(
                id="offset-input",
                type="number",
                min=10, max=240, step=10,
                value=self.default_settings.get("offset", 30),
                style=self.__input_style())],
            style=self.__section_style())

    def __mensen_dropdown_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Mensen",
                style=self.__headline_H2_style()),
            dcc.Dropdown(
                id="mensen-dropdown",
                options=[
                    {'label': f"{city} - {name}", 'value': code}
                    for code, city, name in self.__modify_mensa_name()
                ],
                value=self.default_settings.get("mensa", "EAP"),
                multi=True,
                style=self.__dropdown_style())],
            style=self.__section_style())

    def __timer_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Timer",
                style=self.__headline_H2_style()),
        html.Div([
            html.Label(
                "Hour (24h): ",
                style=self.__label_style()),
            dcc.Input(
                id="hour-input",
                type="number",
                min=0, max=24, step=1,
                value=self.default_settings.get("hour", 9),
                style=self.__input_style())]),
        html.Div([
            html.Label(
                "Minute: ",
                style=self.__label_style()),
            dcc.Input(
                id="minute-input",
                type="number",
                min=0, max=59, step=1,
                value=self.default_settings.get("minute", 0),
                style=self.__input_style())]),
        html.Div([
            html.Label(
                "Alarm Days: ",
                style=self.__label_style()),
            dcc.Checklist(
                id="day-checkbox",
                options=[
                    {'label': 'Monday', 'value': "monday"},
                    {'label': 'Tuesday', 'value': "tuesday"},
                    {'label': 'Wednesday', 'value': "wednesday"},
                    {'label': 'Thursday', 'value': "thursday"},
                    {'label': 'Friday', 'value': "friday"},
                ],
                value=self.default_settings.get(
                    "alarm_days", [
                        'monday', 'tuesday', 'wednesday', 'thursday', 'friday'
                    ]),
                inline=True,
                inputStyle={"marginRight": "5px", "marginTop": "10px"})])],
            style=self.__section_style())

    def __gotify_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Gotify",
                style=self.__headline_H2_style()),
            html.Div([
                html.Label(
                    "Server: ",
                    style=self.__label_style()),
            dcc.Input(
                id="server-url",
                type="text",
                value=self.default_settings.get("server_url", None),
                placeholder="Enter server URL",
                style=self.__input_style())]),
            html.Div([
                html.Label(
                    "Token: ",
                    style=self.__label_style()),
            dcc.Input(
                id="token",
                type="text",
                value=self.default_settings.get("token", None),
                placeholder="Enter token",
                style=self.__input_style())]),
            html.Div([
                html.Label(
                    "Priority (0-10): ",
                    style=self.__label_style()),
            dcc.Input(
                id="priority-input",
                type="number",
                min=0, max=10, step=1,
                value=self.default_settings.get("priority", 5),
                style=self.__input_style())]),
        dcc.RadioItems(
            id="secure-switch",
            options=[
                {"label": "HTTP", "value": False},
                {"label": "HTTPS", "value": True}
            ],
            value=self.default_settings.get("secure", False),
            inline=True,
            style={
                "display": "flex",
                "alignItems": "center",
                "color": "#fff"
            }),
        html.Div(id="switch-output",
                 style={
                     "margin": "10px auto",
                     "text-align": "center", "color": "#fff"
                 })],
            style=self.__section_style())

    def __save_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Save",
                style=self.__headline_H2_style()),
            dcc.Input(
                id="settings-file",
                type="text",
                value=os.path.splitext(self.default_settings.get(
                    "settings_file", "settings.json"))[0],
                placeholder="Enter settings file name",
                style=self.__input_style()),
            html.Button(
                "Save Settings",
                id="save-settings",
                n_clicks=0,
                style=self.__button_style("#007BFF"))],
            style=self.__section_style())

    def __delete_profiles_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Delete Profiles",
                style=self.__headline_H2_style()),
            dcc.Dropdown(
                id="delete-profiles-dropdown",
                options=[
                    {"label": profile, "value": profile}
                    for profile in self.get_existing_profiles()],
                multi=True,
                placeholder="Select profiles to delete",
                style=self.__dropdown_style()),
            html.Button(
                "Delete Selected Profiles",
                id="delete-profiles-button",
                n_clicks=0,
                style=self.__button_style("#FF4136")),
            html.Div(
                id="delete-output",
                style={
                    "margin": "10px auto",
                    "text-align": "center",
                    "color": "#fff"
                })],
            style=self.__section_style())

    def __delete_cronjobs_section(self) -> html.Div:
        return html.Div([
            html.H2("Delete Cron Jobs", style=self.__headline_H2_style()),
            dcc.Dropdown(
                id="delete-cronjobs-dropdown",
                options=[
                    {"label": job_name, "value": full_cronjob}
                    for job_name, full_cronjob in self.__get_existing_cronjobs()],
                multi=True,
                placeholder="Select cron jobs to delete",
                style=self.__dropdown_style()),
            html.Button(
                "Delete Selected Cron Jobs",
                id="delete-cronjobs-button",
                n_clicks=0,
                style=self.__button_style("#FF4136")),
            html.Div(
                id="delete-cron-output",
                style={
                    "margin": "10px auto",
                    "text-align": "center",
                    "color": "#fff"
                })],
            style=self.__section_style())

    @staticmethod
    def __headline_H2_style() -> dict[str, str]:
        return {"margin": "10px 0", "color": "#fff"}

    @staticmethod
    def __label_style() -> dict[str, str]:
        return {
            "marginRight": "10px",
            "marginTop": "5px",
            "marginBottom": "5px",
            "display": "block",
            "color": "#fff"
        }

    @staticmethod
    def __dropdown_style() -> dict[str, str]:
        return {
            "width": "100%",
            "padding": "10px",
            "borderRadius": "5px",
            "border": "1px solid #555",
            "backgroundColor": "#444",
            "color": "#fff"
        }

    @staticmethod
    def __input_style() -> dict[str, str]:
        return {
            "width": "100%",
            "padding": "5px",
            "borderRadius": "5px",
            "border": "1px solid #555",
            "backgroundColor": "#444",
            "color": "#fff"
        }

    @staticmethod
    def __button_style(color: str) -> dict[str, str]:
        return {
            "margin": "10px auto",
            "display": "block",
            "padding": "10px 20px",
            "borderRadius": "5px",
            "border": "none",
            "backgroundColor": color,
            "color": "white",
            "cursor": "pointer"
        }

    @staticmethod
    def __section_style() -> dict[str, str]:
        return {
            "border": "1px solid #555",
            "padding": "20px",
            "borderRadius": "5px",
            "margin": "20px auto",
            "width": "80%",
            "maxWidth": "600px",
            "backgroundColor": "#333"
        }

    def __setup_callbacks(self):
        @self.app.callback(
            Output("save-output", "children"),
            [Input("save-settings", "n_clicks")],
            [
                State("favorite-foods", "value"),
                State("menu-categories-dropdown", "value"),
                State("offset-input", "value"),
                State("mensen-dropdown", "value"),
                State("hour-input", "value"),
                State("minute-input", "value"),
                State("day-checkbox", "value"),
                State("server-url", "value"),
                State("token", "value"),
                State("priority-input", "value"),
                State("secure-switch", "value"),
                State("settings-file", "value")
            ]
        )
        def __save_settings(
                n_clicks: int,
                favorite_foods: list[str],
                menu_categories: list[str],
                offset: int,
                mensen: list[str],
                hour: int,
                minute: int,
                alarm_days: list[str],
                server_url: str,
                token: str,
                priority: int,
                secure: bool,
                settings_file: str
        ):

            if n_clicks > 0:
                favorite_foods = [
                    food.strip() for food in favorite_foods.split(";")
                ] if favorite_foods else []

                settings_file = settings_file + self.file_type \
                    if not settings_file.endswith('.json') else settings_file

                settings_data = {
                    "scraper_settings": {
                        "favorite_foods": favorite_foods,
                        "menu_categories": menu_categories
                        if isinstance(menu_categories, list)
                        else [menu_categories],
                        "mensen": mensen
                        if isinstance(mensen, list) else [mensen],
                    },
                    "schedule_settings": {
                        "offset": offset,
                        "hour": hour,
                        "minute": minute,
                        "alarm_days": self.__update_alarm_days(alarm_days),
                    },
                    "gotify_settings": {
                        "server_url": server_url,
                        "token": token,
                        "priority": priority,
                        "secure": secure
                    },
                    "settings_file": settings_file
                }

                # Save to a JSON file
                os.makedirs(self.settings_dir, exist_ok=True)
                filepath = os.path.join(
                    self.settings_dir, f"{settings_file}"
                )
                with open(filepath, 'w') as file:
                    json.dump(settings_data, file, indent=4)

                create_cronjob(
                    schedule_settings=settings_data['schedule_settings'],
                    settings_name=f"{settings_file}"
                )

                return f"Settings saved to {filepath}. Please reload the Page!"
            return ""

        @self.app.callback(
            Output("delete-output", "children"),
            [Input("delete-profiles-button", "n_clicks")],
            [State("delete-profiles-dropdown", "value")]
        )
        def __delete_profiles(
                n_clicks: int,
                selected_profiles: list[str]
        ) -> str:

            if n_clicks > 0 and selected_profiles:
                for profile in selected_profiles:
                    profile_path = os.path.join(self.settings_dir, profile)
                    try:
                        if os.path.exists(profile_path):
                            os.remove(profile_path)
                        else:
                            return f"Profile '{profile}' does not exist."
                    except Exception as e:
                        return f"Error deleting '{profile}': {e!s}"
                return f"Successfully deleted {len(selected_profiles)} profile(s)."
            return ""

        @self.app.callback(
            Output("delete-cron-output", "children"),
            [Input("delete-cronjobs-button", "n_clicks")],
            [State("delete-cronjobs-dropdown", "value")]
        )
        def __delete_selected_cronjobs(
                n_clicks: int,
                selected_jobs: list[str]
        ) -> str:
            if n_clicks > 0 and selected_jobs:
                try:
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

                    return f"Successfully deleted {len(selected_jobs)} cron job(s)."
                except subprocess.CalledProcessError as e:
                    return f"Error modifying crontab: {e!s}"
            return ""

        @self.app.callback(
            [
                Output("favorite-foods", "value"),
                Output("menu-categories-dropdown", "value"),
                Output("offset-input", "value"),
                Output("mensen-dropdown", "value"),
                Output("hour-input", "value"),
                Output("minute-input", "value"),
                Output("day-checkbox", "value"),
                Output("server-url", "value"),
                Output("token", "value"),
                Output("priority-input", "value"),
                Output("secure-switch", "value"),
                Output("settings-file", "value"),
                Output("load-output", "children"),
            ],
            [Input("load-profiles-button", "n_clicks")],
            [State("load-profiles-dropdown", "value")]
        )
        def __load_settings(
                n_clicks: int,
                profile: str
        ):

            if n_clicks > 0 and profile:
                filepath = os.path.join(self.settings_dir, profile)
                try:
                    with open(filepath) as file:
                        loaded_settings = json.load(file)

                    # Load sub-dictionaries
                    scraper_settings = loaded_settings.get(
                        "scraper_settings",
                        self.default_settings.get("scraper_settings")
                    )
                    schedule_settings = loaded_settings.get(
                        "schedule_settings",
                        self.default_settings.get("schedule_settings")
                    )
                    gotify_settings = loaded_settings.get(
                        "gotify_settings",
                        self.default_settings.get("gotify_settings")
                    )

                    # Update the default settings directly
                    self.default_settings.update({
                        # scraper_settings
                        "favorite_food":
                            "; ".join(scraper_settings.get(
                                "favorite_foods" or "",
                                self.default_settings.get("favorite_foods"))
                            ),
                        "menu_category":
                            scraper_settings.get(
                                "menu_categories",
                                self.default_settings.get("menu_categories")
                            ),
                        "mensa":
                            scraper_settings.get(
                                "mensen",
                                self.default_settings.get("mensen")
                            ),
                        # schedule_settings
                        "offset":
                            schedule_settings.get(
                                "offset",
                                self.default_settings.get("offset")
                            ),
                        "hour":
                            schedule_settings.get(
                                "hour",
                                self.default_settings.get("hour")
                            ),
                        "minute":
                            schedule_settings.get(
                                "minute",
                                self.default_settings.get("minute")
                            ),
                        "alarm_days": [
                            day for day, active in schedule_settings.get(
                                "alarm_days",
                                self.__update_alarm_days(
                                    self.default_settings.get("alarm_days"))
                            ).items() if active
                        ],
                        # gotify_settings
                        "server_url":
                            gotify_settings.get(
                                "server_url",
                                self.default_settings.get("server_url")
                            ),
                        "token":
                            gotify_settings.get(
                                "token",
                                self.default_settings.get("token")
                            ),
                        "priority":
                            gotify_settings.get(
                                "priority",
                                self.default_settings.get("priority")
                            ),
                        "secure":
                            gotify_settings.get(
                                "secure",
                                self.default_settings.get("secure")
                            ),
                        # settings_file
                        "settings_file":
                            os.path.splitext(loaded_settings.get(
                                "settings_file",
                                self.default_settings.get("settings_file")
                            ))[0]
                    })

                    return tuple(self.default_settings.values()) + (
                        f"Settings loaded from {profile}",
                    )
                except Exception as e:
                    return [no_update] * 12 + [f"Error loading settings: {e}"]
            return [no_update] * 12 + [no_update]

        @self.app.callback(
            [
                Output("load-profiles-dropdown", "options"),
                Output("delete-profiles-dropdown", "options")
            ],
            [Input("save-settings", "n_clicks")]
        )
        def __update_profiles_dropdown_options(
                n_clicks: int
        ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:

            profiles = self.get_existing_profiles()
            options = [
                {"label": item.split('.')[0], "value": item}
                for item in profiles
            ]
            return options, options

        @self.app.callback(
            Output("delete-cronjobs-dropdown", "options"),
            [Input("save-settings", "n_clicks")]
        )
        def __update_cronjobs_dropdown_options(
                n_clicks: int
        ) -> list[dict[str, str]]:
            cronjobs = self.__get_existing_cronjobs()

            if not cronjobs:
                return []

            return [
                {"label": job_name, "value": full_cronjob}
                for job_name, full_cronjob in cronjobs
            ]

    @staticmethod
    def __update_alarm_days(
            alarm_days: list
    ) -> dict[str, str]:
        return {day: True for day in alarm_days} if alarm_days else {}

    def get_existing_profiles(self) -> list[str]:
        if not os.path.exists(self.settings_dir):
            return []

        return [
            file for file in os.listdir(self.settings_dir)
            if file.endswith(self.file_type)
        ]

    @staticmethod
    def __get_existing_cronjobs() -> list[tuple]:
        try:
            result = subprocess.run(
                ["crontab", "-l", "-u", "lunchhunt"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return []

            lines = result.stdout.splitlines()
            cronjobs = []

            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    match = re.search(
                        r'^(\d{1,2})\s+(\d{1,2}).*?run\.py\s+([^\s]+)\.json',
                        line
                    )
                    if match:
                        minute = match.group(1)
                        hour = match.group(2)
                        settings_name = match.group(3)

                        time_str = f"{hour.zfill(2)}:{minute.zfill(2)}"
                        cronjob_name = f"{time_str} - {settings_name}"

                        cronjobs.append((cronjob_name, line))

            return cronjobs
        except Exception as e:
            logging.error("Error fetching cron jobs:", e)
            return []

    def __modify_mensa_name(self) -> list[tuple[str, str, str]]:
        return [
            (code, city.title(), name.replace("-", " ").title())
            for code, (city, name) in self.mensa_dict.items()
        ]

    def run(
            self,
            debug: bool = False,
            host: str = '127.0.0.1',
            port: int = 8050
    ) -> None:
        self.app.run(debug=debug, host=host, port=port)


def main():
    app = LunchHuntApp()
    app.run(debug=True, host='0.0.0.0', port=8050)


if __name__ == "__main__":
    main()
