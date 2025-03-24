from flask import Flask, render_template, request, jsonify
from mailtm import Email
import random
import string
from datetime import datetime

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

@app.route('/start_listening', methods=['POST'])
def start_listening():
    try:
        def listener(message):
            email_content = {
                "id": len(received_emails) + 1,
                "sender": message.get('from', 'Unknown Sender'),
                "subject": message.get('subject', 'No Subject'),
                "content": message.get('text', message.get('html', 'No Content')),
                "timestamp": datetime.now().strftime("%b %d, %H:%M")
            }
            received_emails.append(email_content)

        email_client.start(listener, interval=1)
        return jsonify({"message": "Started listening for new emails"})
    except Exception as e:
        return jsonify({"error": f"Failed to start listening: {str(e)}"}), 500

@app.route('/get_emails', methods=['GET'])
def get_emails():
    if not received_emails:
        return jsonify([])
    return jsonify(received_emails)

@app.route('/download_email/<int:email_id>', methods=['GET'])
def download_email(email_id):
    email = next((e for e in received_emails if e['id'] == email_id), None)
    if email:
        return jsonify({"message": f"Downloaded email: {email['subject']}"})
    return jsonify({"error": "Email not found"}), 404

@app.route('/delete_email/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    global received_emails
    received_emails = [e for e in received_emails if e['id'] != email_id]
    return jsonify({"message": f"Deleted email with ID: {email_id}"})

if __name__ == '__main__':
    app.run(debug=True)
