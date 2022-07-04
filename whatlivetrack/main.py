# import the required libraries
from codecs import decode
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import sys
import hashlib
import pywhatkit
import json
sys.stdout.reconfigure(encoding='utf-8')

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails():
	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	creds = None

	# The file token.pickle contains the user access token.
	# Check if it exists
	if os.path.exists('token.pickle'):

		# Read the token from the file and store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If credentials are not available or are invalid, ask the user to log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the Gmail API
	service = build('gmail', 'v1', credentials=creds)

	# request a list of all the messages
	result = service.users().messages().list(userId='me', q='noreply@garmin.com', maxResults=1).execute()

	# We can also pass maxResults to get any number of emails. Like this:
	# result = service.users().messages().list(maxResults=200, userId='me').execute()
	messages = result.get('messages')

	# messages is a list of dictionaries where each dictionary contains a message id.

	# iterate through all the messages
	for msg in messages:
		# Get the message from its id
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()

		# Use try-except to avoid any Errors
		try:
			# Get value of 'payload' from dictionary 'txt'
			payload = txt['payload']
			headers = payload['headers']

			# Look for Subject and Sender Email in the headers
			for d in headers:
				if d['name'] == 'Subject':
					subject = d['value']
				if d['name'] == 'From':
					sender = d['value']

			# The Body of the message is in Encrypted format. So, we have to decode it.
			# Get the data and decode it with base 64 decoder.
			parts = payload.get('parts')
			data = None
			if parts:
				data = parts[0]['body']['data']
			else:
				data = payload.get('body')['data']
			data = data.replace("-","+").replace("_","/")
			decoded_data = base64.b64decode(data)

			# Now, the data obtained is in lxml. So, we will parse
			# it with BeautifulSoup library
			url_start_idx = decoded_data.find(b'https://livetrack.garmin.com/')
			str_data = decoded_data[url_start_idx:url_start_idx+1024].decode('utf-8')
			# This could use regex instead
			url_end_idx = 1
			while str_data[url_end_idx] != '\"':
				url_end_idx += 1

			live_track_url = str_data[:url_end_idx]
			print(live_track_url)
   
			# 37
			session_id = live_track_url[37:73]
			token = live_track_url[80:]
   
			hs = hashlib.sha256((session_id + token).encode('utf-8'), usedforsecurity=False).hexdigest()
			fresh_live_track = False

			if os.path.exists('last_session.sha'):
				with open('last_session.sha', 'r+') as f:
					stored_hs = f.read()

					# Got new live track e-mail
					if stored_hs != hs:
						f.seek(0)
						f.write(hs)
						f.truncate()
						fresh_live_track = True
			else:
				with open('last_session.sha', 'w') as f:
					f.write(hs)

				# Got new live track e-mail
				fresh_live_track = True

			# Send whatsapp message
			if fresh_live_track:
				numbers = {}
				with open('contacts.json') as c:
					numbers = json.load(c)

				print(numbers.values())
       
				for phone_no in numbers.values():
					try:
						pywhatkit.sendwhatmsg_instantly(phone_no, live_track_url, 15, True, 4)
					except:
						pass
			

		except KeyboardInterrupt:
			pass

if __name__ == '__main__':
	getEmails()
