import json
from selenium import webdriver
import openai
import logging

import linkedin_automation
import openai_integration
import document_processing
import application_tracking

# Set up logging
logging.basicConfig(filename='job_application_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JobApplicationBot:
    def __init__(self, config_file, openai_key):
        try:
            with open(config_file) as f:
                self.config = json.load(f)
            self.driver = webdriver.Chrome()
            openai.api_key = openai_key
            self.user_profile = {}
            logging.info("JobApplicationBot initialized successfully.")
        except FileNotFoundError:
            logging.error(f"Configuration file '{config_file}' not found.")
        except Exception as e:
            logging.error(f"An error occurred during initialization: {e}")

    def run(self, job_link, resume_path, cover_letter_path, profile_document_path=None, interview_details=None, job_description=None):
        try:
            linkedin_automation.login_linkedin(self.driver, self.config['linkedin']['username'], self.config['linkedin']['password'])
            if profile_document_path:
                self.user_profile = document_processing.learn_from_document(profile_document_path)
                skills = document_processing.extract_skills_from_document(profile_document_path)
                education = document_processing.extract_education_from_document(profile_document_path)
                self.user_profile['skills'] = skills
                self.user_profile['education'] = education
            linkedin_automation.apply_on_linkedin(self.driver, job_link)
            if resume_path and cover_letter_path:
                linkedin_automation.attach_files(self.driver, resume_path, cover_letter_path)
            if interview_details:
                application_tracking.schedule_interview(interview_details)
            if job_description:
                cover_letter = openai_integration.generate_cover_letter(openai.api_key, job_description, self.user_profile)
                skill_recommendations = openai_integration.get_skill_recommendations(openai.api_key, job_description, self.user_profile)
                application_status = application_tracking.track_application_status(job_id=self.config['job_id'], company_id=self.config['company_id'])
                networking_assistance = application_tracking.networking_assistance(openai.api_key, self.user_profile, job_description)
                print("Cover Letter:", cover_letter)
                print("Skill Recommendations:", skill_recommendations)
                print("Application Status:", application_status)
                print("Networking Assistance:", networking_assistance)
                logging.info("Job application process completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred during the job application process: {e}")
        finally:
            self.driver.quit()
            logging.info("WebDriver quit successfully.")

    def schedule_interview(self, interview_details):
        try:
            application_tracking.schedule_interview(interview_details)
            logging.info(f"Interview scheduled successfully: {interview_details}")
        except Exception as e:
            logging.error(f"An error occurred while scheduling the interview: {e}")

if __name__ == "__main__":
    bot = JobApplicationBot('config.json', 'your_openai_api_key')
    bot.run(
        job_link='https://www.linkedin.com/jobs/your-job-link',
        resume_path='resume.pdf',
        cover_letter_path='cover_letter.docx',
        profile_document_path='your_profile.docx',
        interview_details={'date': '2024-05-01', 'time': '10:00 AM', 'location': 'Virtual'},
        job_description={'role': 'Software Engineer', 'company': 'ABC Corp'}
    )