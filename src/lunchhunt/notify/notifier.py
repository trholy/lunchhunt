import logging
import requests
from typing import List, Dict, Union, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


class Notifier:
    """
    A notification sender for Gotify servers.
    """

    def __init__(
            self,
            server_url: str,
            token: str,
            priority: int = 5,
            secure: bool = False
    ):
        """
        Initializes the Notifier with server details and authentication token.

        :param server_url: The URL of the Gotify server.
        :param token: Authentication token for the server.
        :param priority: Default message priority level (default: 5).
        :param secure: Use HTTPS if True, otherwise HTTP (default: False).
        """
        protocol = "https" if secure else "http"
        self.server_url = f"{protocol}://{server_url}/message"
        self.token = token
        self.priority = priority

        self.logger = logging.getLogger(__name__)

    def send_notification(
            self,
            message: Union[List[str], str, Dict[str, List[str]]],
            website: Optional[str] = None,
            location: Optional[str] = None,
            title: Optional[str] = "‼️LunchHunt‼️",
            priority: Optional[int] = None,
    ) -> None:
        """
        Sends a notification to the Gotify server.

        :param message: Single message, list of messages,
         or categorized dictionary.
        :param location: Mensa location (optional).
        :param website: Mensa website (optional).
        :param title: Notification title (optional, default: '‼️LunchHunt‼️').
        :param priority: Message priority
         (optional, default: class default priority).
        """
        full_message = self._parse_message_input(location, website, message)

        if not full_message.strip():
            self.logger.warning(
                "No valid message content to send. Skipping notification.")
            return

        payload = {
            "title": title,
            "message": full_message,
            "priority": priority or self.priority,
        }
        headers = {"X-Gotify-Key": self.token}

        try:
            response = requests.post(
                self.server_url, json=payload, headers=headers
            )
            response.raise_for_status()
            self.logger.info("Notification sent successfully!")
        except requests.RequestException as e:
            self.logger.error(f"Failed to send notification: {e}")

    def _parse_message_input(
            self,
            location: Optional[str],
            website: Optional[str],
            msg_input: Union[List[str], str, Dict[str, List[str]]],
    ) -> str:
        """
        Parses the input message and ensures proper formatting
         for notifications.

        :param location: Mensa location (optional).
        :param website: Mensa website (optional).
        :param msg_input: Message input (string, list, or dictionary).
        :return: Formatted string ready to send as a notification.
        """
        if isinstance(msg_input, str):
            msg_input = [msg_input]  # Convert single message to list

        if isinstance(msg_input, dict):
            return self._format_dict_message(location, website, msg_input)

        if isinstance(msg_input, list):
            msg_list = msg_input.copy()
            if location:
                msg_list.insert(0, location)
            if website:
                msg_list.append(website)
            return "\n".join(msg_list)

        self.logger.error(
            "Invalid message format. Expected str, list, or dict.")
        return ""

    @staticmethod
    def _format_dict_message(
            location: Optional[str],
            website: Optional[str],
            msg_dict: Dict[str, List[str]]
    ) -> str:
        """
        Formats a dictionary of messages into a structured string.

        :param location: Mensa location (optional).
        :param website: Mensa website (optional).
        :param msg_dict: Dictionary where keys are categories and
         values are lists of messages.
        :return: Formatted string representation of the dictionary.
        """
        message_parts = []

        for category, dishes in msg_dict.items():
            category_header = f"\n{category.upper()} - {location}"\
                if location else f"\n{category.upper()}"
            message_parts.append(category_header)
            message_parts.extend(dishes)

        if website:
            message_parts.append(website)

        return "\n".join(message_parts)
