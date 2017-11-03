# studip-sync
A python script for downloading files from your studip courses. It's designed
to run for the studip platform of the university of bremen: 
https://elearning.uni-bremen.de
But it should be possible to move this to any studip installation by changing
the urls.

## Setup
It's just a script no GUI or service files yet. To run it you need to have
installed python3 with the requests and beatifulsoup4 modules, thats all.

All settings are done via the config.ini file. It's editable with andy text
editor in windows and linux. It needs to be in the same directory as the
studip-sync.py file or the script file must be edited to the correct path of
the config.ini. Replace `studip_username` and `studip_password` in the
config.ini
with your login.
The path can be relative (to python workdir) or absolute.

Just ignore the other lines in [settings] section, they don't do anything yet.

## Courses
In the courses section add the courses you want to download files from. Ofcause
you need to have permissions to download the files otherwise the script wont
work.

To add a course give it a name (this is also the subfolder the script creates to
organize the courses files) and the course id, which is the long number in the
url (at the course page: https://elearning.uni-bremen.de/dispatch.php/course/overview?cid=847b6d81388cd9742f31bdc363507bbc) in the form:

```subfolder_name = 01aj19courseid13981938hf```

## Usage
Run the script with double click or from commandline 
