# Notifier Class Documentation

The `Notifier` class is a utility for sending notifications to a Gotify server. It allows you to easily send messages, optionally including a location and website, with a specified title and priority.

## Constructor (__init__ method)

The `__init__` method initializes the Notifier with server details and authentication token.

### Parameters

- `server_url` (str): The URL of the Gotify server.
- `token` (str): Authentication token for the server.
- `priority` (int, optional): Default message priority level (default: 5).
- `secure` (bool, optional): Use HTTPS if True, otherwise HTTP (default: False).

### Example Usage

```python
notifier = Notifier(
    server_url="your-gotify-server.com",
    token="your-access-token",
    priority=10,
    secure=False
)
```

## Methods

### Public Methods

#### send_notification

Sends a notification to the Gotify server.

##### Parameters

- `message` (Union[List[str], str, Dict[str, List[str]]]): Single message, list of messages, or categorized dictionary.
- `website` (str, optional): Mensa website (optional).
- `location` (str, optional): Mensa location (optional).
- `title` (str, optional): Notification title (optional, default: '‼️LunchHunt‼️').
- `priority` (int, optional): Message priority (optional, default: class default priority).

##### Returns

None

##### Example Usage

```python
notifier.send_notification(
    message={"Zwischenversorgung": ["Kokosmilchreis mit Mangosoße"]},
    website="https://www.stw-thueringen.de/mensen/jena/mensa-ernst-abbe-platz.html",
    location="Mensa Ernst Abbe Platz",
    title="‼️LunchHunt‼️",
    priority=10
)
```

### Hidden/Protected Methods

#### _parse_message_input

Parses the input message, location, and website into a formatted string.

##### Parameters

- `location` (str, optional): Mensa location (optional).
- `website` (str, optional): Mensa website (optional).
- `message` (Union[List[str], str, Dict[str, List[str]]]): Single message, list of messages, or categorized dictionary.

##### Returns

str: The formatted message string.

## Additional Documentation Elements

- Attributes: The `Notifier` class has the following attributes:
  - `server_url` (str): The URL of the Gotify server.
  - `token` (str): Authentication token for the server.
  - `priority` (int): Default message priority level.
  - `logger` (logging.Logger): Logger instance for the class.

- Notes or Warnings:
  - The `send_notification` method will log a warning and skip sending the notification if the message content is empty or invalid.
  - The `send_notification` method will log an error if it fails to send the notification due to a network error or server issue.

- Dependencies: The `Notifier` class depends on the `requests` library for sending HTTP requests to the Gotify server.