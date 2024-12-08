from bigbytes.services.google_chat.config import GoogleChatConfig
import requests


def send_google_chat_message(
    config: GoogleChatConfig,
    message: str,
    title: str = 'Bigbytes pipeline run status logs',
) -> None:
    requests.post(
        url=config.webhook_url,
        json={
            'text': '*{title}*\n{message}'.format(title=title, message=message),
        },
    )
