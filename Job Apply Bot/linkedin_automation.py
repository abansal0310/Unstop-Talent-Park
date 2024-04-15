from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

# Set up logging
logging.basicConfig(filename='linkedin_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_linkedin(driver, username, password):
    try:
        driver.get('https://www.linkedin.com/login')
        username_field = driver.find_element_by_id('username')
        password_field = driver.find_element_by_id('password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for login to complete
        logging.info("Successfully logged in to LinkedIn.")
    except NoSuchElementException:
        logging.error("Unable to locate login fields on the LinkedIn login page.")
    except Exception as e:
        logging.error(f"An error occurred while logging in to LinkedIn: {e}")

from openai_integration import generate_application_form_data

def fill_application_form(driver, application_form_data):
    # Set up the webdriver (replace "chromedriver" with the path to your webdriver if necessary)
    driver = webdriver.Chrome("chromedriver")

    # Navigate to the application form
    driver.get("https://example.com/application-form")

    # Fill out the form
    driver.find_element_by_name("first_name").send_keys(application_form_data["first_name"])
    driver.find_element_by_name("last_name").send_keys(application_form_data["last_name"])
    driver.find_element_by_name("email").send_keys(application_form_data["email"])
    driver.find_element_by_name("phone").send_keys(application_form_data["phone"])
    driver.find_element_by_name("preferred_location").send_keys(application_form_data["preferred_location"])

    # Submit the form
    driver.find_element_by_name("submit").click()

def apply_on_linkedin(driver, job_link):
    try:
        driver.get(job_link)
        time.sleep(2)  # Wait for job page to load

        easy_apply_button = driver.find_element_by_xpath('//button[@data-control-name="jobdetails_topcard_inapply"]')
        easy_apply_button.click()
        time.sleep(2)  # Wait for Easy Apply modal to load

        # Generate application form data
        application_form_data = generate_application_form_data()

        # Fill out application form
        fill_application_form(driver, application_form_data)

        submit_button = driver.find_element_by_xpath('//button[@data-control-name="submit_unify"]')
        submit_button.click()
        time.sleep(2)  # Wait for application to be submitted
        logging.info("Job application submitted successfully.")
    except NoSuchElementException:
        logging.error("Unable to locate the 'Easy Apply' button or the submit button on the job application page.")
    except TimeoutException:
        logging.error("Timed out waiting for the job application page or Easy Apply modal to load.")
    except Exception as e:
        logging.error(f"An error occurred while applying for the job: {e}")

def attach_files(driver, resume_path, cover_letter_path):
    try:
        # Find the input elements for uploading resume and cover letter
        resume_input = driver.find_element_by_xpath('//input[@name="resume"]')
        cover_letter_input = driver.find_element_by_xpath('//input[@name="cover_letter"]')

        # Send the paths of resume and cover letter files to the corresponding input elements
        resume_input.send_keys(resume_path)
        cover_letter_input.send_keys(cover_letter_path)

        logging.info("Resume and cover letter attached successfully.")
    except Exception as e:
        logging.error(f"An error occurred while attaching files: {e}")
