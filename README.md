# Moodle Demo Site Testing Script

This is the basic core script for the project 3. I hope you guys can spend sometime to read this README first, it'll provides instructions on how to set up and run the Selenium WebDriver script for automated black box testing of the Moodle demo site.

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.x
- Selenium package for Python
- Chrome WebDriver

## Installation

1. Install Python 3.x from the official website. (I think you guys should run in venv mode to avoid conflict but anw, your system, your choice)
2. Install Selenium using pip: pip install selenium
3. Download the Chrome WebDriver from the ChromeDriver download page and place it in your system PATH.

## Running the Script

1. Clone or download the testing script from the repository.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is located.
4. Run the script using Python: python moodle_testing_script.py


## Test Cases

The script includes test cases in Part B but I haven't complete the definition yet. You guys should split part and start doing it:
- Searching a post
- Searching documentation
- Login to Moodle
- Course Registration
- Forum Posting
- Assignment Submission
- Page load time measurement

## Data-Driven Testing

For data-driven testing, create a CSV file named `test_cases.csv` with the following columns:
- `Test`: The name of the test case.
- `URL`: The URL to test.
- Additional parameters specific to each test case.

The script will read this file and execute the tests accordingly.

## Customization

You can customize the script by modifying the test functions to fit your specific testing needs. Ensure that the element locators are updated if the Moodle demo site structure changes.

## Support

For any issues or questions regarding the script, please open an issue in the repository or simply text me.

