from flask import Flask, render_template, request, jsonify
from mailtm import Email
import random
import string

app = Flask(__name__)
email_client = Email()  # Initialize the Email object
current_email = None  # Store the current email address
received_emails = []  # Store received emails

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_domain', methods=['GET'])
def get_domain():
    try:
        domain = email_client.domain
        return jsonify({"domain": domain})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch domain: {str(e)}"}), 500

@app.route('/register_email', methods=['POST'])
def register_email():
    global current_email
    try:
        data = request.get_json()
        email_prefix = data.get("email_prefix", "").strip()

        if not email_prefix:
            return jsonify({"error": "Email prefix is required."}), 400

        # Generate a random suffix to ensure uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        # Combine prefix with a random suffix
        email_client.register(email_prefix + random_suffix)
        current_email = email_client.address
        return jsonify({"email": current_email})
    except Exception as e:
        return jsonify({"error": f"Failed to register email: {str(e)}"}), 500

@app.route('/copy_email', methods=['POST'])
def copy_email():
    if current_email:
        return jsonify({"message": "Email copied to clipboard!", "email": current_email})
    return jsonify({"error": "No email to copy!"}), 400

@app.route('/start_listening', methods=['POST'])
def start_listening():
    try:
        def listener(message):
            email_content = {
                "subject": message.get('subject', 'No Subject'),
                "content": message.get('text', message.get('html', 'No Content')),
                "is_html": 'html' in message
            }
            received_emails.append(email_content)

        email_client.start(listener, interval=1)
        return jsonify({"message": "Started listening for new emails"})
    except Exception as e:
        return jsonify({"error": f"Failed to start listening: {str(e)}"}), 500

@app.route('/get_emails', methods=['GET'])
def get_emails():
    if not received_emails:
        return jsonify({"message": "No emails received yet."})
    
    return jsonify(received_emails)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

