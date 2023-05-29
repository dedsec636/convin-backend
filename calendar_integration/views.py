from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
from rest_framework.response import Response
from rest_framework.views import APIView
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['google_auth_state'] = state
        return redirect(authorization_url)

#@api_view(('GET',))
class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        state = request.session.pop('google_auth_state', None)
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            state=state
        )
        flow.fetch_token(
            authorization_response=request.build_absolute_uri()
        )
        credentials = flow.credentials

        # The access token is available in the 'credentials' object
        access_token = credentials.token

        # Use the access token to create a Calendar API client
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

        # Call the 'events' API to retrieve the list of events
        events_result = service.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])
        
        return Response({"events":events})
        #return HttpResponse("Events retrieved successfully.")

