from lunchhunt.utils import update_menu_categories, load_settings
from lunchhunt import MensaScraper
from lunchhunt import Notifier

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


if __name__ == "__main__":
    logging.info("Starting execution of LunchHunt.")

    if len(sys.argv) > len('.json') + 1:
        settings_file = sys.argv[1]
    else:
        settings_file = 'settings.json'
    logging.info(f"Using settings file: {settings_file}")

    # Get settings for scraper and notifier
    scraper_settings, schedule_settings, gotify_settings = load_settings(
        path=f'/home/lunchhunt/app/settings/{settings_file}'
    )

    # Filter categories depending on time of execution
    menu_categories = update_menu_categories(
        categories=scraper_settings['menu_categories'],
        timetable=None,
        offset=schedule_settings['offset']
    )

    # Initialize scraper
    scraper = MensaScraper(
        menu_categories=menu_categories,
        base_url=None,
        mensa_dict=None
    )
    logging.info("Initialized MensaScraper.")

    # Initialize Notifier
    notifier = Notifier(
        server_url=gotify_settings['server_url'],
        token=gotify_settings['token'],
        priority=gotify_settings['priority'],
        secure=gotify_settings['secure']
    )
    logging.info("Initialized Notifier.")

    for mensa in scraper_settings['mensen']:
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

            if scraper_settings['favorite_foods']:
                # Find matches with favourite food
                logging.info("Find matches with favourite food...")
                matches = scraper.find_matches(
                    # dishes=dishes_by_category,  # Optional
                    keywords=scraper_settings['favorite_foods']
                )

                if matches:
                    logging.info(f"Matched dishes: {matches}\n")
                    notifier.send_notification(
                        message=matches,
                        website=scraper.full_url,
                        location=scraper.mensa_name
                    )
                else:
                    logging.info("No matches found.")
            else:
                notifier.send_notification(
                    message=dishes_by_category,
                    website=scraper.full_url,
                    location=scraper.mensa_name
                )
        else:
            logging.info("No dishes found.")

    logging.info("Finished execution of LunchHunt.")
