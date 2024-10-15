import os
import json
import requests
from utils.media import post_media_file
from io import BytesIO


def mark_as_read(phone_number_id: str, message_id: str):
    """
    Mark a message as read
    """
    response = requests.post(
        f"https://graph.facebook.com/v19.0/{phone_number_id}/messages",
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {os.environ.get("GRAPH_API_TOKEN")}'
        },
        json={
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
    )
    response.raise_for_status()


def send_text(phone_number_id: str, sender: str, text: str, reply_to_id: str = None):
    """
    Send a text message
    """
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": sender,
        "type": "text",
        "text": {
            "preview_url": "false",
            "body": text
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("GRAPH_API_TOKEN")}',
    }
    if reply_to_id:
        payload['context'] = {'message_id': reply_to_id}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()


def send_media(phone_number_id: str, sender: str, media_type: str, media_buffer: BytesIO, reply_to_id: str = None):
    """
    Send a media message
    """
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    media_id = post_media_file(phone_number_id, media_buffer)
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": sender,
        "type": media_type,
        media_type: {
            "id": media_id
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("GRAPH_API_TOKEN")}',
    }
    if reply_to_id:
        payload['context'] = {'message_id': reply_to_id}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()