from flask import Flask
from flask import request, redirect
from app.utils import get_homelab_ip
import requests

app = Flask(__name__)


@app.route("/proxy")
def hello_world():
    target = request.args.get('endpoint')
    url = f"https://{get_homelab_ip()}/{target}"
    rsp = requests.get(url, verify=False)
    # redirect(f"https://{get_homelab_ip()}/{target}")
    return rsp.json(), 200
