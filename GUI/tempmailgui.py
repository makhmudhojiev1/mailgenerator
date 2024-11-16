import tkinter as tk
from tkinter import messagebox
from mailtm import Email
import random
import string

# Initialize the Email object
email_client = Email()

def get_domain():
    domain = email_client.domain
    domain_label.config(text=f"Domain: {domain}")
    messagebox.showinfo("Domain Retrieved", f"Domain: {domain}")

def generate_random_string(length=8):
    """Generate a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def register_email():
    custom_name = email_name_entry.get()
    if custom_name:
        # Generate a custom email with a random string appended to it
        unique_name = custom_name + generate_random_string()
        email_client.register(unique_name)  # Register with the custom name
        email_label.config(text=f"Email Address: {email_client.address}")
        copy_button.config(state=tk.NORMAL)  # Enable the copy button after generating the email
        messagebox.showinfo("Email Created", f"Email Address: {email_client.address}")
    else:
        messagebox.showwarning("Input Error", "Please enter a custom email name.")

def copy_email():
    app.clipboard_clear()
    app.clipboard_append(email_client.address)
    app.update()  # Keeps the clipboard content even after the app closes
    messagebox.showinfo("Copied", "Email Address copied to clipboard!")

def start_listening():
    def listener(message):
        output_text = f"\nSubject: {message['subject']}\nContent: {message['text'] if message['text'] else message['html']}"
        text_box.insert(tk.END, output_text)
        text_box.insert(tk.END, "\n" + "-"*50 + "\n")

    email_client.start(listener, interval=1)
    messagebox.showinfo("Listening Started", "Listening for new emails...")

# Set up the GUI
app = tk.Tk()
app.title("MailTM GUI")

# Domain button and label
domain_button = tk.Button(app, text="Get Domain", command=get_domain)
domain_button.pack(pady=5)

domain_label = tk.Label(app, text="Domain: ")
domain_label.pack(pady=5)

# Entry for custom email name
email_name_label = tk.Label(app, text="Enter Custom Email Name: ")
email_name_label.pack(pady=5)

email_name_entry = tk.Entry(app, width=30)
email_name_entry.pack(pady=5)

# Register email button and label
email_button = tk.Button(app, text="Register Email", command=register_email)
email_button.pack(pady=5)

email_label = tk.Label(app, text="Email Address: ")
email_label.pack(pady=5)

# Copy email button
copy_button = tk.Button(app, text="Copy Email", command=copy_email, state=tk.DISABLED)
copy_button.pack(pady=5)

# Start listening button
listen_button = tk.Button(app, text="Start Listening", command=start_listening)
listen_button.pack(pady=5)

# Text box for email output
text_box = tk.Text(app, width=60, height=20, wrap=tk.WORD)
text_box.pack(pady=10)

# Run the GUI application
app.mainloop()
