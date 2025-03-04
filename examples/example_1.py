from LunchHunt import MensaScraper
from LunchHunt import Notifier

import logging
import sys

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout instead of a file
    ]
)

mensen = [
    "MAS",  # Erfurt: mensa-altonaer-strasse
    "EAP",  # Jena: mensa-ernst-abbe-platz
    "CZP",  # Jena: mensa-carl-zeiss-promenade
    "MAP",  # Weimar: mensa-am-park
    "MEH",  # Ilmenau: mensa-ehrenberg
    "MBH",  # Schmalkalden: mensa-blechhammer
    "MWF",  # Gera: mensa-weg-der-freundschaft
    "MAW",  # Eisenach: mensa-am-wartenberg
    "MWH",  # Nordhausen: mensa-weinberghof
]

if __name__ == "__main__":

    logging.info("Starting example_1.py script...")

    menu_categories = [
        "Frühstück",
        "Mittagessen",
        "Zwischenversorgung",
        "Abendessen"
    ]

    # Initialize scraper
    scraper = MensaScraper(
        menu_categories=menu_categories
    )
    logging.info("Initialized MensaScraper.")

    # Initialize Notifier
    notifier = Notifier(
        server_url="your-gotify-sever.com",
        token="your-access-token",
        priority=10,
        secure=False  # Set to True if your MinIO server is HTTPS
    )
    logging.info("Initialized Notifier.")

    for mensa in mensen:
        logging.info(f"\nGet dishes of {mensa} by category...")
        # Get dishes by category
        dishes_by_category = scraper.scrape_menu_by_category(
            mensa=mensa
        )

        if dishes_by_category:
            for key in dishes_by_category:
                logging.info(f"\nDishes for {key}:")
                for value in dishes_by_category[key]:
                    logging.info(value)

            notifier.send_notification(
                message=dishes_by_category,
                website=scraper.full_url,
                location=scraper.mensa_name
            )

    logging.info(
        "Finished execution of example_1.py."
    )
