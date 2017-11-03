import requests
import io
import zipfile
import os
import json, configparser
from bs4 import BeautifulSoup as Bs

url_start = 'https://elearning.uni-bremen.de/index.php?again=yes'
url_course_0 = 'https://elearning.uni-bremen.de/folder.php?cid='
url_course_checkall = '&data%5Bcmd%5D=all&check_all=TRUE'

url_course_new = '&data%5Bcmd%5D=all&zipnewest='


#
#iphysiclink = 'https://elearning.uni-bremen.de/folder.php?cid=fd0aff595c7bcb432b3268534319241b&cmd=all'
#allactive = 'https://elearning.uni-bremen.de/folder.php?cid=fd0aff595c7bcb432b3268534319241b&data%5Bcmd%5D=all&check_all=TRUE'
#downloadnew = 'https://elearning.uni-bremen.de/folder.php?cid=fd0aff595c7bcb432b3268534319241b&data%5Bcmd%5D=all&zipnewest=1509301660'
#downloadall = 'https://elearning.uni-bremen.de/folder.php?cid=d394384404fa1587ea1001edee7d50a2&data%5Bcmd%5D=all&zipnewest=0000000000'
#timestamp -> its unix timestamp
#r_start = requests.get('https://elearning.uni-bremen.de/', auth=(user, password))

cfg = configparser.ConfigParser()
script_path = os.path.dirname(os.path.abspath(__file__))
cfg.read(os.path.join(script_path,'config.ini'))
try:
    user = cfg.get('settings', 'user')
    password = cfg.get('settings', 'password')
    path = cfg.get('settings', 'data_folder')
    timestamp = cfg.get('settings', 'timestamp')
except Exception as e:
    print('error parsing config file')
    print(e)

#start the session
session = requests.Session()
r_start = session.get(url_start)
p_start = Bs(r_start.content, 'html.parser')
#login
inputs = p_start.form.find_all('input')
data = {}
for field in inputs:
    try:
        data[field['name']] = field['value']
    except:
        print('no value attribute')
data['loginname'] = user
data['password'] = password
r_front = session.post(url_start, data=data)
p_front = Bs(r_front.content, 'html.parser')
print(p_front.prettify())

for course in cfg.items('courses'):
    print(course)
    target = os.path.join(path, course[0])
    #url_load = url_course_0 + course[1] + url_course_1
    url_load = url_course_0 + course[1] + url_course_new + timestamp
    print(url_load)
    r_load = session.get(url_load)
    zfile = zipfile.ZipFile(io.BytesIO(r_load.content))
    zfile.extractall(target)

    #p_load = Bs(r_load.content, 'html.parser')
    #print(p_load.prettify())
