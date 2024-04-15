from flask import Flask, render_template, request
import json
from selenium import webdriver
import logging

import JobApplicationBot

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='job_application_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle form submission
        job_link = request.form.get('job_link')
        resume_path = request.form.get('resume_path')
        cover_letter_path = request.form.get('cover_letter_path')
        profile_document_path = request.form.get('profile_document_path')
        interview_details = request.form.get('interview_details')
        job_description = request.form.get('job_description')

        # Load configuration file
        with open('config.json') as f:
            config = json.load(f)

        # Initialize JobApplicationBot
        bot = JobApplicationBot(config_file='config.json', openai_key=config['openai_key'])

        # Run the job application process
        bot.run(job_link, resume_path, cover_letter_path, profile_document_path, interview_details, job_description)

        # Render the results template
        return render_template('results.html')

    # Render the home template
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug='FALSE')
