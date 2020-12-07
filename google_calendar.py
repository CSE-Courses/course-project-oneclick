from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from database import usersDatabase

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(email):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_str = str(start)
        time_arr = start_str.split('T')
        hour_str = time_arr[1]
        date_str = time_arr[0]
        new_hour_arr = hour_str.split(':')
        hour_str = new_hour_arr[0]
        min_str = new_hour_arr[1]

        start_time = hour_str + ':' + min_str + ':00'
        hour = int(hour_str)
        if hour_str == '23':
            hour_str = '00'
        else:
            hour_str = str(hour + 1)
        end_time = hour_str + ':' + min_str + ':00'

        usersDatabase.add_user_info(email, event['summary'], 'No Link', 'No Description', date_str, start_time, end_time)

        #print(start, event['summary'])
        #print(event['summary'])
        #print("   Date: ", date_str)
        #print("   Start Time: ", start_time)
        #print("   End Time: ", end_time)
        #print("   Minute: ", min_str)
