import openai
import logging

# Set up logging
logging.basicConfig(filename='openai_integration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_application_form_data(api_key, job_description):
    try:
        openai.api_key = api_key
        prompt = f"Please provide appropriate responses to fill out a job application form for the following role: {job_description['role']} at {job_description['company']}. Include details relevant to the position and align with the job requirements."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        application_form_data = response.choices[0].text.strip()
        logging.info("Successfully generated application form data using OpenAI.")
        return application_form_data
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while generating application form data: {e}")
        return None

def generate_cover_letter(api_key, job_description, user_profile):
    try:
        openai.api_key = api_key
        prompt = f"Please generate a cover letter for the {job_description['role']} position at {job_description['company']} based on the following user profile:\n\n{user_profile}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        cover_letter = response.choices[0].text.strip()
        logging.info("Successfully generated cover letter using OpenAI.")
        return cover_letter
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while generating cover letter: {e}")
        return None

def get_skill_recommendations(api_key, job_description, user_profile):
    try:
        openai.api_key = api_key
        prompt = f"Based on the job description for the {job_description['role']} position at {job_description['company']} and the following user profile:\n\n{user_profile}\n\nPlease provide recommendations for skills or areas the user should focus on improving or learning to better align with the job requirements."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        skill_recommendations = response.choices[0].text.strip()
        logging.info("Successfully generated skill recommendations using OpenAI.")
        return skill_recommendations
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while generating skill recommendations: {e}")
        return None