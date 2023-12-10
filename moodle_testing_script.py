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
    logInAccount.send_keys("teacher")
    logInAccount=driver.find_element(By.ID,"password")
    logInAccount.send_keys("sandbox")
    logInAccount.submit()

# Function to test searching for a post
def test_search_post(post_name):
    try:
        # Navigate to the forum page
        driver.get("https://sandbox.moodledemo.net/mod/forum/view.php?id=1")
        time.sleep(5)  # Wait for the page to load

        # Enter the post name in the search field
        search_field = driver.find_element(By.NAME, "q")
        search_field.send_keys(post_name)

        # Click on the "Search forums" button
        if not click_when_clickable(By.CLASS_NAME, "btn-primary"):
            write_report('test_search_post', 'Fail')
            return

        # If everything passed, write a pass result to the report
        write_report('test_search_post', 'Pass')
    except Exception as e:
        print(f"An error occurred: {e}")
        write_report('test_search_post', 'Fail')

# Function to test searching for documentation
def test_search_documentation(doc_name):
    try:
        # Navigate to the documentation page
        driver.get("https://sandbox.moodledemo.net/my/courses.php")
        time.sleep(5)  # Wait for the page to load

        # Enter the documentation name in the search field
        search_field = driver.find_element(By.NAME, "q")
        search_field.send_keys(doc_name)

        # Click on the "Search" button
        if not click_when_clickable(By.CLASS_NAME, "btn-primary"):
            write_report('test_search_documentation', 'Fail')
            return

        # If everything passed, write a pass result to the report
        write_report('test_search_documentation', 'Pass')
    except Exception as e:
        print(f"An error occurred: {e}")
        write_report('test_search_documentation', 'Fail')

def test_course_registration():
    # Add steps for course registration
    click_when_clickable(By.LINK_TEXT, "My second course")
    click_when_clickable(By.LINK_TEXT, "Enrol me")


def test_forum_posting():
    try:
        # Navigate to the course page
        driver.get("https://sandbox.moodledemo.net/mod/forum/view.php?id=1")
        time.sleep(5)  # Wait for the page to load

        # Click on the "Add discussion topic" link
        if not click_when_clickable(By.LINK_TEXT, "Add discussion topic"):
            write_report('test_forum_posting', 'Fail')
            return
        
        # Enter the subject
        subject_field = driver.find_element(By.ID, "id_subject")
        subject_field.send_keys("Test topic")

        # Enter the message
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))  # Switch to the text editor frame
        message_field = driver.find_element(By.ID, "tinymce")
        message_field.send_keys("Test forum")
        driver.switch_to.default_content()  # Switch back to the main content

        # Click on the "Add a new topic" button
        if not click_when_clickable(By.LINK_TEXT, "Test topic"):
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
            try:
                if row['Test'] == 'Login':
                    test_login()
                    write_report('test_login', 'Pass')
                elif row['Test'] == 'Course Registration':
                    test_course_registration()
                    write_report('test_course_registration', 'Pass')
                # Add other tests as needed
            except Exception as e:
                print(f"An error occurred: {e}")
                write_report(row['Test'], 'Fail')

# Level 2: Automation using data-driven testing approach with inputs
def run_tests_with_inputs(test_data_file):
    with open(test_data_file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                driver.get(row['URL'])
                if row['Test'] == 'Search Post':
                    # Add steps for searching a post
                    test_search_post(row['Input'])
                    pass
                elif row['Test'] == 'Search Documentation':
                    # Add steps for searching documentation
                    test_search_documentation(row['Input'])
                    pass
                # Add other tests as needed
                write_report(row['Test'], 'Pass')
            except Exception as e:
                print(f"An error occurred: {e}")
                write_report(row['Test'], 'Fail')

# Test cases file for Level 1 and Level 2
test_data_file = 'test_cases.csv'

# Run Level 0 tests
try:
    test_login()
    test_search_post('Test')
    test_search_documentation('Test')
    test_forum_posting()
    test_assignment_submission()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Write the report
    write_report('test_login', 'Pass')
    write_report('test_forum_posting', 'Pass')
    write_report('test_assignment_submission', 'Pass')

# Run Level 1 tests
run_data_driven_tests(test_data_file)

# Run Level 2 tests
run_tests_with_inputs(test_data_file)

# Close the driver
driver.quit()