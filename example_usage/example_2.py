from lunchhunt import MensaScraper
from lunchhunt import Notifier

from datetime import datetime, time
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

favorite_foods = [
    "Eierkuchen",
    "Milchreis",
    "Hefeklöße",
    "Germknödel",
    "Kaiserschmarrn",
    "Waffel",
    "Kartoffelpuffer"
]

if __name__ == "__main__":

    logging.info("Starting example_2.py script...")

    mensa = "EAP"
    menu_categories = [
        "Frühstück",
        "Mittagessen",
        "Zwischenversorgung",
        "Abendessen"
    ]

    """  
    Timetable:
    
    Warmes Frühstück
    8:00 - 10:00 Uhr
    Mittagsversorgung
    11:00 - 14:00 Uhr 
    Zwischenversorgung
    15:00 - 16:30 Uhr
    Abendmensa
    17:30 - 19:30 Uhr
    """
    time_now = datetime.now().time()
    if time_now >= time(9, 30):
        menu_categories.remove("Frühstück")
    if time_now >= time(13, 30):
        menu_categories.remove("Mittagessen")
    if time_now >= time(16, 00):
        menu_categories.remove("Zwischenversorgung")

    # Initialize scraper
    scraper = MensaScraper(
        menu_categories=menu_categories,
        base_url=None,
        mensa_dict=None
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

        # Find matches with favourite food
        logging.info("Find matches with favourite food...")
        matches = scraper.find_matches(
            # dishes=dishes_by_category,  # Optional
            keywords=favorite_foods
        )

        if matches:
            logging.info(f"Matched dishes: {matches}\n")

            notifier.send_notification(
                message=matches,
                website=scraper.full_url,
                location=scraper.mensa_name
            )
            logging.info("Finished execution of example_2.py.")

        else:
            logging.info(
                "No matches found. Finished execution of example_2.py."
            )

    else:
        logging.info(
            "No dishes found. Finished execution of example_2.py."
        )
