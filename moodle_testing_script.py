import csv
import os
import time
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
    try:
        # Navigate to the course page
        driver.get("https://sandbox.moodledemo.net/course/view.php?id=2")
        time.sleep(5)  # Wait for the page to load

        # Click on the "News forum" link
        if not click_when_clickable(By.LINK_TEXT, "News forum"):
            write_report('test_forum_posting', 'Fail')
            return

        # Click on the "Add a new topic" button
        if not click_when_clickable(By.LINK_TEXT, "Add a new topic"):
            write_report('test_forum_posting', 'Fail')
            return

        # Enter the subject
        subject_field = driver.find_element(By.ID, "id_subject")
        subject_field.send_keys("Forum test")

        # Enter the message
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))  # Switch to the text editor frame
        message_field = driver.find_element(By.ID, "tinymce")
        message_field.send_keys("Test forum")
        driver.switch_to.default_content()  # Switch back to the main content

        # Click on the "Post to forum" button
        if not click_when_clickable(By.ID, "id_submitbutton"):
            write_report('test_forum_posting', 'Fail')
            return

        # If everything passed, write a pass result to the report
        write_report('test_forum_posting', 'Pass')
    except Exception as e:
        print(f"An error occurred: {e}")
        write_report('test_forum_posting', 'Fail')

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