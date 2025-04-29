from lunchhunt.utils import create_cronjob

from dash import Dash, dcc, html, no_update, Input, Output, State

from typing import  List, Dict, Tuple, Any
import json
import os


class LunchHuntApp:
    def __init__(
            self,
            settings_dir: str | None = None,
            mensa_dict: Dict | None = None,
            default_settings: Dict | None = None,
    ):
        self.settings_dir = settings_dir or "settings"
        self.file_type = ".json"

        self.default_settings = default_settings or self._default_settings_dict()
        self.mensa_dict = mensa_dict or self._default_mensa_dict()

        self.app = Dash(
            __name__,
            assets_folder='/home/lunchhunt/app/assets/'
        )
        self.setup_layout()
        self.setup_callbacks()

    @staticmethod
    def _default_settings_dict() -> Dict[str, Any]:
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

    @staticmethod
    def _default_mensa_dict() -> Dict[str, Tuple[str, str]]:
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
            "MWH": ("nordhausen", "mensa-weinberghof")
        }

    def setup_layout(self) -> None:
        self.app.layout = html.Div([
            html.Div([
                html.H1(
                    "LunchHunt",
                    style={
                        "margin": "20px",
                        "color": "#fff",
                        "text-align": "center"
                    }),
                self.load_profiles_section(),
                self.favorite_foods_section(),
                self.menu_categories_section(),
                self.mensen_dropdown_section(),
                self.timer_settings_section(),
                self.gotify_settings_section(),
                self.save_settings_section(),
                self.delete_profiles_section(),
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

    def load_profiles_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Load Profiles",
                style=self.headline_H2_style()),
            dcc.Dropdown(
                id="load-profiles-dropdown",
                options=[],
                placeholder="Select a profile to load",
                style=self.dropdown_style()),
            html.Button(
                "Load Profile",
                id="load-profiles-button",
                n_clicks=0,
                style=self.button_style("#007BFF")),
            html.Div(
                id="load-output",
                style={
                    "margin": "10px auto",
                    "text-align": "center",
                    "color": "#fff"
                })], style=self.section_style())

    def favorite_foods_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Favorite Foods",
                style=self.headline_H2_style()),
            dcc.Input(
                id="favorite-foods",
                type="text",
                value=self.default_settings.get("favorite_food", None),
                placeholder="Enter favorite foods and separate by ';'",
                style=self.input_style())],
            style=self.section_style())

    def menu_categories_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Menu Categories",
                style=self.headline_H2_style()),
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
                style=self.dropdown_style()),
            html.Label(
                "Pick-up Offset: ",
                title="This is the minimum amount of time before closing time"
                      " at which notifications are sent."
                      "\nWarm breakfast: 8:00-10:00"
                      "\nLunch service: 11:00-14:00"
                      "\nSnack in between: 15:00-16:30"
                      "\nDinner canteen 17:30-19:30",
                style=self.label_style()),
            dcc.Input(
                id="offset-input",
                type="number",
                min=10, max=240, step=10,
                value=self.default_settings.get("offset", 30),
                style=self.input_style())],
            style=self.section_style())

    def mensen_dropdown_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Mensen",
                style=self.headline_H2_style()),
            dcc.Dropdown(
                id="mensen-dropdown",
                options=[
                    {'label': f"{city} - {name}", 'value': code}
                    for code, city, name in self.modify_mensa_name()
                ],
                value=self.default_settings.get("mensa", "EAP"),
                multi=True,
                style=self.dropdown_style())],
            style=self.section_style())

    def timer_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Timer",
                style=self.headline_H2_style()),
        html.Div([
            html.Label(
                "Hour (24h): ",
                style=self.label_style()),
            dcc.Input(
                id="hour-input",
                type="number",
                min=0, max=24, step=1,
                value=self.default_settings.get("hour", 9),
                style=self.input_style())]),
        html.Div([
            html.Label(
                "Minute: ",
                style=self.label_style()),
            dcc.Input(
                id="minute-input",
                type="number",
                min=0, max=59, step=1,
                value=self.default_settings.get("minute", 0),
                style=self.input_style())]),
        html.Div([
            html.Label(
                "Alarm Days: ",
                style=self.label_style()),
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
            style=self.section_style())

    def gotify_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Gotify",
                style=self.headline_H2_style()),
            html.Div([
                html.Label(
                    "Server: ",
                    style=self.label_style()),
            dcc.Input(
                id="server-url",
                type="text",
                value=self.default_settings.get("server_url", None),
                placeholder="Enter server URL",
                style=self.input_style())]),
            html.Div([
                html.Label(
                    "Token: ",
                    style=self.label_style()),
            dcc.Input(
                id="token",
                type="text",
                value=self.default_settings.get("token", None),
                placeholder="Enter token",
                style=self.input_style())]),
            html.Div([
                html.Label(
                    "Priority (0-10): ",
                    style=self.label_style()),
            dcc.Input(
                id="priority-input",
                type="number",
                min=0, max=10, step=1,
                value=self.default_settings.get("priority", 5),
                style=self.input_style())]),
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
            style=self.section_style())

    def save_settings_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Save",
                style=self.headline_H2_style()),
            dcc.Input(
                id="settings-file",
                type="text",
                value=os.path.splitext(self.default_settings.get(
                    "settings_file", "settings.json"))[0],
                placeholder="Enter settings file name",
                style=self.input_style()),
            html.Button(
                "Save Settings",
                id="save-settings",
                n_clicks=0,
                style=self.button_style("#007BFF"))],
            style=self.section_style())

    def delete_profiles_section(self) -> html.Div:
        return html.Div([
            html.H2(
                "Delete Profiles",
                style=self.headline_H2_style()),
            dcc.Dropdown(
                id="delete-profiles-dropdown",
                options=[
                    {"label": profile, "value": profile}
                    for profile in self.get_existing_profiles()],
                multi=True,
                placeholder="Select profiles to delete",
                style=self.dropdown_style()),
            html.Button(
                "Delete Selected Profiles",
                id="delete-profiles-button",
                n_clicks=0,
                style=self.button_style("#FF4136")),
            html.Div(
                id="delete-output",
                style={
                    "margin": "10px auto",
                    "text-align": "center",
                    "color": "#fff"
                })],
            style=self.section_style())

    @staticmethod
    def headline_H2_style() -> Dict[str, str]:
        return {"margin": "10px 0", "color": "#fff"}

    @staticmethod
    def label_style() -> Dict[str, str]:
        return {
            "marginRight": "10px",
            "marginTop": "5px",
            "marginBottom": "5px",
            "display": "block",
            "color": "#fff"
        }

    @staticmethod
    def dropdown_style() -> Dict[str, str]:
        return {
            "width": "100%",
            "padding": "10px",
            "borderRadius": "5px",
            "border": "1px solid #555",
            "backgroundColor": "#444",
            "color": "#fff"
        }

    @staticmethod
    def input_style() -> Dict[str, str]:
        return {
            "width": "100%",
            "padding": "5px",
            "borderRadius": "5px",
            "border": "1px solid #555",
            "backgroundColor": "#444",
            "color": "#fff"
        }

    @staticmethod
    def button_style(color: str) -> Dict[str, str]:
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
    def section_style() -> Dict[str, str]:
        return {
            "border": "1px solid #555",
            "padding": "20px",
            "borderRadius": "5px",
            "margin": "20px auto",
            "width": "80%",
            "maxWidth": "600px",
            "backgroundColor": "#333"
        }

    def setup_callbacks(self):
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
        def save_settings(
                n_clicks: int,
                favorite_foods: List[str],
                menu_categories: List[str],
                offset: int,
                mensen: List[str],
                hour: int,
                minute: int,
                alarm_days: List[str],
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
                        "alarm_days": self.update_alarm_days(alarm_days),
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
        def delete_profiles(
                n_clicks: int,
                selected_profiles: List[str]
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
                        return f"Error deleting '{profile}': {str(e)}"
                return f"Successfully deleted {len(selected_profiles)} profile(s)."
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
        def load_settings(
                n_clicks: int,
                profile: str
        ):

            if n_clicks > 0 and profile:
                filepath = os.path.join(self.settings_dir, profile)
                try:
                    with open(filepath, 'r') as file:
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
                                self.update_alarm_days(
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
                            loaded_settings.get(
                                "settings_file",
                                self.default_settings.get("settings_file")
                            )
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
        def update_profiles_dropdown_options(
                n_clicks: int
        ) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:

            profiles = self.get_existing_profiles()
            options = [
                {"label": item.split('.')[0], "value": item}
                for item in profiles
            ]
            return options, options

    @staticmethod
    def update_alarm_days(alarm_days) -> Dict[str, str]:
        return {day: True for day in alarm_days} if alarm_days else {}

    def get_existing_profiles(self) -> List[str]:

        if not os.path.exists(self.settings_dir):
            return []

        return [
            file for file in os.listdir(self.settings_dir)
            if file.endswith(self.file_type)
        ]

    def modify_mensa_name(self) -> List[Tuple[str, str, str]]:
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
