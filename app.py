from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        user_message = request.json["message"]
        print("User Message:", user_message)

        # Send POST request to Rasa server
        rasa_response = requests.post(RASA_API_URL, json={"message": user_message})
        rasa_response.raise_for_status()  

        rasa_response_json = rasa_response.json()
        print("Rasa Response:", rasa_response_json)

        # Extract response text from Rasa response
        bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t understand that.'
        return jsonify({'response': bot_response})
    
    except requests.exceptions.RequestException as e:
        print("Error connecting to Rasa server:", e)
        return jsonify({'response': 'Error connecting to Rasa server'})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
