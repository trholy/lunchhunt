# Example Usage: Favorite Foods Notification

This example script demonstrates how to use the `MensaScraper` and `Notifier` classes to send notifications for favorite foods available in a specific mensa.

## Prerequisites

- Python 3.x
- `MensaScraper` and `Notifier` classes from the project
- A Gotify server with a valid access token

## Usage

1. Define your favorite foods:

```python
favorite_foods = [
    "Eierkuchen",
    "Milchreis",
    "Hefeklöße",
    "Germknödel",
    "Kaiserschmarrn",
    "Waffel",
    "Kartoffelpuffer"
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

3. Scrape the menu by category and find matches with favorite foods:

```python
# Get dishes by category
dishes_by_category = scraper.scrape_menu_by_category("EAP")

if dishes_by_category:
    # Find matches with favorite food
    matches = scraper.find_matches(keywords=favorite_foods)

    if matches:
        # Send notification
        notifier.send_notification(
            message=matches,
            website=scraper.full_url,
            location=scraper.mensa_name
        )
```

4. Run the script:

```bash
python example_2.py
```

## Notes

- The script sends a notification using the `Notifier` class if any favorite foods are found in the menu.
- Make sure to replace `"your-gotify-server.com"` and `"your-access-token"` with your Gotify server URL and access token.
