# Steps: https://firebase.google.com/docs/admin/setup
# 1. Add the firebase admin sdk
# 2. Set GOOGLE_APPLICATION_CREDENTIALS environment variable (path to the JSON file containing the service account key)
# 3. Run this script

import firebase_admin
from firebase_admin import messaging

#initialize firebase admin
default_app = firebase_admin.initialize_app()

# The topic name can be optionally prefixed with "/topics/".
topic = 'hjtopic'

# See documentation on defining a message payload.
message = messaging.Message(
    data = {
        'click_action': 'FLUTTER_NOTIFICATION_CLICK',
        'key': 'hijackKey'
    },
    notification = messaging.Notification(
    	title = 'Active Hijack detected!',
    	body = 'Tap to view more'
    ),
    topic=topic,
)

# Send a message to the devices subscribed to the provided topic.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)