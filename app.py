from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path
import os
from datetime import datetime

app = Flask(__name__)

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TRACKERS_FILE = BASE_DIR / "trackers.json"
SOURCES_FILE = BASE_DIR / "verified_sources.json"
RESULTS_FILE = DATA_DIR / "scout_results.json"

def load_json(path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    results = load_json(RESULTS_FILE)
    trackers = load_json(TRACKERS_FILE)
    feed = load_json(DATA_DIR / "live_feed.json")
    
    # Calculate some summary stats
    alarm_count = sum(1 for r in results if r.get('status') == 'ALARM')
    
    return render_template('index.html', results=results, trackers=trackers, feed=feed, alarm_count=alarm_count, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/config')
def config():
    trackers = load_json(TRACKERS_FILE)
    sources = load_json(SOURCES_FILE)
    return render_template('config.html', trackers=trackers, sources=sources)

@app.route('/report/<tracker_id>')
def report(tracker_id):
    results = load_json(RESULTS_FILE)
    result = next((r for r in results if r.get('tracker_id') == tracker_id), None)
    if not result:
        return "Report not found", 404
    return render_template('report.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
