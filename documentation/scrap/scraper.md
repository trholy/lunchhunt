# MensaScraper Class Documentation

The `MensaScraper` class is a web scraper designed to extract the daily menu from university canteens. It provides functionality to scrape the menu by category and search for specific dishes.

## Constructor (__init__ method)

The constructor initializes the `MensaScraper` with a base URL and Mensa mappings.

### Parameters

- `menu_categories` (Optional[Union[List[str], str]]): Categories to filter meals by (default: all). If a single string is provided, it will be converted to a list.
- `base_url` (Optional[str]): Base URL for the Mensa website. If not provided, the default URL `"https://www.stw-thueringen.de/mensen"` will be used.
- `mensa_dict` (Optional[Dict[str, Tuple[str, str]]]): Custom mapping of Mensa codes to locations and URLs. If not provided, a default mapping will be used.

### Example Usage

```python
scraper = MensaScraper(
    menu_categories=["Frühstück", "Mittagessen"],
    base_url="https://www.stw-thueringen.de/mensen",
    mensa_dict={"EAP": ("jena", "mensa-ernst-abbe-platz")}
)
```

By default, the following mapping of cafeteria codes to locations and URLs is provided, reflecting all of thuringa's cafeteria and cafeteria pages.

```python
mensa_dict = {
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
```
## Methods

### Public Methods

#### `scrape_menu_by_category(mensa: str) -> Optional[Dict[str, List[str]]]`

Scrapes the categorized menu for a given Mensa.

- **Return Type**: Optional[Dict[str, List[str]]]
- **Description**: Scrapes the categorized menu for a given Mensa and returns a dictionary of categorized dishes. If the Mensa code is unknown, a `ValueError` is raised. If the request fails, `None` is returned.
- **Parameters**:
  - `mensa` (str): Mensa code.
- **Example Usage**:

```python
dishes_by_category = scraper.scrape_menu_by_category("EAP")
```

#### `find_matches(keywords: Union[List[str], str], dishes: Optional[Union[List[str], Dict[str, List[str]]]] = None) -> Optional[Union[List[str], Dict[str, List[str]]]]`

Finds menu items that contain specified keywords.

- **Return Type**: Optional[Union[List[str], Dict[str, List[str]]]]
- **Description**: Searches for menu items that contain specified keywords and returns a list of matching dishes if input is a list, or a dictionary with matching dishes per category if input is a dict. If no matches are found, `None` is returned.
- **Parameters**:
  - `keywords` (Union[List[str], str]): Single keyword or list of keywords to search for.
  - `dishes` (Optional[Union[List[str], Dict[str, List[str]]]]): List of dishes or dictionary of categories with dish lists. Defaults to the last scraped menu.
- **Example Usage**:

```python
matches = scraper.find_matches(["Eierkuchen", "Milchreis"])
```

### Hidden/Protected Methods

#### `_default_mensa_dict() -> Dict[str, Tuple[str, str]]`

Provides a default mapping of Mensa codes to locations and URL identifiers.

- **Return Type**: Dict[str, Tuple[str, str]]
- **Description**: Returns a dictionary mapping Mensa codes to (location, URL slug).
- **Parameters**: None
- **Example Usage**:

```python
default_mensa_dict = MensaScraper._default_mensa_dict()
```

#### `_build_mensa_url(mensa: str, location: str) -> str`

Constructs the Mensa URL based on the identifier.

- **Return Type**: str
- **Description**: Constructs the Mensa URL based on the identifier and returns the constructed URL. If the Mensa code is invalid, an error message is logged, and an empty string is returned.
- **Parameters**:
  - `mensa` (str): Mensa code.
  - `location` (str): Location name.
- **Example Usage**:

```python
url = scraper._build_mensa_url("EAP", "jena")
```

#### `_get_soup(url: str) -> Optional[BeautifulSoup]`

Fetches and parses the HTML content of a given URL.

- **Return Type**: Optional[BeautifulSoup]
- **Description**: Fetches the HTML content of a given URL and returns a BeautifulSoup object. If the request fails, an error message is logged, and `None` is returned.
- **Parameters**:
  - `url` (str): Target URL.
- **Example Usage**:

```python
soup = scraper._get_soup("https://www.stw-thueringen.de/mensen/jena/mensa-ernst-abbe-platz.html")
```

#### `_get_meal_categories(soup: BeautifulSoup) -> Tuple[Optional[List[BeautifulSoup]], Optional[List[str]]]`

Extracts menu sections and corresponding category names.

- **Return Type**: Tuple[Optional[List[BeautifulSoup]], Optional[List[str]]]
- **Description**: Extracts menu sections and corresponding category names from the parsed BeautifulSoup object of the Mensa page. If no valid menu sections are found, `(None, None)` is returned.
- **Parameters**:
  - `soup` (BeautifulSoup): Parsed BeautifulSoup object of the Mensa page.
- **Example Usage**:

```python
sections, category_names = scraper._get_meal_categories(soup)
```

#### `_get_menu_by_category(menu_sections: Optional[List[BeautifulSoup]], menu_category_names: Optional[List[str]]) -> Optional[Dict[str, List[str]]]`

Extracts dishes categorized by meal type.

- **Return Type**: Optional[Dict[str, List[str]]]
- **Description**: Extracts dishes categorized by meal type from the list of meal sections and category names. If no valid menu sections or category names are provided, an error message is logged, and `None` is returned.
- **Parameters**:
  - `menu_sections` (Optional[List[BeautifulSoup]]): List of meal sections from the website.
  - `menu_category_names` (Optional[List[str]]): List of category names.
- **Example Usage**:

```python
dishes_by_category = scraper._get_menu_by_category(sections, category_names)
```

#### `_modify_mensa_name(mensa_name: str) -> str`

Formats the Mensa name properly.

- **Return Type**: str
- **Description**: Formats the Mensa name properly by replacing hyphens with spaces and capitalizing the first letter of each word.
- **Parameters**:
  - `mensa_name` (str): Raw Mensa name.
- **Example Usage**:

```python
cleaned_mensa_name = scraper._modify_mensa_name("mensa-ernst-abbe-platz")
```

## Additional Documentation Elements

### Attributes

- `dishes_by_category` (Optional[Dict[str, List[str]]]): Dictionary of categorized dishes from the last scraped menu.
- `mensa_name` (Optional[str]): Name of the last scraped Mensa.
- `location` (Optional[str]): Location of the last scraped Mensa.
- `full_url` (Optional[str]): Full URL of the last scraped Mensa page.
- `logger` (logging.Logger): Logger instance for logging messages.

### Notes or Warnings

- This class uses the `requests` and `beautifulsoup4` libraries for web scraping. Make sure these libraries are installed in your environment.
- The web scraping functionality relies on the structure of the target website. If the website structure changes, the scraping logic may need to be updated.
- The `find_matches` method is case-insensitive.
- The `scrape_menu_by_category` method updates the `dishes_by_category`, `mensa_name`, `location`, and `full_url` attributes of the class instance.