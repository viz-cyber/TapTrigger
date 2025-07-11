from flask import Flask, request, jsonify
import json
import os
import sys
import trigger  # ✅ simplified import

app = Flask(__name__)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # When bundled by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # When running from source
    return os.path.join(base_path, relative_path)

# Load routes from file
ROUTES_PATH = resource_path("Routes.json")
with open(ROUTES_PATH, 'r') as f:
    ROUTES = json.load(f)

@app.route('/<path:trigger_name>', methods=['GET', 'POST'])
def handle_trigger(trigger_name):
    action = ROUTES.get(trigger_name)
    if not action:
        return jsonify({"status": "error", "message": "Trigger not found"}), 404

    try:
        action_str = f"{action['type']}:{action['action']}"
        result = trigger.execute_action(action_str)

        return jsonify({"status": "success", "message": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def start_server():
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    start_server()
