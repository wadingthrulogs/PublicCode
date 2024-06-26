import requests
import json
from time import sleep
# This script is used to pull files from Carbon Black. It is used to pull files from a host that is being monitored by Carbon Black.


url = "https://defense-prod05.conferdeploy.net/appservices/v6/orgs/{org_id}/liveresponse/sessions"
# Header used for get_session_id and get_file_id
# ADD API KEY HERE
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Auth-Token": "[API Secret Key]/[API ID]",
}
# Header used for get_file_content
# ADD API KEY HERE
headers_auth = {
    "X-Auth-Token": "API/API",
}
#name of the command used, path of tile, Where to start pulling for bytes, number of bytes allowed to pull.
#No issues seen by Carbon black on pulling files less the on gb
cmd = {
    "name": "get file",
    #"path": "C:/windows/system32/mousocoreworker.exe",
    "path": "",
    "offset": 0,
    "get_count": 10000000000000
}
#device ID used for get_session_id
data = {
  "device_id": ''
}
deviceid = input('please insert the device id: ')
target_file = input('please insert target file path and name: ')
data['device_id']=deviceid
cmd['path']=target_file
#Checking the status of the session to make sure it is active
def check_session_status():
    r = requests.post(url, headers=headers, data=json.dumps(data))
    status = json.loads(r.content)['status']
    print('Session Status:' + status)
    return status
# Establishing the session id to connect to host via carbon black. This session id is used a lot.
def get_session_id():
    r = requests.post(url, headers=headers, data=json.dumps(data))
    session_id = json.loads(r.content)['id']
    status = json.loads(r.content)['status']
    return session_id
# performing 'get file' command. This allows us to get the file ID for the file requested which it will be used in get_file_content.
# It also preps carbon black for us grabing the file.
def get_file_id():
    session_id = get_session_id()
    status = check_session_status()
    while status != 'ACTIVE':
        sleep(10)
        status = check_session_status()
    url = f"https://defense-prod05.conferdeploy.net/appservices/v6/orgs/{org_id}/liveresponse/sessions/{session_id}/commands"
    r = requests.post(url, headers=headers, data=json.dumps(cmd))
    # print(r.status_code)
    # print(json.loads(r.content)['file_details']['file_id'])
    print(json.loads(r.content))
    status = json.loads(r.content)['status']
    print('file:'+ status)
    file_id = (json.loads(r.content)['file_details']['file_id'])
    return file_id
# Pulling the actual file from the server. This is a redirct.
#I name the file using the session_id.
def get_content():
    session_id = get_session_id()
    file_id = get_file_id()
    url = f"https://defense-prod05.conferdeploy.net/appservices/v6/orgs/{org_id}/liveresponse/sessions/{session_id}/files/{file_id}/content"
    r = requests.get(url, headers=headers_auth, allow_redirects=True)
    print(r.url)
    #print(r.content)
    f = open(f'./{file_id}.file', 'wb')
    f.write(r.content)
    f.close()