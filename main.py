import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import flask

app = flask.Flask(__name__)
app.secret_key = "There is a placeholder here"

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
          'https://www.googleapis.com/auth/yt-analytics.readonly'
          ]  
API_SERVICE_NAME1 = 'youtubeAnalytics'
API_VERSION1 = 'v2'
API_SERVICE_NAME2 = "youtubereporting"
API_VERSION2 = 'v1'
METRICS = [
    "views",
    "redViews",
    "comments",
    "likes",
    "dislikes",
    "videosAddedToPlaylists",
    "videosRemovedFromPlaylists",
    "shares",
    "estimatedMinutesWatched",
    "estimatedRedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "annotationClickThroughRate",
    "annotationCloseRate",
    "annotationImpressions",
    "annotationClickableImpressions",
    "annotationClosableImpressions",
    "annotationClicks",
    "annotationCloses",
    "cardClickRate",
    "cardTeaserClickRate",
    "cardImpressions",
    "cardTeaserImpressions",
    "cardClicks",
    "cardTeaserClicks",
    "subscribersGained",
    "subscribersLost"
]

@app.route('/test')
def testfun():
    if 'credentials' not in flask.session:
        return flask.redirect('oauth')
    credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
    youtube = build(
        API_SERVICE_NAME1, API_VERSION1, credentials=credentials
    )
    metric = ""
    for i in range(0,len(METRICS)):
        metric += METRICS[i]
        if i != len(METRICS) - 1:
            metric += ","
            
    print("METRIC:"+metric)
    
    report = youtube.reports().query(
        endDate='2024-07-14', 
        ids='channel==MINE', 
        metrics = metric,
        startDate='2016-05-13'
        ).execute()
    
    flask.session['credentials'] = credtodict(credentials)
    return flask.jsonify(**report)
    


@app.route('/oauth')
def oauth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    
    auth_url,state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    flask.session['state'] = state
    
    return flask.redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    
    auth_response = flask.request.url
    flow.fetch_token(authorization_response=auth_response)
    
    credentials = flow.credentials
    flask.session['credentials']  = credtodict(credentials)
    
    return flask.redirect(flask.url_for("testfun"))
    
    return


@app.route("/")
def home():
    return """
    <p><button><a href="/oauth">Authorize</a></button>  Authorize directly</p>
    <p><button><a href="/test">Access</a></button>  Access the metrics json</p>
    """
    
def credtodict(cred):
    return {
        'token': cred.token,
        'refresh_token': cred.refresh_token,
        'token_uri': cred.token_uri,
        'client_id': cred.client_id,
        'client_secret': cred.client_secret,
        'scopes': cred.scopes
    }

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host="localhost", port=8080, debug=True)