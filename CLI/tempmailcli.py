import random
import string
from mailtm import Email

def listener(message):
    print("\nSubject: " + message['subject'])
    print("Content: " + message['text'] if message['text'] else message['html'])

# Get Domains
test = Email()
print("\nDomain: " + test.domain)

# Allow user to input custom name for the email address
custom_name = input("\nEnter custom email name: ")

# Generate a random suffix to make the email unique
random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Combine custom name and the random suffix
unique_email_name = custom_name + random_suffix

# Make new email address with the custom name and random suffix
test.register(unique_email_name)
print("\nEmail Address: " + str(test.address))

# Start listening
test.start(listener, interval=1)
print("\nWaiting for new emails...")
