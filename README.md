# Download Stup.ID files

A Python script for downloading files from [elearning.uni-bremen.de](https://elearning.uni-bremen.de).
Using Multi-Threading to download and extract files from multiple courses at the same time.

## Setup
1. Install `python3` and the `requests` and `beatifulsoup4` modules, thats all.

2. In the `config.ini` file
* replace `studip_username` and `studip_password` with your Stup.ID login
* set the folder for the files to be placed in
* add the id's of courses you want to download files from

You can find course id (`cid`) in the URL of the course page.

For example `https://elearning.uni-bremen.de/dispatch.php/course/overview?cid=59e9f16a68530c5ab9a100ae908a834d` can be added to the `config.ini` like this:

`mi2 = 59e9f16a68530c5ab9a100ae908a834d`

where `mi2` ist the subfolder name and `59e9f16a68530c5ab9a100ae908a834d` is the course id taken from the url.

> You need to have permission to download the files otherwise the script won't
work.

## Usage
Run the script from the command line to download the files.

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

Contributions of any kind are much appreciated!
