# Example Usage: Multiple Mensas Dishes Notification

This example script demonstrates how to use the `MensaScraper` and `Notifier` classes to send notifications for multiple mensas.

## Prerequisites

- Python 3.x
- `MensaScraper` and `Notifier` classes from the project
- A Gotify server with a valid access token

## Usage

1. Define the list of mensas:

```python
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
```

2. Initialize the `MensaScraper` and `Notifier` classes:

```python
# Initialize scraper
scraper = MensaScraper()

# Initialize Notifier
notifier = Notifier(
    server_url="your-gotify-server.com",
    token="your-access-token",
    priority=10,
    secure=False  # Set to True if your Gotify server is HTTPS
)
```

3. Iterate over the list of mensas and send notifications:

```python
for mensa in mensen:
    # Get dishes by category
    dishes_by_category = scraper.scrape_menu_by_category(mensa)

    if dishes_by_category:
        # Send notification
        notifier.send_notification(
            message=dishes_by_category,
            website=scraper.full_url,
            location=scraper.mensa_name
        )
```

4. Run the script:

```bash
python example_1.py
```

## Notes

- The script sends a notification using the `Notifier` class for each mensa in the list.
- Make sure to replace `"your-gotify-server.com"` and `"your-access-token"` with your Gotify server URL and access token.
