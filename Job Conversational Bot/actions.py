from typing import Dict, Text, Any, List
import random
import datetime
from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_nlu.model import Interpreter
from resources import SAMPLE_JOBS, RECOMMENDED_JOBS, INTERVIEW_RESOURCES, COMPANY_INFO, FAQ, SKILL_RESOURCES

# NLP model for intent classification
nlp = Interpreter.load("Unstop-Talent-Park\Job Conversational Bot\nlu.md")  # Path to your trained Rasa model

# (Optional) Integrate with a job search API (replace with your implementation)
def search_jobs(skills, location):
    try:
        # Simulate job search using sample data
        jobs = SAMPLE_JOBS
        if skills:
            jobs = [job for job in jobs if any(skill.lower() in job["title"].lower() for skill in skills)]
        if location:
            jobs = [job for job in jobs if location.lower() in job["company"].lower()]
        return jobs[:3]  # Return a maximum of 3 jobs
    except Exception as e:
        print(f"Error searching jobs: {e}")
        return []

# Function to recommend jobs based on user's skills and preferences
def recommend_jobs(user_skills):
    try:
        recommended_jobs = RECOMMENDED_JOBS
        if user_skills:
            recommended_jobs = [job for job in recommended_jobs if any(skill.lower() in job["title"].lower() for skill in user_skills)]
        return recommended_jobs
    except Exception as e:
        print(f"Error recommending jobs: {e}")
        return []

# Function to submit resume
def submit_resume(user_details):
    try:
        # Replace this with your resume submission logic
        # For demonstration, print the received details
        print("Resume Submitted:")
        print(user_details)
    except Exception as e:
        print(f"Error submitting resume: {e}")

# Function to provide interview preparation resources
def interview_preparation_resources():
    try:
        return INTERVIEW_RESOURCES
    except Exception as e:
        print(f"Error fetching interview resources: {e}")
        return []

# Function to provide information about a company
def company_information(company_name):
    try:
        return COMPANY_INFO.get(company_name, None)
    except Exception as e:
        print(f"Error fetching company information: {e}")
        return None

# Function to track application status
def track_application_status(application_id):
    try:
        # Replace this with your application status tracking logic
        # For demonstration, return a random application status
        statuses = ["Submitted", "Under review", "Interview scheduled", "Offer extended", "Rejected"]
        return random.choice(statuses)
    except Exception as e:
        print(f"Error tracking application status: {e}")
        return "Error"

# Function to recommend skill development resources
def skill_development_resources(skill):
    try:
        return SKILL_RESOURCES.get(skill, [])
    except Exception as e:
        print(f"Error fetching skill resources: {e}")
        return []

# Function to answer frequently asked questions
def answer_faq(question):
    try:
        return FAQ.get(question, "Sorry, I don't have an answer to that question.")
    except Exception as e:
        print(f"Error answering FAQ: {e}")
        return "Sorry, I'm unable to answer that question at the moment."

# Function to subscribe to job alerts
def subscribe_to_job_alerts(user_email, job_preferences):
    try:
        # Replace this with your job alert subscription logic
        # For demonstration, print the received details
        print("Job Alerts Subscription:")
        print("Email:", user_email)
        print("Preferences:", job_preferences)
    except Exception as e:
        print(f"Error subscribing to job alerts: {e}")

# Function to collect feedback
def collect_feedback(feedback):
    try:
        # Replace this with your feedback collection logic
        # For demonstration, print the received feedback
        print("Feedback Received:", feedback)
    except Exception as e:
        print(f"Error collecting feedback: {e}")

# Function to schedule interviews or appointments
def schedule_interview(user_email, datetime):
    try:
        # Replace this with your interview scheduling logic
        # For demonstration, print the scheduled interview details
        print("Interview Scheduled:")
        print("Email:", user_email)
        print("Date and Time:", datetime)
    except Exception as e:
        print(f"Error scheduling interview: {e}")

class ActionGreet(Action):
    """Greets the user and introduces the chatbot."""

    def name(self) -> Text:
        return "action_greet"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_greet")
        return []

class ActionAskJobSearchIntent(Action):
    """Asks the user what they want to do related to job applications."""

    def name(self) -> Text:
        return "action_ask_job_search_intent"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_ask_job_search_intent")
        return []

class ActionSearchJobsByUserInput(Action):
    """Searches for jobs based on user-provided skills and location."""

    def name(self) -> Text:
        return "action_search_jobs_by_user_input"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        skills = tracker.get_slot("skills")
        location = tracker.get_slot("location")
        jobs = search_jobs(skills, location)

        if jobs:
            message = (
                f"Found some job openings that might be a good fit for you:\n"
                f"{', '.join([job['title'] + ' at ' + job['company'] for job in jobs])}"
            )
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_no_jobs_found")

        return [AllSlotsReset()]

