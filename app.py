from flask import Flask, request, render_template_string, session, jsonify
from mapping import get_maps
from query_handler import get_relevant_canonical_headings
from geminiCall import query_itinerary  # your existing Gemini function
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load your maps
heading_tags_map, section_map = get_maps()
MAX_QUESTIONS = 10

# Inline HTML template for chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Itinerary Mini-Bot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1000px; margin: 50px auto; display: flex; flex-direction: column; background: #f2f2f2; }
        .container { display: flex; gap: 10px; }
        .chat-box { flex: 1; border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; background: #ffffff; border-radius: 10px; }
        .cited-box { width: 400px; border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: auto; background: #f9f9f9; border-radius: 10px; }
        .message { padding: 10px 15px; border-radius: 15px; margin: 5px 0; max-width: 80%; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); word-wrap: break-word; }
        .user { background-color: #dcf8c6; align-self: flex-end; text-align: right; }
        .bot { background-color: #f1f0f0; color: #333; align-self: flex-start; text-align: left; }
        .heading { font-weight: bold; margin-top: 5px; }
        input[type="text"] { width: 80%; padding: 10px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px; margin-top: 10px; border-radius: 5px; border: none; background-color: #4CAF50; color: white; cursor: pointer; }
        button:hover { background-color: #45a049; }
        #input-container { display: flex; gap: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Itinerary Mini-Bot</h2>
    <div class="container">
        <div class="chat-box" id="chat-box"></div>
        <div class="cited-box" id="cited-box">
            <p><em>Cited text from itinerary will appear here...</em></p>
        </div>
    </div>
    <div id="input-container">
        <input type="text" id="query" placeholder="Type your question..."/>
        <button onclick="sendQuery()">Send</button>
    </div>

    <script>
        function addMessage(text, sender) {
            const chatBox = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = 'message ' + sender;
            div.textContent = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function updateCited(heading, line) {
            const citedBox = document.getElementById('cited-box');
            if (heading === "na" || !line) {
                citedBox.innerHTML = "<p><em>No cited text available.</em></p>";
            } else {
                citedBox.innerHTML = `<p><em>Cited text from the itinerary:</em></p>
                                      <div class="heading">${heading}</div>
                                      <div>${line}</div>`;
            }
        }

        async function sendQuery() {
            const queryInput = document.getElementById('query');
            const query = queryInput.value.trim();
            if (!query) return;
            addMessage(query, 'user');
            queryInput.value = '';

            const response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query})
            });
            const data = await response.json();
            addMessage(data.response, 'bot');

            updateCited(data.heading, data.data_line);
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    session['question_count'] = 0
    return render_template_string(HTML_TEMPLATE)


@app.route("/ask", methods=["POST"])
def ask():
    if 'question_count' not in session:
        session['question_count'] = 0

    if session['question_count'] >= MAX_QUESTIONS:
        return jsonify({
            "response": "You have reached 10 questions. Please wait a while before asking again.",
            "heading": "na",
            "data_line": ""
        })

    user_query = request.json.get("query", "").strip()
    if not user_query:
        return jsonify({"response": "Please enter a query.", "heading": "na", "data_line": ""})

    matched_headings_set = get_relevant_canonical_headings(user_query)
    if not matched_headings_set:
        session['question_count'] += 1
        return jsonify({"response": "I don’t see this in your itinerary — contact support",
                        "heading": "na", "data_line": ""})

    matched_headings_list = list(matched_headings_set)
    matched_section_map = {h: section_map.get(h, []) for h in matched_headings_list}

    result = query_itinerary(user_query)
    session['question_count'] += 1

    heading = result.get("heading", "na")
    data_idx = result.get("data_index", -1)
    explanation = result.get("explanation", "")

    if heading == "na" or data_idx == -1:
        data_line = ""
        response_text = explanation
    else:
        data_line = matched_section_map.get(heading, [""])[data_idx]
        response_text = f"{explanation}"

    return jsonify({
        "response": response_text,
        "heading": heading,
        "data_line": data_line
    })


if __name__ == "__main__":
    app.run(debug=True)
