from flask import Flask, render_template, request, jsonify
from mailtm import Email
import random
import string
import threading
import time

app = Flask(__name__)

# Global variables to store email client and state
email_client = None  # Email object
current_email = None  # Store the current email address
received_emails = []  # Store received emails
listener_thread = None  # Thread for listening to emails
is_listening = False  # Flag to track if listening is active

def initialize_email_client():
    """Initialize the Email client."""
    global email_client
    try:
        email_client = Email()
    except Exception as e:
        print(f"Failed to initialize email client: {str(e)}")
        raise

# Initialize the email client when the app starts
initialize_email_client()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/get_domain', methods=['GET'])
def get_domain():
    """Fetch the domain for the temporary email."""
    try:
        domain = email_client.domain
        return jsonify({"domain": domain})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch domain: {str(e)}"}), 500

@app.route('/register_email', methods=['POST'])
def register_email():
    """Register a new temporary email address."""
    global current_email, received_emails, is_listening
    try:
        # Stop any existing listener before registering a new email
        if is_listening:
            stop_listening()

        data = request.get_json()
        email_prefix = data.get("email_prefix", "").strip()

        if not email_prefix:
            return jsonify({"error": "Email prefix is required."}), 400

        # Generate a random suffix to ensure uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        # Combine prefix with a random suffix
        email_client.register(email_prefix + random_suffix)
        current_email = email_client.address
        received_emails = []  # Reset received emails for the new address
        return jsonify({"email": current_email})
    except Exception as e:
        return jsonify({"error": f"Failed to register email: {str(e)}"}), 500

@app.route('/copy_email', methods=['POST'])
def copy_email():
    """Return the current email address for copying."""
    if current_email:
        return jsonify({"message": "Email copied to clipboard!", "email": current_email})
    return jsonify({"error": "No email to copy!"}), 400

def email_listener():
    """Listener function to handle incoming emails."""
    global received_emails
    while is_listening:
        try:
            # Fetch new messages
            messages = email_client.get_messages()
            for message in messages:
                # Extract sender's email address (assuming 'from' field exists in the message)
                sender = message.get('from', {}).get('address', 'Unknown Sender')
                email_content = {
                    "id": message.get('id', len(received_emails)),
                    "sender": sender,  # Add sender information
                    "subject": message.get('subject', 'No Subject'),
                    "content": message.get('text', message.get('html', 'No Content')),
                    "is_html": 'html' in message,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                # Avoid duplicates by checking message ID
                if not any(email['id'] == email_content['id'] for email in received_emails):
                    received_emails.append(email_content)
            time.sleep(1)  # Check every second
        except Exception as e:
            print(f"Error in email listener: {str(e)}")
            time.sleep(5)  # Wait before retrying

@app.route('/start_listening', methods=['POST'])
def start_listening():
    """Start listening for new emails."""
    global listener_thread, is_listening
    try:
        if is_listening:
            return jsonify({"message": "Already listening for new emails"}), 200

        if not current_email:
            return jsonify({"error": "No email address registered. Please register an email first."}), 400

        is_listening = True
        # Start the listener in a separate thread
        listener_thread = threading.Thread(target=email_listener)
        listener_thread.daemon = True  # Thread will terminate when the main app stops
        listener_thread.start()

        return jsonify({"message": "Started listening for new emails"})
    except Exception as e:
        is_listening = False
        return jsonify({"error": f"Failed to start listening: {str(e)}"}), 500

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    """Stop listening for new emails."""
    global is_listening, listener_thread
    try:
        if not is_listening:
            return jsonify({"message": "Not currently listening for emails"}), 200

        is_listening = False
        if listener_thread:
            listener_thread = None
        return jsonify({"message": "Stopped listening for emails"})
    except Exception as e:
        return jsonify({"error": f"Failed to stop listening: {str(e)}"}), 500

@app.route('/get_emails', methods=['GET'])
def get_emails():
    """Fetch all received emails."""
    if not received_emails:
        return jsonify({"message": "No emails received yet."})
    
    # Sort emails by timestamp (newest first)
    sorted_emails = sorted(received_emails, key=lambda x: x['timestamp'], reverse=True)
    return jsonify(sorted_emails)

@app.route('/delete_email/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    """Delete a specific email by ID."""
    global received_emails
    try:
        # Find and remove the email with the given ID
        initial_length = len(received_emails)
        received_emails = [email for email in received_emails if email['id'] != email_id]
        
        if len(received_emails) < initial_length:
            return jsonify({"message": "Email deleted successfully"})
        else:
            return jsonify({"error": "Email not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete email: {str(e)}"}), 500

@app.route('/clear_emails', methods=['POST'])
def clear_emails():
    """Clear all received emails."""
    global received_emails
    try:
        received_emails = []
        return jsonify({"message": "All emails cleared successfully"})
    except Exception as e:
        return jsonify({"error": f"Failed to clear emails: {str(e)}"}), 500

@app.teardown_appcontext
def cleanup(exception=None):
    """Cleanup resources when the app shuts down."""
    global is_listening
    if is_listening:
        stop_listening()
    if email_client:
        try:
            email_client.stop()
        except Exception as e:
            print(f"Error stopping email client: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
