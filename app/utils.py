import firebase_admin
from firebase_admin import credentials, firestore
from app.config import CONFIG
from datetime import datetime, timedelta

import os

COLLECTION = os.environ.get("FIRESTORE_COLLECTION", "hosts")

cred = credentials.Certificate(CONFIG)

firebase_admin.initialize_app(cred)

db = firestore.client()

HOST_CACHE = {
    "url": "",
    "updated_time": datetime.utcnow()
}


def get_homelab_ip():
    if not HOST_CACHE["url"]:
        url = _get_homelab_ip()
        HOST_CACHE["url"] = url
        HOST_CACHE["updated_time"] = datetime.utcnow()
        return url

    time_delta = HOST_CACHE["updated_time"] - datetime.utcnow()

    if time_delta >= timedelta(hours=23):
        url = _get_homelab_ip()
        HOST_CACHE["url"] = url
        HOST_CACHE["updated_time"] = datetime.utcnow()
        return url

    return HOST_CACHE["url"]


def _get_homelab_ip():
    host = db.collection(COLLECTION).where(u'loc', u"==", u"aurora").stream()
    host_one = [h for h in host][0]
    host_dict = host_one.to_dict()
    return f"{host_dict['ip']}:{host_dict['port']}"
