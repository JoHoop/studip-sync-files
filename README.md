# studip-sync-files
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
A python script for downloading files from your studip courses. It's designed
to run for the studip platform of the university of bremen: 
https://elearning.uni-bremen.de
But it should be possible to move this to any studip installation by changing
the urls.
This version is using Multi-Threading to download, extract & clean all 
files from your courses at the same time.

## Setup
It's just a script no GUI or service files yet. To run it you need to have
installed python3 with the requests and beatifulsoup4 modules, thats all.

All settings are done via the config.ini file. It's editable with andy text
editor in windows and linux. It has to be in the same directory as the
studip-sync.py file or the script file must be edited to the correct path of
the config.ini. Replace `studip_username` and `studip_password` in the
config.ini with your login.
The path can be relative (to python workdir) or absolute.

## Courses
In the courses section add the courses you want to download files from.
You need to have permission to download the files otherwise the script won't
work.

To add a course set a name (this is the subfolder the script creates to
organize the courses files) and the course id (cid), which is the long number in the
url (at the course page: https://elearning.uni-bremen.de/dispatch.php/course/overview?cid=847b6d81388cd9742f31bdc363507bbc) like this:

```subfolder_name = 847b6d81388cd9742f31bdc363507bbc```

## Usage
Run the script by double click or from the command line.

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/JoHoop"><img src="https://avatars.githubusercontent.com/u/67421398?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jo</b></sub></a></td>
    <td align="center"><a href="https://github.com/jnthn-b"><img src="https://avatars.githubusercontent.com/u/15343360?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jonathan Bröring</b></sub></a></td>
    <td align="center"><a href="https://github.com/Schlaurens"><img src="https://avatars.githubusercontent.com/u/50379551?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Laurens S.</b></sub></a></td>
    <td align="center"><a href="https://github.com/tomdolhs"><img src="https://avatars.githubusercontent.com/u/66957274?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tom Dolhs</b></sub></a></td>
    <td align="center"><a href="https://github.com/ljelschen"><img src="https://avatars.githubusercontent.com/u/34402946?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ljelschen</b></sub></a></td>
    <td align="center"><a href="https://github.com/lukruh"><img src="https://avatars.githubusercontent.com/u/7965770?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Lukas</b></sub></a></td>
  </tr>
</table>

Contributions of any kind welcome!
