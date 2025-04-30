# LunchHuntApp

The `LunchHuntApp` class initializes and manages the LunchHunt application, which is a web-based tool for configuring and scheduling lunch notifications from various mensas.

## Constructor (__init__ method)

The `__init__` method initializes the LunchHunt application with specified settings and configurations.

### Parameters

- `settings_dir` (str, optional): Directory path where settings files are stored; defaults to `"settings"` if not provided.
- `mensa_dict` (dict, optional): Dictionary containing mensa data; defaults to a predefined dictionary if not provided.
- `default_settings` (dict, optional): Dictionary containing default application settings; defaults to a predefined dictionary if not provided.

### Returns

- `None`

## Methods

---

### Public Methods

#### run

Runs the application with the specified configuration.

##### Parameters

- `debug` (bool, optional): A boolean indicating whether to run the application in debug mode; defaults to `False`.
- `host` (str, optional): A string representing the host address to bind the application to; defaults to `'127.0.0.1'`.
- `port` (int, optional): An integer representing the port number to bind the application to; defaults to `8050`.

##### Returns

- `None`

---

### Hidden/Protected Methods

#### _default_settings_dict

Return a dictionary containing the default settings for the LunchHunt application.

##### Parameters

- None

##### Returns

- A dictionary with default settings for scraping, scheduling, Gotify notifications, and settings file configuration.

#### __setup_layout

Set up the layout of the Dash application.

##### Parameters

- None

##### Returns

- `None`

#### __load_profiles_section

Create the HTML section for loading profiles.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for loading profiles.

#### __favorite_foods_section

Create the HTML section for entering favorite foods.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for entering favorite foods.

#### __menu_categories_section

Create the HTML section for selecting menu categories and setting the pick-up offset.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for selecting menu categories and setting the pick-up offset.

#### __mensen_dropdown_section

Create the HTML section for selecting mensas.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for selecting mensas.

#### __timer_settings_section

Create the HTML section for setting timer preferences.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for setting timer preferences, including hour, minute, and alarm days.

#### __gotify_settings_section

Create the HTML section for configuring Gotify settings.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for configuring Gotify settings, including server URL, token, priority, and secure connection.

#### __save_settings_section

Create the HTML section for saving settings.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for saving settings, including the settings file name and a save button.

#### __delete_profiles_section

Create the HTML section for deleting profiles.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for deleting profiles, including a dropdown to select profiles and a delete button.

#### __delete_cronjobs_section

Create the HTML section for deleting cron jobs.

##### Parameters

- None

##### Returns

- A Dash `html.Div` containing the layout for deleting cron jobs, including a dropdown to select cron jobs and a delete button.

#### __headline_H2_style

Return the style dictionary for H2 headlines.

##### Parameters

- None

##### Returns

- A dictionary containing the style properties for H2 headlines.

#### __label_style

Return the style dictionary for labels.

##### Parameters

- None

##### Returns

- A dictionary containing the style properties for labels.

#### __dropdown_style

Return the style dictionary for dropdowns.

##### Parameters

- None

##### Returns

- A dictionary containing the style properties for dropdowns.

#### __input_style

Return the style dictionary for input fields.

##### Parameters

- None

##### Returns

- A dictionary containing the style properties for input fields.

#### __button_style

Return the style dictionary for buttons.

##### Parameters

- `color` (str): The background color of the button.

##### Returns

- A dictionary containing the style properties for buttons.

#### __section_style

Return the style dictionary for sections.

##### Parameters

- None

##### Returns

- A dictionary containing the style properties for sections.

#### __setup_callbacks

Sets up the callback for saving settings in the application.

This method defines a callback function that triggers when the "save-settings" button is clicked. It collects various settings from the UI components.

##### Parameters

- None

##### Returns

- `None`

---

##### Callback Functions

###### __save_settings

Saves the provided settings to a JSON file and creates a cron job based on the schedule settings.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the save button has been clicked.
- `favorite_foods` (list[str]): A list of strings representing the user's favorite foods.
- `menu_categories` (list[str]): A list of strings representing the menu categories to scrape.
- `offset` (int): An integer representing the offset for the schedule.
- `mensen` (list[str]): A list of strings representing the mensen to scrape.
- `hour` (int): An integer representing the hour for the schedule.
- `minute` (int): An integer representing the minute for the schedule.
- `alarm_days` (list[str]): A list of strings representing the days for the alarm.
- `server_url` (str): A string representing the server URL for Gotify.
- `token` (str): A string representing the token for Gotify.
- `priority` (int): An integer representing the priority for Gotify notifications.
- `secure` (bool): A boolean indicating whether the connection to Gotify should be secure.
- `settings_file` (str): A string representing the name of the file to save the settings to.

##### Returns

- A string message indicating the file path where the settings were saved, or an empty string if no save was performed.

###### __delete_profiles

Deletes the specified profiles from the settings directory.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the delete button has been clicked.
- `selected_profiles` (list[str]): A list of strings representing the names of the profiles to be deleted.

##### Returns

- A string message indicating the result of the deletion operation, or an empty string if no deletion was performed.

###### __delete_selected_cronjobs

Deletes the specified cron jobs for the user 'lunchhunt'.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the delete button has been clicked.
- `selected_jobs` (list[str]): A list of strings representing the full cron job strings to be deleted.

##### Returns

- A string message indicating the result of the deletion operation, or an empty string if no deletion was performed.

###### __load_settings

Loads settings from a specified profile file and updates the default settings.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the load button has been clicked.
- `profile` (str): A string representing the name of the profile file to load.

##### Returns

- A tuple containing the updated settings values followed by a success message, or a tuple with default values and an error message if loading fails.

###### __update_profiles_dropdown_options

Updates the dropdown options for profiles based on existing profile files.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the update button has been clicked.

##### Returns

- A tuple containing two lists of dictionaries, each representing the dropdown options for profiles.

###### __update_cronjobs_dropdown_options

Updates the dropdown options for cron jobs based on existing cron jobs.

##### Parameters

- `n_clicks` (int): An integer representing the number of times the update button has been clicked.

##### Returns

- A list of dictionaries, each representing a dropdown option for cron jobs.

#### __update_alarm_days

Updates the alarm days dictionary based on the provided list of days.

##### Parameters

- `alarm_days` (list): A list of strings representing the days for which the alarm should be set.

##### Returns

- A dictionary where each key is a day from the list and the value is `True`.

#### __get_existing_cronjobs

Retrieves a list of existing cron jobs for the user 'lunchhunt'.

##### Parameters

- None

##### Returns

- A list of tuples, each containing the name and full cron job string of an existing cron job.

#### __modify_mensa_name

Generates a list of tuples containing formatted mensa information.

##### Parameters

- None

##### Returns

- A list of tuples, each containing the mensa code, city name in title case, and mensa name in title case with hyphens replaced by spaces.
