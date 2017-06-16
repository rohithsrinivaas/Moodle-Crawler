# SPW-2017-Project
# Moodle Crawler
Requires the username and password of the user registered in moodle iitm

# Dependencies
Selenium 3.4.3
urllib (1.21.1)
pathlib (1.0.1)
pathlib2 (2.2.1)
urllib3 (1.21.1)
Python 2.7

# Setup
This code has been tested on Ubuntu Mate 16.04


# Program
## CODE.py 
1)This script requires your moodle iitm username and password and logins into your moodle iitm account and downloads the latest uploaded files from moodle from courses that you are enrolled in.
2)This script only files which are pdfs
3)This script also creates the folders(with name as your subject names) in your computer.

# Function Description
## move_to_subject_folder : 
      moves the downloaded files from the temp location to the respective subject folder.
## download_in_folder : 
      downloads the pdfs from the course page
## courses_folder_creater:
      creates the folder for each subject
## login_pwd : 
      enters the username and password given by the user
## login_btn : 
      searches for the login button and clicks it
## init_driver : 
      changes the profile settings of the tab that gets opened such that the file is directly downloaded instead of opening in a new tab

# More Updates : 
    Log file for files already downloaded as to be created
    Log file for username and password has to be remembered in the log file
