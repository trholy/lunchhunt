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

#### `__parse_message_input`

Parses the input message, location, and website into a formatted string.

##### Parameters

- `location` (str, optional): Mensa location (optional).
- `website` (str, optional): Mensa website (optional).
- `message` (Union[List[str], str, Dict[str, List[str]]]): Single message, list of messages, or categorized dictionary.

##### Returns

str: The formatted message string.


#### `__format_dict_message`

Formats a dictionary of messages into a structured string.

##### Parameters

- `location` (Optional[str]): Mensa location (optional). If provided, it will be included in the category header.
- `website` (Optional[str]): Mensa website (optional). If provided, it will be appended to the end of the formatted message.
- `msg_dict` (dict[str, list[str]]): Dictionary where keys are categories and values are lists of messages. Each category will be formatted into a header followed by its corresponding list of messages.

##### Returns

- `str`: Formatted string representation of the dictionary. The string includes category headers, messages, and optionally the website.
