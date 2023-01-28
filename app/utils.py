import firebase_admin
from firebase_admin import credentials, firestore
from app.config import CONFIG

import os

COLLECTION = os.environ.get("FIRESTORE_COLLECTION", "hosts")

cred = credentials.Certificate(CONFIG)

firebase_admin.initialize_app(cred)

db = firestore.client()


def get_homelab_ip():

    host = db.collection(COLLECTION).where(u'loc', u"==", u"aurora").stream()
    host_one = [h for h in host][0]
    host_dict = host_one.to_dict()
    return f"{host_dict['ip']}:{host_dict['port']}"
