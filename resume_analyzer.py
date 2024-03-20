import pandas as pd
from datetime import datetime
from collections import Counter
import re
import PyPDF2
from parse import parse

def get_current_date_string():
    """Returns string for today's date."""
    current_date = datetime.today()
    date_string = current_date.strftime('%Y-%m-%d')
    return date_string

def parse_resume(resume_file):
    """Parses a resume in PDF format using PyPDF2 and extracts relevant information.

    Args:
        resume_file: Path to the PDF file containing the resume.

    Returns:
        A dictionary containing extracted information like skills, experience, and education.
    """
    resume_data = {}
    
    # Read the PDF file
    with open(resume_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    
    # Extract skills using regular expressions (customize as needed)
    skills_pattern = r"(skills?\s*[:\-])\s*(.*)"
    skills_match = parse(skills_pattern, resume_text, ignorecase=True)
    if skills_match:
        resume_data["skills"] = skills_match[2].split(",")
  
    # Extract experience using regular expressions (customize as needed)
    experience_pattern = r"(work experience|experience)\s*[:\-]\s*(.*?)(?=\n\s*work experience|\n\s*education|\Z)"
    experience_matches = parse(experience_pattern, resume_text, multi=True, ignorecase=True)
    if experience_matches:
        experience_data = []
        for match in experience_matches:
            company, title, *_ = match[2].split("\n")  # Assuming company and title on separate lines
            experience_data.append({"company": company.strip(), "title": title.strip()})
        resume_data["experience"] = experience_data

    # Extract education using regular expressions (customize as needed)
    education_pattern = r"(education\s*[:\-])\s*(.*?)(?=\n\s*work experience|\Z)"
    education_matches = parse(education_pattern, resume_text, multi=True, ignorecase=True)
    if education_matches:
        education_data = []
        for match in education_matches:
            degree, institution, *_ = match[2].split("\n")  # Assuming degree and institution on separate lines
            education_data.append({"degree": degree.strip(), "institution": institution.strip()})
        resume_data["education"] = education_data

    return resume_data

def parse_job_description(job_desc_file):
    """Parses a job description in PDF format using PyPDF2 and extracts relevant information.

    Args:
        job_desc_file: Path to the PDF file containing the job description.

    Returns:
        A dictionary containing extracted information like skills, experience, and education.
    """
    job_data = {}
    
    # Similar logic to parse_resume can be implemented here to extract skills, experience, and education information from the job description.
    # You can leverage regular expressions or named entity recognition techniques from NLP libraries for more robust extraction.

    return job_data

def calculate_resume_score(resume_dict, job_dict, weights={}):
    """
    Calculates a score based on how well a resume matches a job description.

    Args:
        resume_dict: Dictionary containing parsed resume data (skills, experience, education).
        job_dict: Dictionary containing parsed job description data (skills, experience, education).
        weights: Optional dictionary assigning weights to different factors (skills, experience, education).

    Returns:
        A numerical score between 0 and 1 indicating the resume's fit for the job.
    """
    default_weights = {"skills": 0.4, "experience": 0.4, "education": 0.2}
    weights = weights or default_weights

    resume_skills = set(resume_dict.get("skills", []))
    job_skills = set(job_dict.get("skills", []))
    skill_match_score = len(resume_skills.intersection(job_skills))

    # Additional logic to calculate scores based on experience and education can be added here
    
    # Combine scores for different factors using weights
    total_score = (weights.get("skills", 0) * skill_match_score +
                   weights.get("experience", 0) * 0 +  # Placeholder for experience score
                   weights.get("education", 0) * 0)   # Placeholder for education score

    # Normalize score to range between 0 and 1
    max_possible_score = sum(weights.values())
    resume_score = total_score / max_possible_score if max_possible_score != 0 else 0

    return resume_score

# Parse candidate's resume
resume_file = "resume_example.pdf"  # Change to actual file path
resume_data = parse_resume(resume_file)

# Parse job description
job_desc_file = "job_description_example.pdf"  # Change to actual file path
job_data = parse_job_description(job_desc_file)

# Calculate resume score
resume_score = calculate_resume_score(resume_data, job_data)
print("Resume Score:", resume_score)
