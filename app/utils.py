import firebase_admin
from firebase_admin import credentials, firestore
from app.config import CONFIG, ONEDRIVE_CONFIG
from datetime import datetime, timedelta
import requests

import os

COLLECTION = os.environ.get("FIRESTORE_COLLECTION", "hosts")

cred = credentials.Certificate(CONFIG)

firebase_admin.initialize_app(cred)

db = firestore.client()

HOST_CACHE = {"url": "", "updated_time": datetime.utcnow()}

ONEDRIVE_CACHE = {"token": ""}


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
    host = db.collection(COLLECTION).where("loc", "==", "aurora").stream()
    host_one = [h for h in host][0]
    host_dict = host_one.to_dict()
    return f"{host_dict['ip']}:{host_dict['port']}"


def _refresh_token():
    token = requests.post(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data={
            "client_id": ONEDRIVE_CONFIG["client_id"],
            "client_secret": ONEDRIVE_CONFIG["client_secret"],
            "scope": ONEDRIVE_CONFIG["scope"],
            "grant_type": ONEDRIVE_CONFIG["grant_type"],
            "refresh_token": ONEDRIVE_CONFIG["refresh_token"]
        },
    ).json()["access_token"]

    ONEDRIVE_CACHE["token"] = token
    return token


def _get_blogs(token, url):
    headers = {"Authorization": "Bearer " + token}
    blogs = requests.get(url, headers=headers)
    return blogs


def get_blogs(id: str | None):
    if not id:
        url = (
            "https://graph.microsoft.com/v1.0/me/drive/items/"
            "1A2DAB738E5C68F9!3873/children?"
            "$top=5000&$expand=thumbnails($select=medium)&"
            "$select=id,name,size,lastModifiedDateTime,content.downloadUrl,file,parentReference"
        )
    else:
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{id}/content"

    token = ONEDRIVE_CACHE["token"]

    if not token:
        token = _refresh_token()

    blogs = _get_blogs(token, url)
    if blogs.status_code == 401:
        token = _refresh_token()
        blogs = _get_blogs(token, url)

    return blogs.json()["value"] if not id else [{"content": blogs.text}]
