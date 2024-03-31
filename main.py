import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import flask
import cred
import requests
from extrafunc import credtodict, formatresa

app = flask.Flask(__name__)
app.secret_key = "There is a placeholder here"

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
          'https://www.googleapis.com/auth/yt-analytics.readonly',
          'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
          'https://www.googleapis.com/auth/userinfo.profile'
          ]  
API_SERVICE_NAME1 = 'youtubeAnalytics'
API_VERSION1 = 'v2'
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

# printing results
@app.route('/result')
def testfun():
    halfcred = flask.session['cred']
    if 'cred' not in flask.session:
        return flask.redirect(flask.url_for("home"))
    data = {
        "client_id": halfcred['client_id'],
        "client_secret": halfcred['client_secret'],
        "refresh_token": halfcred['refresh_token'],
        "grant_type": "refresh_token"
    }
    response = requests.post("https://oauth2.googleapis.com/token", data=data)
    new_tokens = response.json()
    new_access_token = new_tokens.get("access_token")
    
    newcred = {
        'client_id': halfcred['client_id'],
        'client_secret': halfcred['client_secret'],
        'refresh_token': halfcred['refresh_token'],
        'scopes': halfcred['scopes'],
        'token_uri': halfcred['token_uri'],
        'token': new_access_token
    }
    credentials = google.oauth2.credentials.Credentials(**newcred)
    youtube = build(
        API_SERVICE_NAME1, API_VERSION1, credentials=credentials
    )
    metrica = flask.session['selected_metrics']
    metric = ""
    for i in range(0,len(metrica)):
        metric += metrica[i]
        if i != len(metrica) - 1:
            metric += ","
    report = youtube.reports().query(
        endDate='2024-07-14', 
        ids='channel==MINE', 
        metrics = metric,
        startDate='2016-05-13'
        ).execute()
    Results = formatresa(report)
    
    # Enable the following comment if you want to return a json file instead
    # return flask.jsonify(**report)
    return flask.render_template("result.html", Results = Results)

# Oauth page 1
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

# Oauth page 2
@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    auth_response = flask.request.url
    flow.fetch_token(authorization_response=auth_response)
    
    credentials = flow.credentials
    youtube = build('youtube', 'v3', credentials=credentials)
    request = youtube.channels().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    if response['items']:
        channel_name = response['items'][0]['snippet']['title']
    else:
        channel_name = "No channel found"
    cred.credadd(channel_name, credtodict(credentials))
    return flask.redirect(flask.url_for("home"))

# Set account for use
@app.route('/acc', methods=['GET'])
def acc():
    query_param = flask.request.args.get('q', '')
    halfcred = cred.credtget(query_param)
    data = {
        "client_id": halfcred['client_id'],
        "client_secret": halfcred['client_secret'],
        "refresh_token": halfcred['refresh_token'],
        "grant_type": "refresh_token"
    }
    newcred = {
        'client_id': halfcred['client_id'],
        'client_secret': halfcred['client_secret'],
        'refresh_token': halfcred['refresh_token'],
        'scopes': halfcred['scopes'],
        'token_uri': halfcred['token_uri'],
    }
    flask.session['cred'] = newcred
    return flask.redirect(flask.url_for("selmet"))

# Home page
@app.route("/")
def home():
    return flask.render_template("index.html",Users = cred.credget())

# select metrics
@app.route('/selmet')
def selmet():
    return flask.render_template("selmet.html", Metrics= METRICS)

# select metrics request
@app.route('/selmetreq', methods=['GET'])
def selmetreq():
    selected_metrics = flask.request.args.getlist('metric[]')
    flask.session['selected_metrics'] = selected_metrics
    return flask.redirect(flask.url_for("testfun"))

# logout selected user
@app.route('/logout', methods=['GET'])
def logout():
    query_param = flask.request.args.get('q', '')
    cred.credtdel(query_param)
    return flask.redirect(flask.url_for("home"))

# initialize webapp
if __name__ == '__main__':
    cred.credstart()
    cred.credcheck()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host="localhost", port=8080, debug=True)