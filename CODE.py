from selenium import webdriver
import getpass
import urllib2
import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import natsort
import glob
import shutil

final_location = "/home/rohithsrinivaas/Documents/SPW_Project/output"
global courses_enrolled

def init_driver():
    #changes the profile settings of the tab that gets opened such that the file is directly downloaded instead of opening in a new tab
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir",final_location)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    fp.set_preference("pdfjs.disabled", True)
    driver = webdriver.Firefox(fp)
    driver.wait = WebDriverWait(driver, 20)
    return driver
 
def login_btn(driver):
    #searches for the login button and clicks it
    try:
        driver.implicitly_wait(10)
        btn = driver.find_element_by_link_text('Log in')
        btn.click()  
    except TimeoutException:
        print("Log in Button not found")

def login_pwd(driver):
    #enters the username and password given by the user
    try:
        
        username_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(raw_input("Enter the username : "))

    
        password_field = driver.wait.until(EC.presence_of_element_located((By.ID,"password")))
        password_field.send_keys(getpass.getpass("Enter the password : "))
        btn= driver.wait.until(EC.presence_of_element_located((By.ID, "loginbtn")))
        btn.click()
    except TimeoutException:
        print("Box or Button not found")

def courses_folder_creater(driver):
    #creates the folder for each subject
    my_courses=driver.find_element_by_link_text('My courses')
    my_courses.click()
    enrolled = []
    driver.implicitly_wait(10)
    region_content = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div[2]/div/div/div[2]/ul/li/ul/li[@aria-expanded = "true"]/ul/li')
    for region in region_content:
        folder = region.text
        enrolled.append(folder)
        directory = final_location + '/'+ folder
        if not os.path.exists(directory):
            os.makedirs(directory)
    driver.implicitly_wait(10)
    home = driver.find_element_by_link_text('Home')
    home.click()
    return enrolled

def download_in_folder(driver,folder_name):
    #downloads the pdfs from the course page
    my_courses=driver.find_element_by_link_text('My courses')
    my_courses.click()
    driver.implicitly_wait(10)
    course_link= driver.find_element_by_link_text(folder_name)
    course_link.click()
    driver.implicitly_wait(10)

    try:
        topic= driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"course-content")))
        subtopics_list=topic.find_elements_by_css_selector('a')
        driver.implicitly_wait(10)
        for l in subtopics_list:
    
            if l.find_element_by_tag_name('img').get_attribute('src') == 'https://courses.iitm.ac.in/theme/image.php/leatherbound/core/1484031847/f/pdf-24' and l.find_element_by_xpath('.//span[@class = "instancename"]/span[@class = "accesshide "]').text == "File":
                driver.implicitly_wait(10)
                time.sleep(5)
                l.click()
                time.sleep(5)
                driver.implicitly_wait(10)
        home = driver.find_element_by_link_text('Home')
        home.click()
    except TimeoutException:
        print("Not found")
def move_to_subject_folder(folder_name):
    #moves the downloaded files from the temp location to the respective subject folder
    file_list = natsort.natsorted(glob.glob(os.path.join(final_location, '*.*')))
    dst = os.path.join(final_location,folder_name)
    for file in file_list:
        shutil.move(file,dst)
        print(file)



if __name__ == "__main__":
    driver = init_driver()
    driver.get("https://courses.iitm.ac.in/")
    login_btn(driver)
    time.sleep(2)
    login_pwd(driver)
    time.sleep(4)
    subdirectories = courses_folder_creater(driver)
    time.sleep(4)
    for subject in subdirectories:
        print(subject)
    	download_in_folder(driver,subject)
    	move_to_subject_folder(subject)
    driver.quit()