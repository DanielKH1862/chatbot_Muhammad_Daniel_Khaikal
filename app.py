from flask import Flask, request, jsonify, render_template
import main
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# Chat history storage directory
CHAT_HISTORY_DIR = "chat_history"
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

def save_chat(chat_id, title, messages):
    """Save a chat conversation to a JSON file"""
    chat_data = {
        "id": chat_id,
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    filepath = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=2)
    return chat_data

def load_chat(chat_id):
    """Load a chat conversation from a JSON file"""
    filepath = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def get_all_chats():
    """Get all chat conversations sorted by timestamp (newest first)"""
    chats = []
    if os.path.exists(CHAT_HISTORY_DIR):
        for filename in os.listdir(CHAT_HISTORY_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(CHAT_HISTORY_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    chat = json.load(f)
                    chats.append(chat)
    # Sort by timestamp (newest first)
    chats.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return chats

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # tampilkan UI

@app.route("/api/chats", methods=["GET"])
def get_chats():
    """Get all chat history"""
    chats = get_all_chats()
    # Return simplified version without full message history
    return jsonify([{
        "id": chat["id"],
        "title": chat["title"],
        "timestamp": chat["timestamp"],
        "message_count": len(chat.get("messages", []))
    } for chat in chats])

@app.route("/api/chats/latest", methods=["GET"])
def get_latest_chats():
    """Get 5 most recent chats"""
    chats = get_all_chats()[:5]
    return jsonify([{
        "id": chat["id"],
        "title": chat["title"],
        "timestamp": chat["timestamp"],
        "message_count": len(chat.get("messages", []))
    } for chat in chats])

@app.route("/api/chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    """Get a specific chat conversation"""
    chat = load_chat(chat_id)
    if chat:
        return jsonify(chat)
    return jsonify({"error": "Chat not found"}), 404

@app.route("/api/chat", methods=["POST"])
def create_chat():
    """Create a new chat conversation"""
    data = request.get_json()
    chat_id = str(uuid.uuid4())
    title = data.get("title", f"Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    messages = data.get("messages", [])
    chat = save_chat(chat_id, title, messages)
    return jsonify(chat), 201

@app.route("/api/chat/<chat_id>", methods=["PUT"])
def update_chat(chat_id):
    """Update an existing chat conversation"""
    data = request.get_json()
    chat = load_chat(chat_id)
    if not chat:
        return jsonify({"error": "Chat not found"}), 404
    
    # Update messages and title if provided
    if "messages" in data:
        chat["messages"] = data["messages"]
    if "title" in data:
        chat["title"] = data["title"]
    
    chat["timestamp"] = datetime.now().isoformat()
    save_chat(chat_id, chat["title"], chat["messages"])
    return jsonify(chat)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "prompt tidak boleh kosong"}), 400

    result = main.generate_text(prompt)
    return jsonify({"prompt": prompt, "result": result})

@app.route("/generate-http", methods=["POST"])
def generate_http():
    """Generate using direct HTTP API (Gemini 2.0 Flash)"""
    data = request.get_json()
    prompt = data.get("prompt", "")
    model_name = data.get("model", "gemini-2.0-flash")

    if not prompt:
        return jsonify({"error": "prompt tidak boleh kosong"}), 400

    try:
        result = main.generate_text_http(prompt, model_name)
        return jsonify({"prompt": prompt, "result": result, "model": model_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)