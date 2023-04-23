## Google Calendar Integration - Django Rest Framework

I have implemented google calendar integration using django rest api. OAuth2.0 mechanism is used to get users calendar access. Below are details of API endpoints and corresponding views that are implemented - 

```
/rest/v1/calendar/init/ -> GoogleCalendarInitView()
```
This view starts step 1 of the OAuth which will prompt user for his/her credentials.

```
/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
```
This view will do two things
1. Handle redirect request sent by google with code for token
2. Using the access_token, get list of events in users calendar

To run this project on a local machine: 

```sh
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client djangorestframework
 ```

### Note: This application must have authorization credentials that identify the application to Google's OAuth 2.0 server to access Google APIs

## References

| Resource |
| ------ | 
| [Google Identity: Using OAuth 2.0 for Web Server Applications][PlDb] | 
| [Google Calendar API][PlGh] |

[PlDb]: <https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-code>
[PlGh]: <https://developers.google.com/calendar/api/v3/reference>
 