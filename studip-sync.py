import configparser
import io
import os
import re
import requests
import zipfile
from bs4 import BeautifulSoup
import threading
from dataclasses import dataclass
from glob import glob

@dataclass
class FileInfo:
    """A file from StudIP.
    
    Attributes:
        file_id: The Stud.IP internal file ID.
        name: The filename.
        path: A list of the parent folders of this file."""
    file_id: str
    name: str
    path: list[str]


login_url = 'https://elearning.uni-bremen.de/index.php?again=yes'
course_url = 'https://elearning.uni-bremen.de/dispatch.php/course/files?cid='
files_flat_url = 'https://elearning.uni-bremen.de/dispatch.php/course/files/flat?cid='

cfg = configparser.ConfigParser()
script_path = os.path.dirname(os.path.abspath(__file__))
cfg.read(os.path.join(script_path, 'config.ini'))
try:
    user = cfg.get('settings', 'user')
    password = cfg.get('settings', 'password')
    path = cfg.get('settings', 'data_folder')
    new_only = cfg.getboolean('settings', 'new_only')
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
    
    print(f'{course[0]} : fetching file information')

    file_infos: list[FileInfo] = []

    def get_files_recursively(url: str, path: list[str] = []):
        files_page = BeautifulSoup(session.get(url, data={
            'security_token': security_token,
        }).content, 'html.parser')

        tbody_subfolders = files_page.find('tbody', attrs={'class': 'subfolders'})

        if tbody_subfolders != None:
            for subfolder_row in tbody_subfolders.find_all('tr'):
                if subfolder_row.has_attr('class') and 'empty' in subfolder_row['class']:
                    continue
                    
                anchor = subfolder_row.find_all('td')[2].find('a')

                new_path = path.copy()
                new_path.append(anchor.string.strip())

                get_files_recursively(anchor['href'], new_path)

        tbody_files = files_page.find('tbody', attrs={'class': 'files'})

        if tbody_files != None:
            for file_row in tbody_files.find_all('tr', id=re.compile(r'^fileref_')):
                file_id = re.match(r'^fileref_(.+)', file_row['id']).group(1)
                filename = file_row.find_all('td')[2]['data-sort-value']

                if (not new_only) or (not os.path.exists(os.path.join(file_target, *path, filename))):
                    file_infos.append(FileInfo(file_id, filename, path))


    get_files_recursively(download_url)

    print(f'{course[0]} : found {len(file_infos)} new file(s)')

    if len(file_infos) == 0:
        return

    
    files_flat_content = session.get(files_flat_url + course[1], data = {
        'security_token': security_token
    }).content

    files_flat_page = BeautifulSoup(files_flat_content, 'html.parser')
    
    post_url = files_flat_page.find('form', attrs={'method': 'post', 'action': re.compile(
        '^https://elearning.uni-bremen.de/dispatch.php/file/bulk/')}).attrs['action']

    token = {}
    token['security_token'] = security_token
    token['ids[]'] = [file.file_id for file in file_infos]
    token['download'] = ''

    print(course[0], ': requesting download')
    r = session.post(post_url, data=token)
    if (r.status_code != 200):
        print(course[0], ': request failed')

    # if only one file is downloaded, it will not be a zip file
    if len(file_infos) > 1:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print(course[0], ': extracting zip')
        z.extractall(file_target)
    else:
        with open(os.path.join(file_target, file_infos[0].name), 'wb') as file:
            file.write(r.content)

    for root, dirs, files in os.walk(file_target):
        for file in files:
            if file == "archive_filelist.csv":
                os.remove(os.path.join(root, file))
                continue

            filename = os.path.join(root, file)
            os.replace(filename, os.path.join(root, re.sub('^\[\d+\]_', '', file)))

    print(course[0], ': cleaned files')

    print(f'{course[0]} : moving files into subfolders')

    for fileinfo in file_infos:
        # create the directories if they don't exist
        os.makedirs(os.path.join(file_target, *fileinfo.path), exist_ok=True)

        # move the files into their subfolders
        try:
            os.rename(
                os.path.join(file_target, fileinfo.name),
                os.path.join(file_target, *fileinfo.path, fileinfo.name)
            )
        except:
            print(f'{course[0]} : failed to move file {fileinfo.name}, skipping file')

for course in cfg.items('courses'):
    threading.Thread(target=getfiles, args=(course,)).start()

