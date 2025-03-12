import logging
import requests
from bs4 import BeautifulSoup
from typing import Union, List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


class MensaScraper:
    """
    A web scraper for extracting the daily menu from university canteens.
    """

    def __init__(
        self,
        menu_categories: Optional[Union[List[str], str]] = None,
        base_url: Optional[str] = None,
        mensa_dict: Optional[Dict[str, Tuple[str, str]]] = None
    ):
        """
        Initializes the MensaScraper with a base URL and Mensa mappings.

        :param menu_categories: Categories to filter meals by (default: all).
        :param base_url: Base URL for the Mensa website.
        :param mensa_dict: Custom mapping of Mensa codes to locations and URLs.
        """
        self.menu_categories = (
            [menu_categories] if isinstance(menu_categories, str)
            else menu_categories
        ) or ["Frühstück", "Mittagessen", "Zwischenversorgung", "Abendessen"]

        self.base_url = base_url or "https://www.stw-thueringen.de/mensen"
        self.mensa_dict = mensa_dict or self._default_mensa_dict()

        self.dishes_by_category: Optional[Dict[str, List[str]]] = None
        self.mensa_name: Optional[str] = None
        self.location: Optional[str] = None
        self.full_url: Optional[str] = None

        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _default_mensa_dict() -> Dict[str, Tuple[str, str]]:
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

    def _build_mensa_url(
            self,
            mensa: str,
            location: str
    ) -> str:
        """
        Constructs the Mensa URL based on the identifier.

        :param mensa: Mensa code.
        :param location: Location name.
        :return: Constructed URL or empty string if invalid.
        """
        if mensa not in self.mensa_dict:
            self.logger.error(f"Invalid Mensa code: {mensa}")
            return ""

        _, mensa_name = self.mensa_dict[mensa]
        return f"{self.base_url}/{location}/{mensa_name}.html"

    def _get_soup(
            self,
            url: str
    ) -> Optional[BeautifulSoup]:
        """
        Fetches and parses the HTML content of a given URL.

        :param url: Target URL.
        :return: BeautifulSoup object or None if request fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch URL {url}: {e}")
            return None

    @staticmethod
    def _get_meal_categories(
            soup: BeautifulSoup
    ) -> Tuple[Optional[List[BeautifulSoup]], Optional[List[str]]]:
        """
        Extracts menu sections and corresponding category names.

        :param soup: Parsed BeautifulSoup object of the Mensa page.
        :return: Tuple of (sections, category names) or (None, None) on failure.
        """
        sections = soup.find_all(
            'div', class_='container-fluid px-xl-0 splGroupWrapper'
        )

        category_names = [
            (section.find('div', class_='pl-2').get_text(strip=True)
             or "Unknown Category") for section in sections
        ]

        return (sections, category_names) if sections and category_names\
            else (None, None)

    def _get_menu_by_category(
        self,
        menu_sections: Optional[List[BeautifulSoup]],
        menu_category_names: Optional[List[str]]
    ) -> Optional[Dict[str, List[str]]]:
        """
        Extracts dishes categorized by meal type.

        :param menu_sections: List of meal sections from the website.
        :param menu_category_names: List of category names.
        :return: Dictionary of categorized dishes or None if no data found.
        """
        if not menu_sections or not menu_category_names:
            self.logger.error("No valid menu sections found.")
            return None

        dishes_by_category = {
            category: [
                f"\u2022 {meal.get_text(strip=True)}"
                for meal in section.find_all('div', class_='mealText')
            ]
            for section, category in zip(menu_sections, menu_category_names)
            if category in self.menu_categories
        }

        return dishes_by_category or None

    def scrape_menu_by_category(
            self,
            mensa: str
    ) -> Optional[Dict[str, List[str]]]:
        """
        Scrapes the categorized menu for a given Mensa.

        :param mensa: Mensa code.
        :return: Dictionary of categorized dishes or None on failure.
        """
        if mensa not in self.mensa_dict:
            raise ValueError(f"Unknown Mensa code: {mensa}")

        location, _ = self.mensa_dict[mensa]
        self.full_url = self._build_mensa_url(mensa, location)
        self.mensa_name = self._modify_mensa_name(mensa)
        self.location = location

        soup = self._get_soup(self.full_url)
        if not soup:
            return None

        menu_sections, category_names = self._get_meal_categories(soup)
        self.dishes_by_category = self._get_menu_by_category(
            menu_sections, category_names
        )

        return self.dishes_by_category

    def _modify_mensa_name(
            self,
            mensa_name: str
    ) -> str:
        """
        Formats the Mensa name properly.

        :param mensa_name: Raw Mensa name.
        :return: Cleaned and formatted Mensa name.
        """
        _, mensa_name = self.mensa_dict.get(mensa_name, (None, mensa_name))
        return mensa_name.replace("-", " ").title()

    def find_matches(
            self,
            keywords: Union[List[str], str],
            dishes: Optional[Union[List[str], Dict[str, List[str]]]] = None
    ) -> Optional[Union[List[str], Dict[str, List[str]]]]:
        """
        Finds menu items that contain specified keywords.

        :param keywords: Single keyword or list of keywords to search for.
        :param dishes: List of dishes or dictionary of categories with
         dish lists. Defaults to last scraped menu.
        :return: List of matching dishes if input is a list, or dictionary
         with matching dishes per category if input is a dict. Returns None
         if no matches are found.
        """
        if not dishes:
            dishes = self.dishes_by_category
            if not dishes:
                self.logger.error("No dishes available for searching.")
                return None

        keywords = [keywords.lower()] if isinstance(keywords, str) else [
            kw.lower() for kw in keywords
        ]

        if isinstance(dishes, list):
            matches = [
                dish for dish in dishes
                if any(kw in dish.lower() for kw in keywords)
            ]
            return matches if matches else None

        if isinstance(dishes, dict):
            matched_dishes = {
                category: [
                    dish for dish in dish_list
                    if any(kw in dish.lower() for kw in keywords)
                ]
                for category, dish_list in dishes.items()
            }

            return {
                category: matches for category, matches in
                matched_dishes.items() if matches
            } or None

        self.logger.error(
            "Invalid data type for dishes. Expected list or dict.")
        return None
