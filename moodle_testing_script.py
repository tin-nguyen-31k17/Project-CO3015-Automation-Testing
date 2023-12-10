import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Initialize the WebDriver
driver = webdriver.Chrome()

# Function to wait for an element to be clickable and then click
def click_when_clickable(by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except NoSuchElementException:
        print(f"Element not found: {value}")
        return False
    except TimeoutException:
        print(f"Timeout while waiting for element: {value}")
        return False

# Function to write a report to a CSV file
def write_report(test_name, result, filename='test_report.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([test_name, result, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())])

# Level 0: Automation without using data-driven testing approach
def test_login():
    driver.get("https://sandbox.moodledemo.net/login/index.php")
    logInAccount=driver.find_element(By.ID,"username")
    logInAccount.send_keys("student")
    logInAccount=driver.find_element(By.ID,"password")
    logInAccount.send_keys("sandbox")
    logInAccount.submit()

def test_course_registration():
    # try to register for a course
    click_when_clickable(By.LINK_TEXT, "My second course")

def test_forum_posting():
    # Add steps for forum posting
    driver.get("https://sandbox.moodledemo.net/")
    click_when_clickable(By.LINK_TEXT, "My first course")
    click_when_clickable(By.LINK_TEXT, "News Forum")
    click_when_clickable(By.ID, "yui_3_18_1_1_1702097450106_51")
    postForum=driver.find_element(By.ID,"id_subject")
    postForum.send_keys("Forum test")
    postForum=driver.find_element(By.ID,"tinymce")
    postForum.send_keys("test forum")
    click_when_clickable(By.ID, "id_submitbutton")

def test_assignment_submission():
    # Add steps for assignment submission
    click_when_clickable(By.LINK_TEXT, "My first course")
    click_when_clickable(By.LINK_TEXT, "Assignment 1")
    click_when_clickable(By.CLASS_NAME, "singlebutton")
    driver.implicitly_wait(5)
    click_when_clickable(By.CLASS_NAME, "fp-btn-add")
    click_when_clickable(By.CLASS_NAME, "px-3")

    upload_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".", "test.pdf"))
    file_upload = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "repo_upload_file")))

    file_upload.send_keys(upload_file)
    click_when_clickable(By.CLASS_NAME, "fp-upload-btn")

    click_when_clickable(By.ID, "id_submitbutton")

# Level 1: Automation using data-driven testing approach
def run_data_driven_tests(test_data_file):
    with open(test_data_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Test'] == 'Login':
                test_login()
            elif row['Test'] == 'Course Registration':
                test_course_registration()
            # Add other tests as needed

# Level 2: Automation using data-driven testing approach with inputs
def run_tests_with_inputs(test_data_file):
    with open(test_data_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            driver.get(row['URL'])
            if row['Test'] == 'Search Post':
                # Add steps for searching a post
                pass
            elif row['Test'] == 'Search Documentation':
                # Add steps for searching documentation
                pass
            # Add other tests as needed

# Test cases file for Level 1 and Level 2
test_data_file = 'test_cases.csv'

# Run Level 0 tests
try:
    test_login()
    test_forum_posting()
    test_assignment_submission()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Write the report
    write_report('Test Name', 'Pass or Fail')

# Run Level 1 tests
# run_data_driven_tests(test_data_file)

# Run Level 2 tests
# run_tests_with_inputs(test_data_file)

# Write the report
write_report('Test Name', 'Pass or Fail')