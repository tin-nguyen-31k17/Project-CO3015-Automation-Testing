import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome()

# Level 0: Automation without using data-driven testing approach
def test_login():
    driver.get("https://moodle.org/demo")
    driver.find_element(By.LINK_TEXT, "Log in as a guest").click()

def test_course_registration():
    # Add steps for course registration
    pass

def test_forum_posting():
    # Add steps for forum posting
    pass

def test_assignment_submission():
    # Add steps for assignment submission
    pass

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
test_login()
test_course_registration()
test_forum_posting()
test_assignment_submission()

# Run Level 1 tests
run_data_driven_tests(test_data_file)

# Run Level 2 tests
run_tests_with_inputs(test_data_file)

# Close the WebDriver
driver.quit()

