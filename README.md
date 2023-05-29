## Google Calendar API OAuth 2.0  - Django Rest Framework

Problem: In this assignment you have to implement google calendar integration using django rest api. 
You need to use the OAuth2 mechanism to get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement



- Endpoint:
```
/rest/v1/calendar/init/ -> google_calendar_init_view()
```
This view should start step 1 of the OAuth. Which will prompt user for his/her credentials

```
/rest/v1/calendar/redirect/ -> google_calendar_redirect_view()
```

## Sample output
![](sample.png)

This view will do two things
1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar

### Note: To run this assignment need google account credentials which need to save in the project directory and add a redirect URL in your google cloud. 