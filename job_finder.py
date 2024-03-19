import pandas as pd
from datetime import datetime

def get_current_date_string():
    """Returns string for today's date."""
    current_date = datetime.today()
    date_string = current_date.strftime('%Y-%m-%d')
    return date_string

def load_job_listings(data_file):
    """Loads job listings data from a CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(data_file)
        return df
    except FileNotFoundError:
        print(f"Error: File '{data_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: Unable to load data from '{data_file}': {str(e)}")
        return None

def search_jobs(df, search_terms, location=None, posted_after=None, job_type=None, experience_level=None, salary_range=None, sort_by=None):
    """Searches job listings based on various criteria."""
    filtered_df = df.copy()

    # Filter by keywords in job title, description, and requirements
    if search_terms:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(search_terms, case=False) |
                                filtered_df['Description'].str.contains(search_terms, case=False) |
                                filtered_df['Requirements'].str.contains(search_terms, case=False)]

    # Filter by location (if provided)
    if location:
        filtered_df = filtered_df[filtered_df['Location'] == location]

    # Filter by posted date (if provided)
    if posted_after:
        filtered_df = filtered_df[pd.to_datetime(filtered_df['Posted Date']) >= pd.to_datetime(posted_after)]

    # Filter by job type (if provided)
    if job_type:
        filtered_df = filtered_df[filtered_df['Job Type'] == job_type]

    # Filter by experience level (if provided)
    if experience_level:
        filtered_df = filtered_df[filtered_df['Experience Level'] == experience_level]

    # Filter by salary range (if provided)
    if salary_range:
        min_salary, max_salary = salary_range.split('-')
        min_salary = float(min_salary.strip().replace('₹', '').replace(',', ''))
        max_salary = float(max_salary.strip().replace('₹', '').replace(',', ''))
        filtered_df = filtered_df[(filtered_df['Salary Min (₹)'] >= min_salary) & (filtered_df['Salary Max (₹)'] <= max_salary)]

    # Sort the results (if provided)
    if sort_by:
        if sort_by == 'relevance':
            # Sort by relevance (based on keyword matches)
            # You may need to implement a custom relevance scoring algorithm here
            pass
        elif sort_by == 'job_score':
            filtered_df = filtered_df.sort_values(by='Job Score', ascending=False)
        elif sort_by == 'trending_score':
            filtered_df = filtered_df.sort_values(by='Trending Score', ascending=False)

    return filtered_df

def highlight_keywords(text, keywords):
    """Highlights search keywords within the provided text."""
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword}**")  # Replace with bold tags (adjust as needed)
    return text

def calculate_trending_score(df, window=7):
    """Calculates a trending score for each job based on recent views/applications."""
    # Assuming columns exist for 'Views' (in the last 'window' days) and 'Applications'
    df['Trending Score'] = df['Views'].rolling(window=window).mean() * 0.7 + df['Applications'].rolling(window=window).mean() * 0.3
    return df

def calculate_job_score(df, review_data=None):
    """Calculates a job score based on factors like company rating and (optional) reviews."""
    # Assuming a column 'Company Rating' exists
    df['Job Score'] = df['Company Rating']
    if review_data is not None:
        # Integrate logic to merge review data with job listings (e.g., by company ID)
        # and calculate a score based on review sentiment analysis (not implemented here)
        pass
    return df

def display_jobs(df, search_terms, num_to_print=5):
    """Prints information about the top job listings, highlighting matched keywords and trending scores."""
    if len(df) < num_to_print:
        num_to_print = len(df)
    if num_to_print == 0:
        print("No matching job listings found")
    else:
        for i in range(num_to_print):
            job = df.iloc[i]
            title = highlight_keywords(job['Title'], search_terms)
            company = job['Company']
            location = job['Location']
            link = job['Link']  # Assuming a 'Link' column exists for job listing URLs
            requirements = highlight_keywords(job['Requirements'], search_terms)
            trending_score = job['Trending Score']
            job_score = job['Job Score']
            print(f"Job #{i+1}:\n{title} at {company} ({location})\n")
            print(f"Job Score: {job_score:.1f} (based on company rating)")  # Display score with one decimal
            if trending_score > 0:
                print(f"Trending Score: {trending_score:.1f} (based on recent views/applications)\n")  # Display score with one decimal
            print(f"Requirements: {requirements}\n")
            print(f"More details: {link}\n")

# Example usage
data_file = "job_listings.csv"  # Replace with your actual data file path
job_df = load_job_listings(data_file)

# Example search query
search_terms = "Python Developer"
location = "Bangalore"
posted_after = "2023-01-01"
job_type = "Full-time"
experience_level = "Mid-level"
salary_range = "70000-100000"
sort_by = "job_score"

# Search for jobs based on the provided criteria
filtered_jobs = search_jobs(job_df, search_terms=search_terms, location=location, posted_after=posted_after,
                            job_type=job_type, experience_level=experience_level, salary_range=salary_range,
                            sort_by=sort_by)

# Display the filtered job listings
display_jobs(filtered_jobs, search_terms, num_to_print=5)
