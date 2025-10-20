# content/utils.py
import requests
from django.conf import settings

def notify_n8n(batch, event="approved"):
    """
    Sends a webhook to n8n when a batch changes status (e.g. approved or revised).
    """
    n8n_url = getattr(settings, "N8N_WEBHOOK_URL", None)
    if not n8n_url:
        print("⚠️ N8N_WEBHOOK_URL not set in settings.py")
        return

    payload = {
        "token": batch.token,
        "status": batch.status,
        "chapter_id": batch.chapter_id,
        "event": event,
    }

    try:
        resp = requests.post(n8n_url, json=payload, timeout=5)
        print(f"✅ Notified n8n ({event}):", resp.status_code)
    except Exception as e:
        print("❌ Failed to notify n8n:", e)
