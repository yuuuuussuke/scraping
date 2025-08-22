#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)


def load_articles(json_path: str = "news_articles.json"):
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


@app.route("/")
def index():
    articles = load_articles()
    # 最新順に並べ替え（scraped_atがある場合）
    def sort_key(a):
        ts = a.get("scraped_at") or ""
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime.min

    articles_sorted = sorted(articles, key=sort_key, reverse=True)
    return render_template("index.html", articles=articles_sorted)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


