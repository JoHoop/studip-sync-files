import configparser
import io
import os
import re
import requests
import zipfile
from bs4 import BeautifulSoup
import threading

login_url = 'https://elearning.uni-bremen.de/index.php?again=yes'
course_url = 'https://elearning.uni-bremen.de/dispatch.php/course/files?cid='
newest_url = 'https://elearning.uni-bremen.de/dispatch.php/course/files/newest_files?cid='

cfg = configparser.ConfigParser()
script_path = os.path.dirname(os.path.abspath(__file__))
cfg.read(os.path.join(script_path, 'config.ini'))
try:
    user = cfg.get('settings', 'user')
    password = cfg.get('settings', 'password')
    path = cfg.get('settings', 'data_folder')
    new_only = cfg.get('settings', 'new_only')
except Exception as e:
    print('error parsing config file')
    print(e)
print("Config Loaded!")

print('starting session')
session = requests.Session()
login_response = session.get(login_url)
login_page = BeautifulSoup(login_response.content, 'html.parser')

inputs = login_page.form.find_all('input')
data = {}
for i in inputs:
    try:
        data[i['name']] = i['value']
    except:
        print('no value attribute')
data['loginname'] = user
data['password'] = password
r = session.post(login_url, data=data)
if(r.status_code == 200):
    print('login successful')
else:
    print('login failed')

def getfiles(course):
    file_target = os.path.join(path, course[0])
    download_url = course_url + course[1]
    print('finding course', course[0], '(', course[1], ')')

    download_page = session.get(download_url)

    parsed_content = BeautifulSoup(download_page.content, 'html.parser')

    print(course[0], ': extracting post parameters')
    security_token = parsed_content.find('input', attrs={'type': 'hidden', 'name': 'security_token'}).attrs['value']
    parent_folder_id = parsed_content.find('input', attrs={'type': 'hidden', 'name': 'parent_folder_id'}).attrs['value']
    post_url = parsed_content.find('form', attrs={'method': 'post', 'action': re.compile(
        '^https://elearning.uni-bremen.de/dispatch.php/file/bulk/')}).attrs['action']
    checkboxes = parsed_content.find_all('input',
                                         attrs={'class': 'studip-checkbox', 'type': 'checkbox', 'name': 'ids[]',
                                                'id': re.compile('^file_checkbox_')})
    ids = list(map(lambda c: c.attrs['value'], checkboxes))

    token = {}
    token['security_token'] = security_token
    token['parent_folder_id'] = parent_folder_id
    token['ids[]'] = ids
    token['download'] = ''

    if (new_only == 'yes'):
        post_url = newest_url + course[1]
        token = {}

    print(course[0], ': requesting download')
    r = session.post(post_url, data=token)
    if (r.status_code != 200):
        print(course[0], ': request failed')

    z = zipfile.ZipFile(io.BytesIO(r.content))
    print(course[0], ': extracting zip')
    z.extractall(file_target)

    for root, dirs, files in os.walk(file_target):
        for file in files:
            if file == "archive_filelist.csv":
                os.remove(os.path.join(root, file))
                continue

            filename = os.path.join(root, file)
            os.replace(filename, os.path.join(root, re.sub('^[+[0-9]+]_', '', file)))

    print(course[0], ': cleaned files')

for course in cfg.items('courses'):
    threading.Thread(target=getfiles, args=(course,)).start()

