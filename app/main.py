from flask import Flask, jsonify
from flask import request
from app.utils import get_homelab_ip, get_blogs
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"homelab-proxy": "python client"}), 200


@app.route("/get")
def proxy_get():
    target = request.args.get("target")
    url = f"https://{get_homelab_ip()}/{target}"
    rsp = requests.get(url, verify=False)
    return rsp.json(), 200


@app.route("/other-get")
def other_get():
    target = request.args.get("t")
    rsp = requests.get(target, verify=False)
    return rsp.content, 200


@app.route("/blog/<id>")
@app.route("/blog")
def get_blog(id: str | None = None):
    blogs = get_blogs(id)
    return jsonify(blogs), 200
