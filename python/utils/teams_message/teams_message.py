"""Tutorial on How to set-up the Teams channel: https://www.datacamp.com/tutorial/how-to-send-microsoft-teams-messages-with-python"""
import pymsteams


# Microsoft Teams Channel Link
channel_link = ""  # Replace with your actual Microsoft Teams channel webhook URL

# Key Vault Secrets (Replace with your actual values)
kv_secret_name = 'Title of the message' 
kv_name = '' 

def notify_to_teams(message: str, web_hook_url: str, title: str) -> bool:
    """Sends a notification message to a Microsoft Teams channel using a webhook.

    Args:
        message: The message content to send.
        web_hook_url: The Microsoft Teams webhook URL.
        title: The title to display in the Teams message card.
    """
    teams_message = pymsteams.connectorcard(web_hook_url)
    teams_message.title(title)
    teams_message.text(message)
    return teams_message.send()


if __name__ == "__main__":
    message = 'Hi, this message is from a Python application using the Webhook connector.'
    notify_to_teams(message, channel_link, kv_secret_name) 
