from django.shortcuts import redirect
import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from rest_framework.response import Response
 
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

# This file contains the OAuth 2.0 information for this application, including its client_id and client_secret
CLIENT_SECRETS_FILE = "C:/Users/Asus/Documents/Convin Task/Code/backend_task/rest_api/credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection and REDIRECT URL
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']

REDIRECT_URL = 'http://localhost:8000/rest/v1/calendar/redirect'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@api_view(['GET'])
def GoogleCalendarInitView(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs for the OAuth 2.0 client (GCP Project)
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true'
        )

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return Response({"Click to authorize": authorization_url})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    # Specify the state when creating the flow in the callback so that it can verified in the authorization server response.
    state = request.session['state']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)


    # Save credentials back to session in case access token was refreshed
    credentials = flow.credentials
    request.session['credentials'] =    {'token': credentials.token,
                                        'refresh_token': credentials.refresh_token,
                                        'token_uri': credentials.token_uri,
                                        'client_id': credentials.client_id,
                                        'client_secret': credentials.client_secret,
                                        'scopes': credentials.scopes}

    # Check if credentials are in session
    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

    # Here builds build client libraries, IDE plugins, and other tools that interact with Google APIs 
    # calendar API v3 using credentials built using OAuth2.0 flow
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)   

    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']
    events = service.events().list(calendarId=calendar_id, maxResults=10).execute()

    if not events['items']:
        return Response({'message': 'No data found or user credentials invalid'})
    else:
        return Response({'events': events['items']})