class ActionProcessJobApplication(Action):
    """Processes user intent to apply for a job using NLP."""

    def name(self) -> Text:
        return "action_process_job_application"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        message = tracker.latest_message.get("text")
        # Use NLP to understand the user's intent and extract job title (if possible)
        interpretation = nlp.parse(message)
        job_title = interpretation.get("entities", {}).get("job_title", [None])[0]

        if job_title:
            # User might have mentioned a job title, confirm details before proceeding
            dispatcher.utter_message(template="utter_confirm_job_application", job_title=job_title)
            return [SlotSet("job_title", job_title)]
        else:
            # User didn't mention a job title, ask for clarification
            dispatcher.utter_message(template="utter_need_more_info_job_application")
            return []

class ActionTrackApplications(Action):
    """ (Optional) Handles tracking job applications. (Not implemented yet)"""

    def name(self) -> Text:
        return "action_track_applications"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        # (Replace with logic to access and display tracked applications)
        dispatcher.utter_message(template="utter_applications_not_implemented")
        return []

class ActionRecommendJobs(Action):
    """Recommends jobs based on user's skills."""

    def name(self) -> Text:
        return "action_recommend_jobs"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        user_skills = tracker.get_slot("skills")
        recommended_jobs = recommend_jobs(user_skills)
        if recommended_jobs:
            message = (
                f"Here are some job recommendations based on your skills:\n"
                f"{', '.join([job['title'] + ' at ' + job['company'] for job in recommended_jobs])}"
            )
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_no_jobs_found")

        return []

class ActionSubmitResume(Action):
    """Submits user's resume."""

    def name(self) -> Text:
        return "action_submit_resume"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        user_details = {
            "name": tracker.get_slot("name"),
            "email": tracker.get_slot("email"),
            "resume": tracker.get_slot("resume")
        }
        submit_resume(user_details)
        dispatcher.utter_message(template="utter_resume_submitted")
        return []

class ActionProvideInterviewResources(Action):
    """Provides interview preparation resources."""

    def name(self) -> Text:
        return "action_provide_interview_resources"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        resources = interview_preparation_resources()
        dispatcher.utter_message(text="Here are some interview preparation resources:")
        for resource in resources:
            dispatcher.utter_message(text="- " + resource)
        return []

class ActionProvideCompanyInfo(Action):
    """Provides information about a company."""

    def name(self) -> Text:
        return "action_provide_company_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        company_name = tracker.get_slot("company_name")
        company_info = company_information(company_name)
        if company_info:
            message = (
                f"{company_info['name']}: {company_info['description']}\n"
                f"Available jobs: {', '.join(company_info['jobs'])}"
            )
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_company_info_not_found")
        return []

class ActionTrackApplicationStatus(Action):
    """Tracks the status of a job application."""

    def name(self) -> Text:
        return "action_track_application_status"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        application_id = tracker.get_slot("application_id")
        application_status = track_application_status(application_id)
        dispatcher.utter_message(text=f"The status of your application (ID: {application_id}) is: {application_status}")
        return []

class ActionRecommendSkillResources(Action):
    """Recommends skill development resources based on user's skill."""

    def name(self) -> Text:
        return "action_recommend_skill_resources"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        skill = tracker.get_slot("skill")
        skill_resources = skill_development_resources(skill)
        if skill_resources:
            message = f"Here are some resources for developing your {skill} skills:"
            for resource in skill_resources:
                message += f"\n- {resource}"
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(template="utter_skill_resources_not_found")
        return []

class ActionSubscribeToJobAlerts(Action):
    """Subscribes user to job alerts."""

    def name(self) -> Text:
        return "action_subscribe_to_job_alerts"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        user_email = tracker.get_slot("email")
        job_preferences = tracker.get_slot("job_preferences")
        subscribe_to_job_alerts(user_email, job_preferences)
        dispatcher.utter_message(template="utter_job_alerts_subscribed")
        return []

class ActionCollectFeedback(Action):
    """Collects user feedback."""

    def name(self) -> Text:
        return "action_collect_feedback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        feedback = tracker.latest_message.get("text")
        collect_feedback(feedback)
        dispatcher.utter_message(template="utter_feedback_collected")
        return []

class ActionScheduleInterview(Action):
    """Schedules an interview."""

    def name(self) -> Text:
        return "action_schedule_interview"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        user_email = tracker.get_slot("email")
        interview_datetime = datetime.datetime.strptime(tracker.get_slot("interview_datetime"), "%Y-%m-%dT%H:%M:%S.%fZ")
        schedule_interview(user_email, interview_datetime)
        dispatcher.utter_message(template="utter_interview_scheduled")
        return []

class ActionAnswerFAQ(Action):
    """Answers frequently asked questions."""

    def name(self) -> Text:
        return "action_answer_faq"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        question = tracker.latest_message.get("text")
        answer = answer_faq(question)
        dispatcher.utter_message(text=answer)
        return []