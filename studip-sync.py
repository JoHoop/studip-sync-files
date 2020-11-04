import requests, io, zipfile, os, configparser
from lxml import html
from bs4 import BeautifulSoup as Bs

login_url = 'https://elearning.uni-bremen.de/index.php?again=yes'
course_url = 'https://elearning.uni-bremen.de/dispatch.php/course/files?cid='

cfg = configparser.ConfigParser()
script_path = os.path.dirname(os.path.abspath(__file__))
cfg.read(os.path.join(script_path,'config.ini'))
try:
    user = cfg.get('settings', 'user')
    password = cfg.get('settings', 'password')
    path = cfg.get('settings', 'data_folder')   
except Exception as e:
    print('error parsing config file')
    print(e)

print('starting session')
session = requests.Session()
login_response = session.get(login_url)
login_page = Bs(login_response.content, 'html.parser')

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

for course in cfg.items('courses'):
    file_target = os.path.join(path, course[0])
    download_url = course_url + course[1]
    print('finding course',course[0],'with cid:',course[1])

    download_page = session.get(download_url)
    
    parsed_content = Bs(download_page.content, 'html.parser')
    security_token = parsed_content.find('input', {'name':'security_token'}).attrs['value']
    parent_folder_id = parsed_content.find('input', {'name':'parent_folder_id'})
    post_url = parsed_content.find('form', {'method': 'post'}).attrs['action']

    print('extracting token')

    token = {}
    token['security_token'] = security_token
    token['parent_folder_id'] = '81d65fb167cc56cff42e8e9f29a6ab0c'
    token['ids[]'] = ['8c54f3199fbb3db4d983111297467017', '72a64f3ae8daec098670592deabcd31a', '4cdce89850aa14b2c8d42b3a6d288da6', '1cfde817c0060d0618ab6384902b8649']
    token['download'] = ''

    print('requesting download')
    r = session.post(post_url, data=token)
    if(r.status_code != 200):
        print('request failed')

    #p = Bs(r.content, 'html.parser')
    #file = open('response.html', 'w')
    #file.write(p.prettify())
    #file.close()

    z = zipfile.ZipFile(io.BytesIO(r.content))
    print('extracting zip')
    z.extractall(file_target)
    print('done')