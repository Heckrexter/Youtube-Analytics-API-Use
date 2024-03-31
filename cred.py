import sqlite3
import datetime

# initialize the database
def credstart():
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS cred(channel_name, refresh_token, token_uri, client_id, client_secret, scopes, create_date, UNIQUE(token_uri, channel_name))")
    conn.close()

# acc credentials
def credadd(name,string):
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    scope = string['scopes']
    scope2 = ""
    for i in range(0,len(scope)):
        scope2 += scope[i]
        if i != len(scope) - 1:
            scope2 += ","
    datestring = f"{datetime.date.today()}"
    cur.execute(f"INSERT OR IGNORE INTO cred VALUES ('{name}', '{string['refresh_token']}', '{string['token_uri']}', '{string['client_id']}', '{string['client_secret']}', '{scope2}','{datestring}')")
    conn.commit()
    conn.close()

# delete all credentials
def creddelete():
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM cred")
    conn.commit()
    conn.close()

# get all credentials
def credget():
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cred")
    output = cur.fetchall()
    if len(output) == 0:
        return {}
    conn.close()
    outputdict = []
    for i in output:
        outputdict.append({
            'channel_name': i[0],
            'refresh_token': i[1],
            'token_uri': i[2],
            'client_id': i[3],
            'client_secret': i[4],
            'scopes': i[5].split(',')
        })
    return outputdict

# get specific credentials
def credtget(string):
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM cred WHERE refresh_token = '{string}'")
    output = cur.fetchall()
    conn.close()
    outputdict = []
    output = output[0]
    outputdict = {
        'channel_name': output[0],
        'refresh_token': output[1],
        'token_uri': output[2],
        'client_id': output[3],
        'client_secret': output[4],
        'scopes': output[5].split(',')
    }
    return outputdict

# check if refresh token is older than 7 days
def credcheck():
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cred")
    output = cur.fetchall()
    if len(output) == 0:
        print("empty database")
        return
    for i in output:
        stringa = i[6]
        date = stringa[0:4] + stringa[5:7] + stringa[8:10]
        date = int(date)
        if date < (date-7):
            print("deleting")
            cur.execute(f"DELETE FROM cred WHERE refresh_token = {i[1]}")
            conn.commit()
    print("done checking")
    conn.close()

# delete specific credentials
def credtdel(string):
    conn = sqlite3.connect('cred.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM cred WHERE refresh_token = '{string}'")
    conn.commit()
    conn.close()